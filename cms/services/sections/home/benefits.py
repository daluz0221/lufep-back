from apps.showcase.models import BenefitsSection



class BenefitsService:
    
    @staticmethod
    def get(website):
        section = (
            BenefitsSection.objects.filter(
                website=website,
                is_active=True
            )
            .prefetch_related("benefits")
            .first()
        )
        
        return section.to_dict() if section else None