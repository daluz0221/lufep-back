from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from core.views import AdminView
from ....services.sections.products.products import ProductsItemService
from ....serializers.products.product import ProductsItemSerializer


class ProductsItemsAdminView(AdminView):

    def post(self, request):
        website = request.context.get("website")
        payload = ProductsItemSerializer(data=request.data)

        if payload.is_valid():
            item = ProductsItemService.create(website, payload.validated_data)
            return Response(
                ProductsItemSerializer(item).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = ProductsItemService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class ProductsItemsAdminDetailView(AdminView):

    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = ProductsItemService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ProductsItem not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request, id):
        website = request.context.get("website")
        serializer = ProductsItemSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            try:
                item = ProductsItemService.update(
                    website, id, serializer.validated_data
                )
                return Response(
                    ProductsItemSerializer(item).data,
                    status=status.HTTP_200_OK,
                )
            except Exception:
                return Response(
                    {"error": "ProductsItem not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        website = request.context.get("website")

        try:
            ProductsItemService.delete(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ProductsItem not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
