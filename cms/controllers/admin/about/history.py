from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from ....serializers.about.history import AboutHistorySectionSerializer
from ....services.sections.about.history import HistoryService


class AboutHistoryAdminView(APIView):

    def post(self, request):
        website = request.context.get("website")
        payload = AboutHistorySectionSerializer(data=request.data)

        if payload.is_valid():
            section = HistoryService.create(website, payload.validated_data)
            return Response(
                AboutHistorySectionSerializer(section).data,
                status=status.HTTP_201_CREATED
            )

        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = HistoryService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class AboutHistoryAdminDetailView(APIView):

    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = HistoryService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "AboutHistorySection not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, id):
        website = request.context.get("website")
        data = AboutHistorySectionSerializer(data=request.data, partial=True)
        if data.is_valid():
            try:
                updated_section = HistoryService.update(website, id, data.validated_data)
                return Response(
                    AboutHistorySectionSerializer(updated_section).data,
                    status=status.HTTP_200_OK
                )
            except Exception:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        website = request.context.get("website")
        try:
            HistoryService.delete(website, id)
        except Exception:
            return Response(
                {"error": "AboutHistorySection not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({}, status=status.HTTP_200_OK)
