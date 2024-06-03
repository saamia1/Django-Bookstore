# cart/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CartViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet)
router.register(r'', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('purchase/', CartViewSet.as_view({'post': 'purchase'}), name='cart-purchase'),
    path('view-cart-items/', CartViewSet.as_view({'get': 'view_cart_items'}), name='view-cart-items'),
]
