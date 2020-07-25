from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.shortcuts import get_object_or_404
from .models import (
    Item,
    ItemImages,
    OrderItem,
    Order,
    Category,
    Payment,
    Coupon,
    Address,
    Refund,
    UserProfile,
    Variant,
    ItemVariant,
    AddressDefaults,
    ItemColor,
    Material,
)
from .forms import MultipleImagesForm, ItemColorForm, ItemForm


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = "Update orders to refund granted"


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "products_count"]

    def products_count(self, instance):
        return instance.items.count()


@admin.register(ItemColor)
class ItemColorAdmin(admin.ModelAdmin):
    form = ItemColorForm
    search_fields = ["name"]
    list_display = ["name", "products_count",  "color_preview"]

    def color_preview(self, obj):
        return format_html(
            f"""
            <div style="height:20px;width:20px;background-color:{obj.hex}"></div>
            """
        )

    color_preview.short_description = "Preview"

    def products_count(self, instance):
        return instance.items.count()


class AddItemImagesInline(admin.TabularInline):
    """ dedicated input form for uploading product images """

    # FIXME double saving last image
    model = ItemImages
    form = MultipleImagesForm
    extra = 0
    max_num = 1

    fields = ["image"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


class ItemImagesInline(admin.TabularInline):
    # form = MultipleImagesForm
    model = ItemImages
    min_num = 1  # required for validation
    extra = 0
    readonly_fields = ["item_image"]

    def item_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75" height=75/>')

    def get_formset(self, request, obj=None, **kwargs):
        """ validate for minimum one image on model save """
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset

    # def has_add_permission(self, request):
    # # uncomment if use dedicated input form
    #     return False

    # def has_change_permission(self, request, obj=None):
    # # uncomment if use dedicated input form
    #     return False


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = (
        "id",
        "name",
        "price",
        "discount_price",
        "categories",
        "label",
        "color",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "label"]

    inlines = [ItemImagesInline]
    list_editable = ["label", "color"]
    # inlines = [AddItemImagesInline, ItemImagesInline]

    def categories(self, obj):
        return " / ".join([p.name for p in obj.category.all()])

    # def save_model(self, request, obj, form, change):
    # # todo add multiple files from one formfield
    # files = request.FILES.getlist("images-0-image")
    # for f in files:
    #     instance = ItemImages(image=f, item=obj)
    #     instance.save()
    # super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "products_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def products_count(self, instance):
        return instance.items.count()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
        "billing_address",
        "shipping_address",
        "payment",
        "coupon",
    )
    list_display_links = [
        "user",
        "billing_address",
        "shipping_address",
        "payment",
        "coupon",
    ]
    list_filter = (
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
    )
    search_fields = ["user__username", "ref_id"]
    actions = [make_refund_accepted]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "street_address",
        "apartment_address",
        "country",
        "zip",
        "address_type",
        "default",
        "get_is_default",
    ]
    list_filter = ["default", "address_type", "country"]
    search_fields = ["user", "street_address", "apartment_address", "zip"]

    def get_is_default(self, obj):
        return obj.default_shipping.exists() or obj.default_billing.exists()

    get_is_default.short_description = "Is default"


@admin.register(AddressDefaults)
class AddressDefaultsAdmin(admin.ModelAdmin):
    list_display = ["user", "shipping", "billing"]
    search_fields = ["user"]

    object = None

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if self.object and db_field.name == "billing" or db_field.name == "shipping":
    #         kwargs["queryset"] = Address.objects.filter(user=self.object.user.id)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_object(self, request, object_id, from_field=None):
    #     self.object = super().get_object(request, object_id)
    #     return self.object


@admin.register(ItemVariant)
class ItemVariantAdmin(admin.ModelAdmin):
    list_display = ["variant", "value", "attachment"]
    list_filter = ["variant", "variant__item"]
    search_fields = ["value"]


class ItemVariantInLineAdmin(admin.TabularInline):
    model = ItemVariant
    extra = 1


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ["item", "name"]
    list_filter = ["item"]
    search_fields = ["name"]
    inlines = [ItemVariantInLineAdmin]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "amount", "unit"]
    list_filter = ["code", "unit"]
    search_fields = ["code"]


admin.site.register(OrderItem)
admin.site.register(Payment)

admin.site.register(Refund)
