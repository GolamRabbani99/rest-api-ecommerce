from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from products.views import CategoryViewSet, ProductViewSet
from users.views import UserViewSet
from orders.views import OrderViewSet
from cart.views import CartViewSet, CartItemViewSet
from rest_framework_nested import routers

# Create a router for the main API endpoints.
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'carts', CartViewSet, basename='carts')

# Create a nested router for the items inside each cart.
carts_router = routers.NestedDefaultRouter(router, r'carts', lookup='cart')
carts_router.register(r'items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Use the router's URLs for our API.
    path('api/', include(router.urls)),
    path('api/', include(carts_router.urls)),
    
    # URL for authentication and token creation
    path('api/auth/', obtain_auth_token),
    
    # URL for browsable API authentication
    path('api-auth/', include('rest_framework.urls')),
]
