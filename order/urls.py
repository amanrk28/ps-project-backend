from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.OrderList.as_view()),
    path('orders/<int:pk>', views.OrderDetail.as_view()),
    path('orders/<int:pk>/cancel', views.cancel_order)
]