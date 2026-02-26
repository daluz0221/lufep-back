
from django.http import JsonResponse # type: ignore
from django.views import View # type: ignore

from ..services.pages.about_page_service import AboutPageService

class AboutView(View):
    
    def get(self, request):
        website = request.context.get("website")
        data = AboutPageService.get_data(website)
        return JsonResponse(data)