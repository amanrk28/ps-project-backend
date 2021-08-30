from django.urls import path
from . import views

urlpatterns = [
    path('product', views.ProductItemList.as_view()),
    path('product/<int:pk>', views.ProductItemDetail.as_view()),
]