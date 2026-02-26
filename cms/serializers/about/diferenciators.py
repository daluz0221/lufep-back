from rest_framework import serializers # type: ignore
from apps.showcase.models.about import AboutDifferentiatorsSection, AboutDifferentiator


class AboutDifferentiatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutDifferentiator
        fields = [
            "id",
            "title",
            "description",
            "order",
        ]
        
class AboutDifferentiatorsSectionSerializer(serializers.ModelSerializer):
    differentiators = AboutDifferentiatorSerializer(many=True)
    class Meta:
        model = AboutDifferentiatorsSection
        fields = [
            "id",
            "title",
            "differentiators",
            "is_active",
            "order",
        ]