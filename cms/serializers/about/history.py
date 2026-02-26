from rest_framework import serializers # type: ignore
from apps.showcase.models.about import AboutHistorySection


class AboutHistorySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutHistorySection
        fields = [
            "id",
            "title",
            "image",
            "image_alt",
            "content",
            "is_active",
            "order",
        ]