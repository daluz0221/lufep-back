from apps.showcase.models import HowItWorksSection



class StepsService:
    
    
    @staticmethod
    def get(website):
        section = (
            HowItWorksSection.objects.filter(
                website=website,
                is_active=True
            )
            .prefetch_related("steps")
            .first()
        )
        
        return section.to_dict() if section else None