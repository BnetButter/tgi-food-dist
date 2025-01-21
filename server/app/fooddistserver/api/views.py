from rest_framework import viewsets
from .models import DistributionCenter
from .serializers import DistributionCenterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
import json
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class DistributionCenterViewSet(viewsets.ModelViewSet):
    queryset = DistributionCenter.objects.all()
    serializer_class = DistributionCenterSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']  # Add the field(s) you want to filter by

    @action(detail=False, methods=['get'])
    def geojson(self, request):
        """
        Custom action to generate a GeoJSON of all distribution centers.
        """
        distribution_centers = DistributionCenter.objects.all()
        
        features = []
        for center in distribution_centers:
            
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [center.longitude, center.latitude]
                },
                "properties": {
                    "id": center.id,
                    "address": center.address,
                    "user": center.user.id,
                    "center_name": center.center_name,
                    "poc_email": center.poc_email,
                    "poc_phone_number": str(center.poc_phone_number),
                    "distribution_type": center.distribution_type,
                    "other_description": center.other_description
                }
            })

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        return Response(geojson)
   
    def get_permissions(self):
        """
        Override get_permissions to allow unauthenticated access to the geojson action.
        """
        if self.action == 'geojson':
            return [AllowAny()]  # No authentication required
        return super().get_permissions()

from rest_framework.filters import SearchFilter
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from rest_framework.pagination import PageNumberPagination
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['distribution_center']  # Explicit filtering by distribution_center
    search_fields = ['name']  # Search by name

    class pagination_class(PageNumberPagination):
        page_size = 10  # Default page size
        page_size_query_param = 'page_size'  # Enables the `page_size` query parameter
