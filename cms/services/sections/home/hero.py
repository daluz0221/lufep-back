
from django.db import transaction

from apps.showcase.models import HeroSection

from ....serializers.home.hero import HeroSectionSerializer
from ....exceptions.home.hero import HeroNotFound


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
            return HeroSectionSerializer(hero).data
        except HeroSection.DoesNotExist:
            raise HeroNotFound( f"Hero with ud {hero_id} not found")
        
     
    
    @staticmethod
    def create_hero(website, valid_payload):
        with transaction.atomic():
            if valid_payload.get("is_active"):
                HeroSection.objects.filter(website=website, is_active=True).update(is_active=False)
                
            return HeroSection.objects.create(website=website, **valid_payload)
        
        
    
    @staticmethod
    def update_hero(website, hero_id: int, valid_payload):
        try:
            hero_to_update = HeroSection.objects.get(
                website=website,
                id=hero_id
            )
            with transaction.atomic():
                if valid_payload.get('is_active'):
                    HeroSection.objects.filter(
                        website=website, 
                        is_active=True
                    ).exclude(pk=hero_to_update.pk).update(is_active=False)
            
            for attr, value in valid_payload.items():
                setattr(hero_to_update, attr, value)
            
            hero_to_update.save()
            return hero_to_update
        except HeroSection.DoesNotExist:
            raise HeroNotFound( f"Hero with ud {hero_id} not found")
        
        
    @staticmethod
    def delete_hero(website, hero_instance):
        with transaction.atomic():
            was_active = hero_instance.is_active
            
            hero_instance.delete()
            
            if was_active:
                next_hero = HeroSection.objects.filter(website=website).order_by('-id').first()
                if next_hero:
                    next_hero.is_active = True
                    next_hero.save()
            