from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from core.views import AdminView
from ....services.sections.contact.form import FormService
from ....serializers.contact.form import ContactFormSectionSerializer


class ContactFormAdminView(AdminView):

    def post(self, request):
        website = request.context.get("website")
        payload = ContactFormSectionSerializer(data=request.data)

        if payload.is_valid():
            section = FormService.create_section(
                website, payload.validated_data
            )
            return Response(
                ContactFormSectionSerializer(section).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = FormService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class ContactFormAdminDetailView(AdminView):

    def get(self, request, id):
        website = request.context.get("website")
        try:
            section = FormService.get_by_id(website, id)
            return Response(section, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ContactFormSection not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request, id):
        website = request.context.get("website")
        serializer = ContactFormSectionSerializer(
            data=request.data, partial=True
        )

        if serializer.is_valid():
            try:
                section = FormService.update_section(
                    website, id, serializer.validated_data
                )
                return Response(
                    ContactFormSectionSerializer(section).data,
                    status=status.HTTP_200_OK,
                )
            except Exception:
                return Response(
                    {"error": "ContactFormSection not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        website = request.context.get("website")

        try:
            FormService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "ContactFormSection not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
