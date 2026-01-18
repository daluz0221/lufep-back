from apps.showcase.models import ServiceSection




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