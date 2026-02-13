



from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from apps.showcase.models.home import HeroSection
from core.views import AdminView

from ....services.sections.home.hero import HeroService
from ....exceptions.home.hero import HeroNotFound

from ....serializers.home.hero import HeroSectionSerializer


class HomeHeroAdminView(AdminView):

    
    def post(self, request):
        website = request.context.get("website")
        payload = HeroSectionSerializer(data=request.data)
        
        if payload.is_valid():
            hero = HeroService.create_hero(website, payload.validated_data)

            return Response(HeroSectionSerializer(hero).data, status=status.HTTP_201_CREATED)
        
        
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        website = request.context.get("website")
        data = HeroService.get_for_admin(website)
        
        return JsonResponse(data, status=201)
    

class HomeHeroAdminDetailView(AdminView):
    

    
    def patch(self, request, id):
        website = request.context.get("website")
        payload = HeroSectionSerializer(data=request.data, partial=True)
        hero_id = id
       
        if payload.is_valid():
            try:
                updated_hero = HeroService.update_hero(website, hero_id, payload.validated_data)
                return Response(HeroSectionSerializer(updated_hero).data, status=status.HTTP_302_FOUND)
            except HeroNotFound:
                return Response(payload.errors, status=status.HTTP_404_NOT_FOUND)
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, id):
        website = request.context.get("website")
        hero_id = id
        
        
        try:
            hero = HeroService.get_by_id(website=website, hero_id=hero_id)
            return Response(hero, status=status.HTTP_302_FOUND)
        except HeroNotFound:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        
    def delete(self, request, id):
        website = request.context.get("website")
        try:
            hero = HeroSection.objects.get(pk=id, website=website)
        except HeroSection.DoesNotExist:
            hero = None
            
        if not hero:
            return Response(
                {"error": "HeroSection no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        HeroSection.delete(hero)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
        

