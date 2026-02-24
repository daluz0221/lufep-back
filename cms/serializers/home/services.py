from rest_framework import serializers #type: ignore
from apps.showcase.models.home import ServiceSection, Service


class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    
    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "short_description",
            "description",
            "image",
            "url_text",
            "ur",
            "order",
        ]
        
        
class SerivceSectionSerializer(serializers.ModelSerializer):
    
    servicios = ServiceSerializer(many=True)
    
    
    class Meta:
        model = ServiceSection
        fields = [
            "id",
            "title",
            "subtitle",
            "url",
            "servicios",
            "is_active",
            "order"
        ]
        
        