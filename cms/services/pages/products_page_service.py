from ..sections.products.intro import IntroService
from ..sections.products.products import ProductsItemService

class ProductsPageService:
    
    @staticmethod
    def get_data(website):
        return {
            "intro": IntroService.get(website),
            "products": ProductsItemService.get(website),
        }