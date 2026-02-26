from rest_framework import serializers # type: ignore
from apps.showcase.models.about import AboutVisionSection, AboutVisionItem


class AboutVisionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutVisionItem
        fields = [
            "id",
            "title",
            "description",
            "order",
        ]
        

class AboutVisionSectionSerializer(serializers.ModelSerializer):
    vision_items = AboutVisionItemSerializer(many=True)
    class Meta:
        model = AboutVisionSection
        fields = [
            "id",
            "title",
            "vision_items",
            "is_active",
            "order",
        ]