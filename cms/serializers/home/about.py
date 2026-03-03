from rest_framework import serializers  # type: ignore
from apps.showcase.models.home import AboutSection, AboutMetric


class AboutMetricSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = AboutMetric
        fields = [
            "id",
            "metric",
            "text",
            "order",
        ]


class AboutSectionSerializer(serializers.ModelSerializer):
    metrics = AboutMetricSerializer(many=True)

    class Meta:
        model = AboutSection
        fields = [
            "id",
            "title",
            "text",
            "cta_text",
            "cta_url",
            "metrics",
            "is_active",
            "order",
        ]
