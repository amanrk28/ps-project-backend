from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from authentication.models import User
from store.models import CartStatus, Product, Cart, CartItem, ProductCategory
from store.serializers import ProductSerializer, CartItemSerializer
from project_backend.utils import compute_hash, Response
from project_backend.renderer import ApiRenderer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_serializer(self, *args, **kwargs):
        included_fields = ('name', 'price', 'stock', 'is_available', 'description', 'category')
        return super(ProductList, self).get_serializer(*args, **kwargs, fields = included_fields)

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def create(self,request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.initial_data['added_by'] = request.user.id
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, msg="Successfully Created Product")


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# API view to fetch Product Categories List
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
@renderer_classes([ApiRenderer])
def get_product_categories(request):
    data = {'categories': [category[1] for category in ProductCategory.choices]}
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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.initial_data['cart_id'] = cart.id
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
