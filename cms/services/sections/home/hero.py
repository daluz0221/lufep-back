from apps.showcase.models import HeroSection


class HeroService:
    
    @staticmethod
    def get(website):
        hero = HeroSection.objects.filter(
            website=website,
            is_active=True
        ).first()
        
        return hero.to_dict() if hero else None