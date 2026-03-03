from rest_framework import serializers  # type: ignore
from apps.showcase.models.products import ProductsIntroSection


class ProductsIntroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsIntroSection
        fields = [
            "id",
            "title",
            "description",
            "is_active",
            "order",
        ]