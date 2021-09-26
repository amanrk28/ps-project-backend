from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls'), name='auth'),
    path('store/', include('store.urls'), name='store'),
    path('order/', include('order.urls'), name='order'),
]
