

from apps.showcase.models import HeroSection

from ....exceptions.home.hero import HeroNotFound
from ....dtos.admin.home.hero.update_hero_dto import UpdateHeroDTO


class HeroService:
    
    @staticmethod
    def get(website):
        hero = HeroSection.objects.filter(
            website=website,
            is_active=True
        ).first()
        
        return hero.to_dict() if hero else None
    
    @staticmethod
    def get_for_admin(website):
        heros = HeroSection.objects.filter(
            website=website
        )
        
        return { "heros" : [hero.to_dict() for hero in heros if hero] }
    
    
    @staticmethod
    def get_by_id(website, hero_id):
        try:
            hero = HeroSection.objects.get(website=website, id=hero_id)
            return {"hero": hero.to_dict()} if hero else None
        except HeroSection.DoesNotExist:
            raise HeroNotFound( f"Hero with ud {hero_id} not found")
        
     
    
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
    
    @staticmethod
    def update_hero(website, hero_id: int, hero: UpdateHeroDTO):
        try:
            hero_to_update = HeroSection.objects.get(
                website=website,
                id=hero_id
            )
            
            for field, value in vars(hero).items():
                if value is not None:
                    setattr(hero_to_update, field, value)
            
            hero_to_update.save()
            return {"ok": "Hero actualizado con éxito"}
        except HeroSection.DoesNotExist:
            raise HeroNotFound( f"Hero with ud {hero_id} not found")
        