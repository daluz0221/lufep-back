from django.db import transaction

from apps.showcase.models import ServiceSection, Service

from ....serializers.home.services import SerivceSectionSerializer

class ServiceSectionService:
    
    @staticmethod
    def get(website):
        section = (
            ServiceSection.objects.filter(
                website=website,
                is_active=True
            )
            .prefetch_related("servicios")
            .first()
        )
        
        return section.to_dict() if section else None
    
    
    
    
    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            
            services_data = data.pop("servicios", [])
            
            if data.get("is_active"):
                ServiceSection.objects.filter(website=website, is_active=True).update(is_active=False)
            
            section = ServiceSection.objects.create(website=website, **data)
            
            for service_data in services_data:
                Service.objects.create(
                    section=section,
                    **service_data
                )            
                
            return section