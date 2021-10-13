from django.core.exceptions import FieldDoesNotExist
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.decorators import api_view, permission_classes, renderer_classes
import django_filters.rest_framework as filters
from authentication.models import User
from authentication.config import *
from project_backend.utils import Response, get_datetime_from_timestamp, permission_required
from order.models import Order, OrderItem
from order.config import ORDER_DATE_FIELDS
from order.serializers import OrderSerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.with_closed_objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,
                          permission_required([ADD_ORDER, READ_ORDER]))
    filter_backends = [filters.DjangoFilterBackend,]
    filterset_fields = ('status', 'placed_by')

    def list(self, request, *args, **kwargs):
        user: User = request.user
        queryset = self.get_queryset()
        if not user.is_admin and not user.is_store_owner and not user.is_superuser:
            queryset = Order.with_closed_objects.filter(placed_by=user).order_by('-id')
        return Response(OrderSerializer(queryset, many=True).data)

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
        serializer.is_valid(raise_exception=True)
        serializer.save()

        order = serializer.data['id']
        for item in products:
            OrderItem.objects.create({'product': item.product, 'quantity': item.quantity, 'order': order})

        return Response(serializer.data, msg="Order created Successfully")

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.with_closed_objects.all()
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

        for key, value in data.items():
            try:
                _ = Order._meta.get_field(key)
            except FieldDoesNotExist:
                data['more_details'][key] = value

        res_data = self.partial_update(request, *args, **kwargs)
        res_instance = Order.all_objects.get(id=res_data.data['id'])
        return Response(self.get_serializer(res_instance).data)

    def put(self, request, *args, **kwargs):
        user: User = request.user
        if user.has_perm(UPDATE_ORDER):
            return self.update_data(request, *args, **kwargs)
        else:
            raise PermissionDenied()