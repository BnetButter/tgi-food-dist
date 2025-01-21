from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet, RoleViewSet
from api import views


# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'distribution-center', views.DistributionCenterViewSet, basename='distribution-center')
router.register(r'inventory-item', views.InventoryItemViewSet, basename="inventory-item")
urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
]