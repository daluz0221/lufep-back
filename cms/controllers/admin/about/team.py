from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from core.views import AdminView
from ....services.sections.about.team import TeamService
from ....serializers.about.team import AboutTeamSectionSerializer


class AboutTeamAdminView(AdminView):

    def post(self, request):
        website = request.context.get("website")
        payload = AboutTeamSectionSerializer(data=request.data)

        if payload.is_valid():
            section = TeamService.create_section(website, payload.validated_data)
            return Response(
                AboutTeamSectionSerializer(section).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = TeamService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class AboutTeamAdminDetailView(AdminView):

    def get(self, request, id):
        website = request.context.get("website")
        try:
            section = TeamService.get_by_id(website, id)
            return Response(section, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        website = request.context.get("website")
        serializer = AboutTeamSectionSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            try:
                section = TeamService.update_section(
                    website, id, serializer.validated_data
                )
                return Response(
                    AboutTeamSectionSerializer(section).data,
                    status=status.HTTP_200_OK,
                )
            except Exception:
                return Response(
                    serializer.errors, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        website = request.context.get("website")

        try:
            TeamService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "AboutTeamSection not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
