from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.core.validators import MinValueValidator, RegexValidator

from decimal import Decimal

from django_countries.fields import CountryField

USER = get_user_model()


LABEL_CHOICES = (("N", "New"), ("P", "Popular"), ("D", "Discount"))
ADDRESS_CHOICES = (("B", "Billing"), ("S", "Shipping"))
DISCOUNT_UNIT_CHOICES = (("C", "$"), ("P", "%"))


# todo database shopping cart


class ItemManager(models.Manager):
    def get_queryset(self):
        # custom price order filter based on regular and discount price (if exists)
        qs = super().get_queryset()

        qs = qs.annotate(
            order_price=models.Case(
                models.When(discount_price__isnull=False, then="discount_price"),
                default="price",
            )
        )

        return qs


def get_upload_path(instance, filename):
    """ create directory for item images """
    return f"products/{instance.item.id}/{filename}"


def get_upload_variant_path(instance, filename):
    """ create directory for item images """
    return f"variants/{instance.variant.id}/{filename}"


class ItemColor(models.Model):
    name = models.CharField(max_length=64)
    hex = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex="^#(?:[0-9a-fA-F]{3}){1,2}$",
                message="Hex color format needs to be #xxx or #xxxxxx",
            )
        ],
    )

    def __str__(self):
        return f"{self.name}-{self.hex}"

    class Meta:
        ordering = ["name"]


class Material(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class UserProfile(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.address_type}"

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if self.default == True:
            qs = Address.objects.filter(
                user=self.user, default=True, address_type=self.address_type
            )
            if qs.exists():
                qs.update(default=False)
        return super().save(*args, **kwargs)


class AddressDefaults(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    shipping = models.ForeignKey(
        "Address",
        related_name="default_shipping",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    billing = models.ForeignKey(
        "Address",
        related_name="default_billing",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Addresses defaults"

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal("0.01"))]
    )
    discount_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    category = models.ManyToManyField(Category, related_name="items")
    label = models.CharField(
        choices=LABEL_CHOICES, max_length=1, blank=True, null=True, default="N"
    )
    slug = models.SlugField(unique=True)
    description = models.TextField()
    # todo thumbnail img
    # https://stackoverflow.com/questions/23922289/django-pil-save-thumbnail-version-right-when-image-is-uploaded
    # thumbnail = models.ImageField(editable=False)
    color = models.ForeignKey(
        ItemColor, related_name="items", on_delete=models.DO_NOTHING, null=True
    )
    material = models.ManyToManyField(Material, related_name="items")
    objects = ItemManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ItemImages(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_upload_path, default="default.jpg")

    class Meta:
        verbose_name = "Item Image"
        verbose_name_plural = "Item Images"

    def delete(self, *args, **kwargs):
        # remove file from storage
        if self.image != "default.jpg":
            self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # remove old file on update
        try:
            this = ItemImages.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        return super().save(*args, **kwargs)


class Variant(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # size

    class Meta:
        unique_together = ("item", "name")

    def __str__(self):
        return self.name


class ItemVariant(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)  # S, M, L
    attachment = models.ImageField(blank=True, upload_to=get_upload_variant_path)

    class Meta:
        unique_together = ("variant", "value")

    def __str__(self):
        return self.value

    def delete(self, *args, **kwargs):
        # remove file from storage
        self.attachment.delete()
        super().delete(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_variants = models.ManyToManyField(ItemVariant)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(
        USER, related_name="orders_created", on_delete=models.CASCADE
    )
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        "Address",
        related_name="billing_address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    shipping_address = models.ForeignKey(
        "Address",
        related_name="shipping_address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    payment = models.ForeignKey(
        "Payment", on_delete=models.SET_NULL, null=True, blank=True
    )
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.SET_NULL, null=True, blank=True
    )
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-order_date"]

    def __str__(self):
        return self.user.username

    def get_subtotal(self):
        subtotal = 0
        for order_item in self.items.all():
            subtotal += order_item.get_final_price()
        return subtotal

    def get_total(self):
        total = self.get_subtotal()

        if self.coupon:
            if self.coupon.unit == "P":
                total = round(
                    Decimal(total)
                    - round(
                        (Decimal(self.coupon.amount) / Decimal("100") * Decimal(total)),
                        2,
                    ),
                    2,
                )
            else:
                total -= Decimal(self.coupon.amount)
        return total


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["-timestamp"]


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    unit = models.CharField(choices=DISCOUNT_UNIT_CHOICES, max_length=1, default="C")

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


""" =========== signals =========== """


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    """ create user profile on register """
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=USER)


# def create_product(sender, instance, created, **kwargs):
#     """ assign default image to item if not set any """
#     """ moved to admin validation """
#     if created:
#         if instance.images.empty():
#             ItemImages.objects.create(item=instance)
#         else:
#             pass
# post_save.connect(create_product, sender=Item)


def delete_item(sender, instance, using, **kwargs):
    """ delete reated images on item delete """
    for img in instance.images.all():
        img.delete()


pre_delete.connect(delete_item, sender=Item)
