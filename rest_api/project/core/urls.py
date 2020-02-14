from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AddToCartView,
    OrderDetailView,
    PaymentView,
    CountryListView,
    AddressViewSet,
    OrderItemDeleteView,
    OrderQuantityDecreaseView,
    AddCouponView,
    ItemViewSet,
    CategoryView,
    OrderListView,
    FiltersView,
)

router = DefaultRouter()
router.register("address", AddressViewSet, basename="address")
router.register("products", ItemViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
    path("cart/", OrderDetailView.as_view(), name="cart-get"),
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("cart/<int:pk>/delete/", OrderItemDeleteView.as_view(), name="cart-delete"),
    path("cart/update/", OrderQuantityDecreaseView.as_view(), name="cart-update"),
    path("coupon/add/", AddCouponView.as_view(), name="coupon-add"),
    path("category/", CategoryView.as_view(), name="category-list"),
    #
    path("checkout/", PaymentView.as_view(), name="checkout"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    #
    path("country-list/", CountryListView.as_view(), name="country-list"),
    path("filters/", FiltersView.as_view(), name="filters-values"),
]
