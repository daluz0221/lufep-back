from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from core.views import AdminView
from ....services.sections.home.steps import StepsService
from ....serializers.home.how_it_works import HowItWorksSectionSerializer, HowItWorksStepSerializer



class HomeHowItWorksAdminView(AdminView):
    
    def post(self, request):
        website = request.context.get("website")
        payload = HowItWorksSectionSerializer(data=request.data)
        
        if payload.is_valid():
            section = StepsService.create_section(website, payload.validated_data)
            return Response(HowItWorksSectionSerializer(section).data, status=status.HTTP_201_CREATED)
         
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        website = request.context.get("website")
        data = StepsService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)
    
    
class HomeHowItWorksAdminDetailView(AdminView):
    
    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = StepsService.get_by_id(website, id)
            return Response(data, status=status.HTTP_302_FOUND)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    
    def patch(self, request, id):
        website = request.context.get("website")
        serializer = HowItWorksSectionSerializer(data=request.data, partial=True)
        
        if serializer.is_valid():
            try:
                update_section = StepsService.update_section(website, id, serializer.validated_data)
                return Response(HowItWorksSectionSerializer(update_section).data, status=status.HTTP_302_FOUND)
            except Exception:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        website = request.context.get("website")
        try:
            StepsService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "HowItWorksSection not found"}, status=status.HTTP_404_NOT_FOUND)