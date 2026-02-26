from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from ....serializers.about.intro import AboutIntroSectionSerializer
from ....services.sections.about.intro import IntroService



class AboutIntroAdminView(APIView):
    
    
    def post(self, request):
        website = request.context.get("website")
        payload = AboutIntroSectionSerializer(data=request.data)
        
        if payload.is_valid():
            section = IntroService.create(website, payload.validated_data)
            return Response(AboutIntroSectionSerializer(section).data, status=status.HTTP_201_CREATED)
        
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        website = request.context.get("website")
        data = IntroService.get_for_admin(website)
        return Response(data, status=status.HTTP_200_OK)
    
    
class AboutIntroAdminDetailView(APIView):
    
    def get(self, request, id):
        website = request.context.get("website")
        try:
            data = IntroService.get_by_id(website, id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "AboutIntroSection not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, id):
        website = request.context.get("website")
        data = AboutIntroSectionSerializer(data=request.data, partial=True)
        if data.is_valid():
            try:
                updated_section = IntroService.update(website, id, data.validated_data)
                return Response(AboutIntroSectionSerializer(updated_section).data, status=status.HTTP_200_OK)
            except Exception:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        website = request.context.get("website")
        try:
            IntroService.delete(website, id)
        except Exception:
            return Response(
                {"error": "AboutIntroSection not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({}, status=status.HTTP_200_OK)