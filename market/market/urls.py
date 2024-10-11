from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from marketAPI.views import PartnerUpdateView, ProductView, BasketProductViewSet, OrderProductModelViewSet, \
    UpdateUserAddressView

router = DefaultRouter()
router.register(r'basket', BasketProductViewSet, basename='basket')
router.register(r'orders', OrderProductModelViewSet, basename='orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('lk/address/', UpdateUserAddressView.as_view()),
    path('update/', PartnerUpdateView.as_view()),
    path('products/', ProductView.as_view()),
    path('product/<int:pk>/', ProductView.as_view()),
    path('', include(router.urls)),
]
