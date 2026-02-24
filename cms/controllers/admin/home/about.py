from rest_framework import status
from rest_framework.response import Response

from core.views import AdminView

from ....services.sections.home.about import AboutService
from ....serializers.home.about import AboutSectionSerializer


class HomeAboutAdminView(AdminView):
    def post(self, request):
        website = request.context.get("website")
        payload = AboutSectionSerializer(data=request.data)

        if payload.is_valid():
            section = AboutService.create_section(website, payload.validated_data)
            return Response(
                AboutSectionSerializer(section).data,
                status=status.HTTP_201_CREATED
            )
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = AboutService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class HomeAboutAdminDetailView(AdminView):
    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = AboutService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        website = request.context.get("website")
        serializer = AboutSectionSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            try:
                update_section = AboutService.update_section(
                    website, id, serializer.validated_data
                )
                return Response(
                    AboutSectionSerializer(update_section).data,
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
            AboutService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "AboutSection not found"},
                status=status.HTTP_404_NOT_FOUND
            )
