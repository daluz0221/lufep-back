import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.views import View

from ....services.sections.home.hero import HeroService



@method_decorator(csrf_exempt, name="dispatch")
class HomeHeroAdminView(View):
    
    def post(self, request):
        website = request.context.get("website")
        payload = json.loads(request.body)
        
        hero = HeroService.create_hero(website, payload)
        return JsonResponse(hero, status=201)