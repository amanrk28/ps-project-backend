from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.OrderList.as_view()),
    # path('product/<int:pk>', views.ProductItemDetail.as_view()),
]