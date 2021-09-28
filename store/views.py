import datetime
from rest_framework import generics, filters as searchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.decorators import api_view, permission_classes, renderer_classes
import django_filters.rest_framework as filters

from authentication.models import User
from authentication.config import *
from store.models import CartStatus, Product, Cart, CartItem, ProductCategory
from store.serializers import CartSerializer, ProductSerializer, CartItemSerializer
from order.models import Order, OrderItem
from project_backend.utils import compute_hash, Response, permission_required
from project_backend.renderer import ApiRenderer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_on')
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend, searchFilter.SearchFilter)
    filterset_fields = ['category',]
    search_fields = ['^name']

    def get_serializer(self, *args, **kwargs):
        included_fields = ('id', 'name', 'price', 'image', 'stock', 'is_available', 'description', 'category', 'added_by')
        return super(ProductList, self).get_serializer(*args, **kwargs, fields = included_fields)

    def create(self,request, *args, **kwargs):
        user: User = request.user
        if not user.has_perm(ADD_PRODUCT) or not user.is_store_owner or not user.is_admin:
            raise PermissionDenied()
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.initial_data['added_by'] = request.user.id
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, msg="Successfully Created Product")


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,
                          permission_required([UPDATE_PRODUCT, DELETE_PRODUCT, READ_PRODUCT]))

    def get_object(self):
        try:
            return Product.objects.get(id=self.kwargs.get('pk'))
        except Product.DoesNotExist:
            raise APIException("Product Not Found")

    def put(self, request, *args, **kwargs):
        user: User = request.user
        if not user.is_store_owner and not user.is_admin:
            raise PermissionDenied()
        product: Product = self.get_object()
        if 'name' in request.data and request.data.get('name') != product.name:
            raise APIException("Cannot change Product Name")
        return self.partial_update(request, *args, **kwargs)


# API view to fetch Product Categories List
@api_view(["GET"])
@permission_classes((AllowAny,))
@renderer_classes([ApiRenderer])
def get_product_categories(request):
    data = {'categories': [{ 'id': category[0], 'name':category[1]} for category in ProductCategory.choices]}
    return Response(data)


class CartItemList(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user: User = None if self.request.user.is_anonymous else self.request.user
        try:
            cart = Cart.objects.get(user=user, status=CartStatus.NEW)
            return CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            return CartItem.objects.none()

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        user: User = None if request.user.is_anonymous else request.user

        if not product_id or not Product.objects.filter(id=product_id).exists():
            raise APIException("Please enter valid Product")

        try:
            cart = Cart.objects.get(user=user, status=CartStatus.NEW)
        except Cart.DoesNotExist:
            hash_id = compute_hash()
            cart = Cart.objects.create(user=user, hash=hash_id)

        if CartItem.objects.filter(cart=cart, product=product_id).exists():
            raise APIException("Product already Added to Cart")

        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['cart_id'] = cart.id
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_cart(self):
        user: User = None if self.request.user.is_anonymous else self.request.user
        try:
            return Cart.objects.get(user=user, status=CartStatus.NEW)
        except Cart.DoesNotExist:
            raise APIException("Cart Not Found")

    def get_object(self):
        cart = self.get_cart()
        try:
            return CartItem.objects.get(cart=cart, product_id=self.kwargs.get('pk'))
        except:
            raise APIException("Cart Item does not exists")

    def put(self, request, *args, **kwargs):
        data = request.data
        cart_item = self.get_object()
        # Add cart id and product id when updating item in cart
        data['cart_id'] = cart_item.cart.id
        data['product_id'] = self.kwargs.get('pk')
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        super(CartItemDetail, self).delete(request, *args, **kwargs)
        cart = self.get_cart()
        res = {'cart_count': CartItem.objects.filter(cart=cart).count()}
        return Response(res, msg="Successfully deleted Item from Cart")

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
@renderer_classes([ApiRenderer])
def checkout_page_details(request):
    user: User = request.user
    cart_hash = request.data.get('cart_hash')

    if not cart_hash or not Cart.objects.filter(hash=cart_hash).exists():
        raise APIException("Cart Doesnot Exist")

    try:
        cart = Cart.objects.get(user=user, hash=cart_hash, status=CartStatus.NEW)
    except Cart.DoesNotExist:
        raise APIException("Please refresh your page once")

    try:
        cart_items_qs = CartItem.objects.filter(cart=cart)
        total_amount = 0
        for item in list(cart_items_qs):
            cart_item = CartItemSerializer(item).data
            total_amount += cart_item['amount']
    except CartItem.DoesNotExist:
        raise APIException("Cart is empty. Add items to cart to proceed")

    serializer = CartSerializer(cart)
    data = serializer.data
    data.update({'total_amount': total_amount})
    return Response(data, msg="Checkout page details")



@api_view(["POST"])
@permission_classes((IsAuthenticated, permission_required([ADD_ORDER, DELETE_CARTITEM, READ_CART, READ_CARTITEM, UPDATE_CART])))
@renderer_classes([ApiRenderer])
def order_from_cart(request):
    user: User = request.user
    cart_hash = request.data.get('cart_hash')

    if not cart_hash or not Cart.objects.filter(hash=cart_hash).exists():
        raise APIException("Cart Doesnot Exist")

    try:
        cart = Cart.objects.get(user=user, hash=cart_hash, status=CartStatus.NEW)
    except Cart.DoesNotExist:
        raise APIException("Please refresh your page once")

    try:
        cart_items = CartItem.objects.filter(cart=cart)
    except CartItem.DoesNotExist:
        raise APIException("Cart is empty. Add items to cart to proceed")

    dispatch_eta = datetime.datetime.now() + datetime.timedelta(days=2)
    delivery_eta = dispatch_eta + datetime.timedelta(days=2)
    order_data = {'placed_by': user, 'delivery_address': user.address,
                  'expected_dispatch_date': dispatch_eta, 'expected_delivery_date': delivery_eta}

    order = Order.objects.create(**order_data)

    for item in cart_items:
        order_item = {'product_id': item.product.id, 'quantity': item.quantity, 'order_id': order.id}
        OrderItem.objects.create(**order_item)

    cart.status = CartStatus.ORDERED
    cart.save()
    CartItem.objects.filter(cart=cart.id).delete()
    return Response({'order_id': order.id}, msg="Order Created")