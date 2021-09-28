from django.urls import path
from . import views

urlpatterns = [
    path('product', views.ProductList.as_view()),
    path('product/<int:pk>', views.ProductDetail.as_view()),
    path('product_categories', views.get_product_categories),
    path('cart', views.CartItemList.as_view()),
    path('cart/<int:pk>', views.CartItemDetail.as_view()),
    path('checkout', views.checkout_page_details),
    path('order_from_cart', views.order_from_cart),
]