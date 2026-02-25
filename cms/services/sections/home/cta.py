from django.db import transaction #type: ignore

from apps.showcase.models import FinalCTASection


from ....serializers.home.cta import FinalCTASectionSerializer



class CTAService:
    
    
    
    @staticmethod
    def get(website):
        
        section = FinalCTASection.objects.filter(website=website, is_active=True, is_deleted=False).first()
        
        
        return FinalCTASectionSerializer(section).data if section else None
    
    @staticmethod
    def get_for_admin(website):
        sections = FinalCTASection.objects.filter(website=website, is_deleted=False)
        return { "ctaSections": [FinalCTASectionSerializer(section).data for section in sections] }
    
    @staticmethod
    def get_by_id(website, id):
        try:
            section = FinalCTASection.objects.get(website=website, id=id, is_deleted=False)
            return FinalCTASectionSerializer(section).data
        except FinalCTASection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
        
    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            if data.get("is_active"):
                FinalCTASection.objects.filter(website=website, is_active=True, is_deleted=False).update(is_active=False)
                
            return FinalCTASection.objects.create(website=website, **data)
        
    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = FinalCTASection.objects.get(website=website, id=id, is_deleted=False)
            with transaction.atomic():  
                if data.get("is_active"):
                    FinalCTASection.objects.filter(website=website, is_active=True, is_deleted=False).exclude(id=id).update(is_active=False)
                    
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)
                    
                section_to_update.save()
                return section_to_update
        except FinalCTASection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
        
    @staticmethod
    def delete_section(website, id):
        try:
            section = FinalCTASection.objects.get(website=website, id=id, is_deleted=False)
            with transaction.atomic():
                section.is_deleted = True
                section.save()
                return section
        except FinalCTASection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")