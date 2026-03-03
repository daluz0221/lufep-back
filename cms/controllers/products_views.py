from django.http import JsonResponse # type: ignore
from django.views import View # type: ignore

from ..services.pages.products_page_service import ProductsPageService



class ProductsView(View):
    
    def get(self, request):
        website = request.context.get("website")
        data = ProductsPageService.get_data(website)
        return JsonResponse(data)