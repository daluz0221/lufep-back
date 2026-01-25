from django.http import JsonResponse
from django.views import View

from ..services.pages.home_page_service import HomePageService


class HomeView(View):
    
    
    def get(self, request):
        website = request.context.get("website")
        data = HomePageService.get_data(website)
        
        return JsonResponse(data)
    

        