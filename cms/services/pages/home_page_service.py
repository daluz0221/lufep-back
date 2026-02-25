
from ..sections.home import HeroService, BenefitsService, ProductSectionService, StepsService, AboutService, TestimonialsService, CTAService


class HomePageService:

    @staticmethod
    def get_data(website):
        return {
            "hero": HeroService.get(website),
            "benefits": BenefitsService.get(website),
            "products": ProductSectionService.get(website),
            "steps": StepsService.get(website),
            "about": AboutService.get(website),
            "testimonials": TestimonialsService.get(website),
            "CTA": CTAService.get(website)
        }