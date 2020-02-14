from django_filters import rest_framework as filters
from rest_framework.serializers import ValidationError
from .models import Item


class NumberRangeFilter(filters.BaseRangeFilter, filters.NumberFilter):
    pass


class ListFilter(filters.Filter):
    """
    handle multiple digit values in one query param
    """

    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = "in"
        list_values = value.strip(",").split(",")
        if not all(item.isdigit() for item in list_values):
            raise ValidationError(f"All values in {list_values} the are not integer")
        return super().filter(qs, list_values)


class ItemFilterSet(filters.FilterSet):
    price = NumberRangeFilter(
        field_name="order_price", lookup_expr="range", label="Order price is in range"
    )
    color = ListFilter(field_name="color", lookup_expr="in", distinct=True)
    material = ListFilter(field_name="material", lookup_expr="in", distinct=True)

    search = filters.CharFilter(lookup_expr="icontains", field_name="name")

    class Meta:
        model = Item
        fields = ["search", "price", "color", "material"]
