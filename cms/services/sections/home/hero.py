from apps.showcase.models import HeroSection


class HeroService:
    
    @staticmethod
    def get(website):
        hero = HeroSection.objects.filter(
            website=website,
            is_active=True
        ).first()
        
        return hero.to_dict() if hero else None
    
    @staticmethod
    def create_hero(website, payload):
        hero = HeroSection.objects.create(
            website=website,
            headline=payload.headline,
            highlight_word=payload.highlight_word if payload.highlight_word else '',
            subheadline=payload.subheadline,
            imageUrl=payload.imageUrl if payload.imageUrl else '',
            imageAlt=payload.imageAlt if payload.imageAlt else '',
            textCta=payload.textCta,
            urlCta=payload.urlCta
        )
        
        
        return hero.to_dict() if hero else None