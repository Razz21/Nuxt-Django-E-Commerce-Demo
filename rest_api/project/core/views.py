from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings
from django.db.models import Q, Case, DecimalField, When, functions
from django.db import models


from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound

from rest_framework.decorators import action

from django_countries import countries

from .models import (
    Item,
    Order,
    OrderItem,
    Address,
    Payment,
    Category,
    UserProfile,
    Variant,
    Coupon,
    ItemColor,
    Material,
)
from .serializers import (
    ItemSerializer,
    OrderSerialzier,
    CouponSerializer,
    ItemDetailSerializer,
    AddressSerializer,
    PaymentSerializer,
    CategoryDetailSerializer,
    CategorySerializer,
    MaterialSerializer,
    ColorSerializer,
    OrderCompletedSerializer,
)
from .pagination import StandardResultsSetPagination, LeadListPagination
from .permissions import AccessOwnData, IsADmin
from .filters import ItemFilterSet
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class CategoryView(ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    paginator = None


class ItemViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = []  # not not authorize/ validate token -> raise Ex
    queryset = Item.objects.all()
    lookup_field = "slug"
    ordering_fields = ["name", "order_price"]  # allowed ordering fields
    # ordering = ["name"]  # default
    filterset_class = ItemFilterSet
    pagination_class = LeadListPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ItemDetailSerializer
        else:
            return ItemSerializer

    @action(detail=False, methods=["get"], url_path="category/(?P<slug>[^/.]+)")
    def category(self, request, slug=None):
        if slug is None:
            return Response({"detail": "Invalid data"}, status=HTTP_400_BAD_REQUEST)

        category = get_object_or_404(Category, slug=slug)

        category_items = self.filter_queryset(
            self.get_queryset().filter(category=category)
        )
        page = self.paginate_queryset(category_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(category_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        latest_items = self.get_queryset().order_by("-id")[:5]
        page = self.paginate_queryset(latest_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(latest_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """quick search preview to return only first 3 results and total count"""
        query = request.query_params.get("search")
        if not query:
            return Response({"detail": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
        # self.pagination_class.page_size = 3
        search_items = self.filter_queryset(self.get_queryset())
        count = search_items.count()
        search_items = search_items[:3]  # return only first 3 results

        serializer = self.get_serializer(search_items, many=True)
        return Response({"count": count, "results": serializer.data})


class OrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated | IsADmin]
    serializer_class = OrderSerialzier

    def get_object(self):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            raise NotFound(detail="You do not have an active order", code=404)
        return order


class OrderQuantityDecreaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = request.data.get("slug", None)
        if slug is None:
            return Response({"detail": "Invalid data"}, status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item, user=request.user, ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                return Response(status=HTTP_200_OK)
            else:
                return Response(
                    {"detail": "This item was not in your cart"},
                    status=HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "You do not have an active order"},
                status=HTTP_400_BAD_REQUEST,
            )


class OrderItemDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, AccessOwnData]
    queryset = OrderItem.objects.all()


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        slug = request.data.get("slug", None)
        variants = request.data.get("variants", [])

        if slug is None:
            return Response({"detail": "Invalid Request"}, status=HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Item, slug=slug)
        min_variant_count = Variant.objects.filter(item=item).count()
        if len(variants) < min_variant_count:
            return Response(
                {"detail": "Please specify requested parameters"},
                status=HTTP_400_BAD_REQUEST,
            )
        order_item_qs = OrderItem.objects.filter(
            item=item, user=request.user, ordered=False
        )

        for v in variants:
            order_item_qs = order_item_qs.filter(Q(item_variants__exact=v))

        if order_item_qs.exists():
            order_item = order_item_qs.first()
            order_item.quantity += 1
        else:
            order_item = OrderItem.objects.create(
                item=item, user=request.user, ordered=False
            )
            order_item.item_variants.add(*variants)
        order_item.save()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if not order.items.filter(item__id=order_item.id).exists():
                order.items.add(order_item)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, order_date=ordered_date)
            order.items.add(order_item)

        return Response(status=HTTP_200_OK)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        userprofile = UserProfile.objects.get(user=self.request.user)
        token = request.data.get("stripeToken")

        billing_address_id = request.data.get("billing_id")
        shipping_address_id = request.data.get("shipping_id")

        billing_address = get_object_or_404(
            Address, id=billing_address_id, user=self.request.user
        )
        shipping_address = get_object_or_404(
            Address, id=shipping_address_id, user=self.request.user
        )

        if (
            userprofile.stripe_customer_id != ""
            and userprofile.stripe_customer_id is not None
        ):
            customer = stripe.Customer.retrieve(userprofile.stripe_customer_id)
            customer.sources.create(source=token)

        else:
            customer = stripe.Customer.create(email=self.request.user.email)
            customer.sources.create(source=token)
            userprofile.stripe_customer_id = customer["id"]
            userprofile.one_click_purchasing = True
            userprofile.save()

        amount = int(order.get_total() * 100)

        try:

            # charge the customer because we cannot charge the token more than once
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                customer=userprofile.stripe_customer_id,
            )
            # charge once off on the token
            # charge = stripe.Charge.create(
            #     amount=amount,  # cents
            #     currency="usd",
            #     source=token
            # )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge["id"]
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.billing_address = billing_address
            order.shipping_address = shipping_address
            # order.ref_code = create_ref_code()
            order.save()

            return Response(status=HTTP_200_OK)

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get("error", {})
            return Response(
                {"detail": f"{err.get('message')}"}, status=HTTP_400_BAD_REQUEST
            )

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return Response({"detail": "Rate limit error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            print(e)
            # Invalid parameters were supplied to Stripe's API
            return Response(
                {"detail": "Invalid parameters"}, status=HTTP_400_BAD_REQUEST
            )

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return Response(
                {"detail": "Not authenticated"}, status=HTTP_400_BAD_REQUEST
            )

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return Response({"detail": "Network error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return Response(
                {
                    "detail": "Something went wrong. You were not charged. Please try again."
                },
                status=HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # send an email to ourselves
            return Response(
                {"detail": "A serious error occurred. Please, try again later."},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": "Invalid data"}, status=HTTP_400_BAD_REQUEST)


class AddCouponView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        code = request.data.get("code", None)
        if code is None:
            return Response({"detail": "Invalid data"}, status=HTTP_400_BAD_REQUEST)
        print(code)
        order = Order.objects.get(user=self.request.user, ordered=False)
        coupon = get_object_or_404(Coupon, code=code)
        order.coupon = coupon
        order.save()
        return Response(status=HTTP_200_OK)


class CountryListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(countries, status=HTTP_200_OK)


class AddressViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, AccessOwnData)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     if request.data["default"] == True:
    #         self.removeDefaultAddress(request.data["address_type"])
    #     return super().create(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     if request.data["default"] == True:
    #         self.removeDefaultAddress(request.data["address_type"])
    #     return super().update(request, *args, **kwargs)

    # def removeDefaultAddress(self, address_type):
    #     qs = Address.objects.filter(user=self.request.user, address_type=address_type)
    #     if qs.exists():
    #         qs.update(default=False)


class OrderListView(ListAPIView):
    permission_classes = (IsAuthenticated | IsADmin,)
    serializer_class = OrderCompletedSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, ordered=True)


class FiltersView(APIView):
    def get(self, request, *args, **kwargs):

        colors = ItemColor.objects.all()
        colors_serializer = ColorSerializer(colors, many=True).data
        materials = Material.objects.all()
        materials_serializer = MaterialSerializer(materials, many=True).data
        max_price = round(
            Item.objects.aggregate(models.Max("order_price"))["order_price__max"]
        )
        return Response(
            {
                "colors": colors_serializer,
                "materials": materials_serializer,
                "max_price": max_price,
            }
        )

