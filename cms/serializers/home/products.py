from rest_framework import serializers  # type: ignore
from apps.showcase.models.home import ProductSection, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "short_description",
            "description",
            "image",
            "url_text",
            "url",
            "order",
        ]


class ProductSectionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductSection
        fields = [
            "id",
            "title",
            "subtitle",
            "url",
            "products",
            "is_active",
            "order",
        ]
