from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore


from core.views import AdminView
from ....services.sections.home.testimonials import TestimonialsService
from ....serializers.home.testimonials import TestimonialSectionSerializer


class HomeTestimonialsAdminView(AdminView):
    def post(self, request):
        website = request.context.get("website")
        payload = TestimonialSectionSerializer(data=request.data)

        if payload.is_valid():
            section = TestimonialsService.create_section(
                website, payload.validated_data
            )
            return Response(
                TestimonialSectionSerializer(section).data,
                status=status.HTTP_201_CREATED
            )
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        website = request.context.get("website")
        data = TestimonialsService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)


class HomeTestimonialsAdminDetailView(AdminView):
    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = TestimonialsService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        website = request.context.get("website")
        serializer = TestimonialSectionSerializer(
            data=request.data, partial=True
        )

        if serializer.is_valid():
            try:
                update_section = TestimonialsService.update_section(
                    website, id, serializer.validated_data
                )
                return Response(
                    TestimonialSectionSerializer(update_section).data,
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
            TestimonialsService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "TestimonialSection not found"},
                status=status.HTTP_404_NOT_FOUND
            )
