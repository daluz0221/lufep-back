
from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore

from apps.showcase.models.home import FinalCTASection
from core.views import AdminView

from ....services.sections.home.cta import CTAService

from ....serializers.home.cta import FinalCTASectionSerializer




class HomeCTAAdminView(AdminView):
    
    def post(self, request):
        website = request.context.get("website")
        payload = FinalCTASectionSerializer(data=request.data)
        
        if payload.is_valid():
            section = CTAService.create_section(website, payload.validated_data)
            return Response(FinalCTASectionSerializer(section).data, status=status.HTTP_201_CREATED)
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        website = request.context.get("website")
        data = CTAService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)
    

class HomeCTAAdminDetailView(AdminView):
    
    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = CTAService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
    
    def patch(self, request, id):
        website = request.context.get("website")
        payload = FinalCTASectionSerializer(data=request.data, partial=True)
        if payload.is_valid():
            section = CTAService.update_section(website, id, payload.validated_data)
            return Response(FinalCTASectionSerializer(section).data, status=status.HTTP_200_OK)
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        website = request.context.get("website")
        CTAService.delete_section(website, id)
        return Response(status=status.HTTP_204_NO_CONTENT)