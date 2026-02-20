from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from ....services.sections.home.services import ServiceSectionService
from ....serializers.home.services import SerivceSectionSerializer


class HomeServicesAdminView(APIView):
    
    
    def post(self, request):
        website = request.context.get("website")
        payload = SerivceSectionSerializer(data=request.data)
        
        if payload.is_valid():
            section = ServiceSectionService.create_section(website, payload.validated_data)
            
            return Response(SerivceSectionSerializer(section).data, status=status.HTTP_201_CREATED)
        
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)


