from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from core.views import AdminView
from ....services.sections.about.vision import VisionService
from ....serializers.about.vision import AboutVisionSectionSerializer






class AboutVisionAdminView(AdminView):
    
    
    def post(self, request):
        
        website = request.context.get("website")
        payload = AboutVisionSectionSerializer(data=request.data)
        
        if payload.is_valid():
            section = VisionService.create_section(website, payload.validated_data)
            return Response(AboutVisionSectionSerializer(section).data, status=status.HTTP_201_CREATED)
        
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        website = request.context.get("website")
        data = VisionService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)
    
    
class AboutVisionAdminDetailView(AdminView):
    
    def get(self, request, id):
        website = request.context.get("website")
        try:
            section = VisionService.get_by_id(website, id)
            return Response(section, status=status.HTTP_302_FOUND)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, id):   
        website = request.context.get("website")
        serializer = AboutVisionSectionSerializer(data=request.data, partial=True)
        
        if serializer.is_valid():
            
            try:
                section = VisionService.update_section(website, id, serializer.validated_data)
                return Response(AboutVisionSectionSerializer(section).data, status=status.HTTP_302_FOUND)
            except Exception:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        website = request.context.get("website")
        
        try:
            VisionService.delete_section(website, id)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "AboutVisionSection not found"}, status=status.HTTP_404_NOT_FOUND)