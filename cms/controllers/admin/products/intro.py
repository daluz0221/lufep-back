from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from core.views import AdminView
from ....serializers.products.intro import ProductsIntroSectionSerializer
from ....services.sections.products.intro import IntroService


class ProductsIntroAdminView(AdminView):

    def post(self, request):
        website = request.context.get("website")
        payload = ProductsIntroSectionSerializer(data=request.data)

        if payload.is_valid():
            section = IntroService.create(website, payload.validated_data)
            return Response(
                ProductsIntroSectionSerializer(section).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = IntroService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class ProductsIntroAdminDetailView(AdminView):

    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = IntroService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ProductsIntroSection not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request, id):
        website = request.context.get("website")
        payload = ProductsIntroSectionSerializer(data=request.data, partial=True)
        if payload.is_valid():
            try:
                updated_section = IntroService.update(
                    website, id, payload.validated_data
                )
                return Response(
                    ProductsIntroSectionSerializer(updated_section).data,
                    status=status.HTTP_200_OK,
                )
            except Exception:
                return Response(
                    {"error": "ProductsIntroSection not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        website = request.context.get("website")
        try:
            IntroService.delete(website, id)
        except Exception:
            return Response(
                {"error": "ProductsIntroSection not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response({}, status=status.HTTP_200_OK)
