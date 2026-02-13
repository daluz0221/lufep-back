import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.views import View

from ....services.sections.home.hero import HeroService
from ....dtos.admin.home.hero.create_hero_dto import CreateHeroDTO
from ....dtos.admin.home.hero.update_hero_dto import UpdateHeroDTO
from ....exceptions.home.hero import HeroNotFound



@method_decorator(csrf_exempt, name="dispatch")
class HomeHeroAdminView(View):
    
    def post(self, request):
        website = request.context.get("website")
        payload = json.loads(request.body)
        dto_hero = CreateHeroDTO.from_dict(payload)
        
        hero = HeroService.create_hero(website, dto_hero)
        return JsonResponse(hero, status=201)
    
    def get(self, request):
        website = request.context.get("website")
        data = HeroService.get_for_admin(website)
        
        return JsonResponse(data, status=201)
    
@method_decorator(csrf_exempt, name="dispatch")
class HomeHeroAdminDetailView(View):
    
    
    def put(self, request, id):
        website = request.context.get("website")
        payload = json.loads(request.body)
        hero_id = id
        update_hero_dto = UpdateHeroDTO.from_dict(payload)
        
        try:
            updated_hero = HeroService.update_hero(website, hero_id, update_hero_dto)
            return JsonResponse(updated_hero, status=201)
        except HeroNotFound:
            return JsonResponse(
                {"error": "Hero not found"},
                status=404
            )
        
    def get(self, request, id):
        website = request.context.get("website")
        hero_id = id
        
        try:
            hero = HeroService.get_by_id(website=website, hero_id=hero_id)
            return JsonResponse(hero, status=201)
        except HeroNotFound:
            return JsonResponse(
                {"error": "Hero not found"},
                status=404
            )
        
        
        
    

