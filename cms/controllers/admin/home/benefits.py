from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


from core.views import AdminView

from ....services.sections.home.benefits import BenefitsService
from ....serializers.home.benefits import BenefitsSectionSerializer


class HomeBenefitsAdminView(AdminView):
    
    
    def post(self, request):
        website = request.context.get("website")
        payload = BenefitsSectionSerializer(data=request.data)
        
        if payload.is_valid():
            section = BenefitsService.create(website, payload.validated_data)
            
            return Response(BenefitsSectionSerializer(section).data, status=status.HTTP_201_CREATED)
        
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
    def get(self, request):
        website = request.context.get("website")
        data = BenefitsService.get_for_admin(website)
        
        return JsonResponse(data, status=status.HTTP_200_OK)
    
    
    
class HomeBenefitsAdminDetailView(AdminView):
    
    
    def get(self, request, id):
        website = request.context.get("website")
        
        try:
            section = BenefitsService.get_by_id(website, id)
            return Response(section, status=status.HTTP_302_FOUND)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        
    def patch(self, request, id):
        website = request.context.get("website")
        serializer = BenefitsSectionSerializer(data=request.data, partial=True)
        
        if serializer.is_valid():
            try:
                update_section = BenefitsService.update_section(website, id, serializer.validated_data)
                return Response(BenefitsSectionSerializer(update_section).data, status=status.HTTP_302_FOUND)
            except Exception:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, id):
        website = request.context.get("website")
        
        try:
            BenefitsService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "BenefitSection not found"}, status=status.HTTP_404_NOT_FOUND)

            