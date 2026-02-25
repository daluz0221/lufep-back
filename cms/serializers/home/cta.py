from rest_framework import serializers # type: ignore

from apps.showcase.models.home import FinalCTASection


class FinalCTASectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FinalCTASection
        fields = [
            "id",
            "headline",
            "subheadline",
            "button_text",
            "button_url",
        ]
        
    def validate_button_url(self, value):
        if not value.startswith("http"):
            raise serializers.ValidationError("La URL debe comenzar con http o https")
        return value    
    
