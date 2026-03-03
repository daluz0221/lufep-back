from rest_framework import serializers  # type: ignore
from apps.showcase.models.products import ProductsItem, ProductsItemInclude


class ProductsItemIncludeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = ProductsItemInclude
        fields = ["id", "text", "order"]


class ProductsItemSerializer(serializers.ModelSerializer):
    includes = ProductsItemIncludeSerializer(many=True)

    class Meta:
        model = ProductsItem
        fields = [
            "id",
            "title",
            "description",
            "imageUrl",
            "imageAlt",
            "forWho",
            "includes",
            "is_active",
            "order",
        ]