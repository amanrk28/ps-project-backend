import datetime
from django.core.exceptions import FieldDoesNotExist
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from django_filters.rest_framework import DjangoFilterBackend
from authentication.models import User
from authentication.config import *
from project_backend.utils import Response, get_datetime_from_timestamp, permission_required
from order.models import Order, OrderItem, OrderStatus
from order.config import ORDER_DATE_FIELDS
from order.serializers import OrderSerializer
from store.models import Product
from project_backend.renderer import ApiRenderer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.with_closed_objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,
                          permission_required([ADD_ORDER, READ_ORDER]))
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ('status')

    def list(self, request, *args, **kwargs):
        user: User = request.user
        queryset = self.get_queryset()
        if not user.is_admin and not user.is_store_owner and not user.is_superuser:
            queryset = Order.with_closed_objects.filter(placed_by=user).order_by('-id')
        status = request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        included_fields = ['id', 'placed_by', 'order_date', 'expected_delivery_date', 'status', 'delivery_date']
        return Response(OrderSerializer(queryset, many=True, fields=included_fields).data)

    def create(self, request, *args, **kwargs):
        data = request.data
        products = data.pop('products', None)

        if not request.user.is_admin:
            return PermissionDenied()

        if 'more_details' not in data:
            data['more_details'] = dict()

        if not products:
            raise APIException("Not Product added to cart. Cannot create Order")

        for key, value in data.items():
            try:
                _ = Order._meta.get_field(key)
            except FieldDoesNotExist:
                data['more_details'][key] = value

        serializer = self.get_serializer(data=data)
        serializer.initial_data['placed_by'] = request.user.id
        serializer.initial_data['cancellation_time_limit'] = datetime.datetime.now() + datetime.timedelta(hours=1)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        order = serializer.data['id']
        for item in products:
            product_price = Product.objects.get(id=item.product).price
            OrderItem.objects.create({'product': item.product, 'quantity': item.quantity, 'order': order, 'amount': product_price * item.quantity})

        return Response(serializer.data, msg="Order created Successfully")

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.with_closed_objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,
                          permission_required([ADD_ORDER, READ_ORDER]))

    def get_object(self):
        try:
            order = Order.with_closed_objects.get(pk=self.kwargs.get('pk'))
            return order
        except Order.DoesNotExist:
            raise APIException("Unable to get Order details")

    def get(self, request, *args, **kwargs):
        user: User = request.user
        order = self.get_object()
        if not user.has_perm(READ_ORDER):
            raise PermissionDenied()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def update_data(self, request, *args, **kwargs):
        data = request.data
        if not 'more_details' in data:
            data['more_details'] = dict()

        for field in ORDER_DATE_FIELDS:
            if field in data and data[field]:
                data[field] = get_datetime_from_timestamp(data[field])

        if 'status' in data and data.get('status'):
            status = data.get('status')
            if status == 'dispatched':
                data['dispatch_date'] = datetime.datetime.now()
            elif status == 'closed':
                data['delivery_date'] = datetime.datetime.now()

        for key, value in data.items():
            try:
                _ = Order._meta.get_field(key)
            except FieldDoesNotExist:
                data['more_details'][key] = value

        self.partial_update(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        user: User = request.user
        if user.has_perm(UPDATE_ORDER):
            return self.update_data(request, *args, **kwargs)
        else:
            raise PermissionDenied()

@api_view(["GET"])
@permission_classes((IsAuthenticated, permission_required([UPDATE_ORDER])))
@renderer_classes([ApiRenderer])
def cancel_order(request, pk):
    user: User = request.user
    if not user.has_perm(UPDATE_ORDER):
        raise PermissionDenied()
    order = Order.all_objects.get(id=pk)
    if timezone.now() > order.cancellation_time_limit:
        raise APIException("Order cannot be cancelled anymore!")
    else:
        order.cancelled = True
        order.status = OrderStatus.CANCELLED
        order.save()
        return Response("Order cancelled Successfully")

