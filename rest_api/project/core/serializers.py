from rest_framework import serializers
from .models import (
    Item,
    ItemImages,
    Category,
    Order,
    OrderItem,
    Coupon,
    Variant,
    ItemVariant,
    Address,
    Payment,
    ItemColor,
    Material,
)
from django_countries.serializer_fields import CountryField


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemColor
        fields = ("id", "name", "hex")


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    # todo category image?

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "items_count")

    def get_items_count(self, obj):
        return obj.items.count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "items")

    def get_items(self, obj):
        return ItemDetailSerializer(obj.items.all(), many=True).data


class ImageSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = ItemImages
        fields = ("id", "path")

    def get_path(self, obj):
        return obj.image.url


class CouponSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ("id", "code", "amount", "unit")

    def get_unit(self, obj):
        return obj.get_unit_display()


class ItemBaseSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)
    color = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "price",
            "discount_price",
            "category",
            "label",
            "slug",
            "color",
        )
        read_only_fields = ("slug",)

    def get_label(self, obj):
        return obj.get_label_display()

    def get_color(self, obj):
        return obj.color.hex


class ItemSerializer(ItemBaseSerializer):
    image = serializers.CharField(source="images.first.image.url")  # first image

    class Meta:
        model = Item
        fields = ItemBaseSerializer.Meta.fields + ("image",)


class MaterialNameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Material


class ItemDetailSerializer(ItemBaseSerializer):
    variants = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    material = MaterialNameSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ItemBaseSerializer.Meta.fields + (
            "images",
            "material",
            "variants",
            "description",
        )

    def get_variants(self, obj):
        return VariantSerializer(obj.variant_set.all(), many=True).data

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(), many=True).data


class ItemVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVariant
        fields = ("id", "value", "attachment")


class ItemVariantDetailSerializer(serializers.ModelSerializer):
    variant = serializers.SerializerMethodField()

    class Meta:
        model = ItemVariant
        fields = ("id", "value", "attachment", "variant")

    def get_variant(self, obj):
        return VariantDetailSerializer(obj.variant).data


class VariantSerializer(serializers.ModelSerializer):
    item_variants = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ("id", "name", "item_variants")

    def get_item_variants(self, obj):
        return ItemVariantSerializer(obj.itemvariant_set.all(), many=True).data


class VariantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ("id", "name")


class OrderItemSerialzier(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    item_variants = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("id", "item", "item_variants", "quantity", "final_price")

    def get_item(self, obj):
        return ItemSerializer(obj.item).data

    def get_item_variants(self, obj):
        return ItemVariantDetailSerializer(obj.item_variants.all(), many=True).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class OrderSerialzier(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "items", "total", "subtotal", "coupon")

    def get_items(self, obj):
        return OrderItemSerialzier(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()

    def get_subtotal(self, obj):
        return obj.get_subtotal()

    def get_coupon(self, obj):
        if obj.coupon is not None:
            return CouponSerializer(obj.coupon).data
        return None


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "street_address",
            "apartment_address",
            "country",
            "zip",
            "address_type",
            "default",
        )
        read_only_fields = ("user",)

    # def create(self, request, validated_data):
    #     address, created = Address.objects.update_or_create(**validated_data)
    #     return address


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "amount", "timestamp")


class OrderCompletedSerializer(OrderSerialzier):
    payment = serializers.SerializerMethodField()

    class Meta(OrderSerialzier.Meta):
        model = Order
        fields = OrderSerialzier.Meta.fields + ("payment",)

    def get_payment(self, obj):
        return PaymentSerializer(obj.payment).data
