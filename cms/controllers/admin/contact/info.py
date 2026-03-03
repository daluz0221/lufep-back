from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from core.views import AdminView
from ....services.sections.contact.info import InfoService
from ....serializers.contact.info import ContactInfoSectionSerializer


class ContactInfoAdminView(AdminView):

    def post(self, request):
        website = request.context.get("website")
        payload = ContactInfoSectionSerializer(data=request.data)

        if payload.is_valid():
            section = InfoService.create_section(
                website, payload.validated_data
            )
            return Response(
                ContactInfoSectionSerializer(section).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = InfoService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class ContactInfoAdminDetailView(AdminView):

    def get(self, request, id):
        website = request.context.get("website")
        try:
            section = InfoService.get_by_id(website, id)
            return Response(section, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ContactInfoSection not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request, id):
        website = request.context.get("website")
        serializer = ContactInfoSectionSerializer(
            data=request.data, partial=True
        )

        if serializer.is_valid():
            try:
                section = InfoService.update_section(
                    website, id, serializer.validated_data
                )
                return Response(
                    ContactInfoSectionSerializer(section).data,
                    status=status.HTTP_200_OK,
                )
            except Exception:
                return Response(
                    {"error": "ContactInfoSection not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        website = request.context.get("website")

        try:
            InfoService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ContactInfoSection not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
