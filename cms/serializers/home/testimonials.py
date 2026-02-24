from rest_framework import serializers  # type: ignore
from apps.showcase.models.home import (
    TestimonialSection,
    Testimonial,
    TertimonialMetric,
)


class TestimonialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Testimonial
        fields = [
            "id",
            "author",
            "role",
            "content",
            "rating",
            "order",
        ]


class TertimonialMetricSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TertimonialMetric
        fields = [
            "id",
            "metric",
            "text",
            "order",
        ]


class TestimonialSectionSerializer(serializers.ModelSerializer):
    testimonials = TestimonialSerializer(many=True, required=False, default=list)
    metrics = TertimonialMetricSerializer(many=True, required=False, default=list)

    class Meta:
        model = TestimonialSection
        fields = [
            "id",
            "title",
            "testimonials",
            "metrics",
            "is_active",
            "order",
        ]
