from rest_framework import serializers
from apps.showcase.models.home import HeroSection


class HeroSectionSerializer(serializers.ModelSerializer):
    highlightWord = serializers.CharField(
        source="highlight_word",
        allow_null=True,
        allow_blank=True,
        required=False
    )
    
    class Meta:
        model = HeroSection
        fields = [
            "id",
            "headline",
            "highlightWord",
            "subheadline",
            "is_active",
            "imageUrl",
            "imageAlt",
            "textCta",
            "urlCta",
        ]
        
        
    def validate_urlCta(self, value):
        if not value.startswith("http"):
            raise serializers.ValidationError("La URL debe comenzar con http o https")
        return value