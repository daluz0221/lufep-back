from django.http import JsonResponse  # type: ignore
from django.views import View  # type: ignore

from ..services.pages.contact_page_service import ContactPageService


class ContactView(View):

    def get(self, request):
        website = request.context.get("website")
        data = ContactPageService.get_data(website)
        return JsonResponse(data)
