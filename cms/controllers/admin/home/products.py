from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from core.views import AdminView

from ....services.sections.home.products import ProductSectionService
from ....serializers.home.products import ProductSectionSerializer


class HomeProductsAdminView(AdminView):

    def post(self, request):
        website = request.context.get("website")
        payload = ProductSectionSerializer(data=request.data)

        if payload.is_valid():
            section = ProductSectionService.create_section(
                website, payload.validated_data
            )
            return Response(
                ProductSectionSerializer(section).data,
                status=status.HTTP_201_CREATED
            )
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = ProductSectionService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class HomeProductsAdminDetailView(AdminView):

    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = ProductSectionService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        website = request.context.get("website")
        serializer = ProductSectionSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            try:
                update_section = ProductSectionService.update_section(
                    website, id, serializer.validated_data
                )
                return Response(
                    ProductSectionSerializer(update_section).data,
                    status=status.HTTP_200_OK
                )
            except Exception:
                return Response(
                    serializer.errors,
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        website = request.context.get("website")
        try:
            ProductSectionService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ProductSection not found"},
                status=status.HTTP_404_NOT_FOUND
            )
