from rest_framework import serializers # type: ignore
from apps.showcase.models.about import AboutIntroSection


class AboutIntroSectionSerializer(serializers.ModelSerializer):
    highlightWord = serializers.CharField(
        source="highlight_word",
        allow_null=True,
        allow_blank=True,
        required=False
    )
    
    class Meta:
        model = AboutIntroSection
        fields = [
            "id",
            "title",
            "highlightWord",
            "description",
            "is_active",
            "order",
        ]
        