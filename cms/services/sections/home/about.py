from apps.showcase.models import AboutSection



class AboutService:
    
    
    @staticmethod
    def get(website):
        section = (
            AboutSection.objects.filter(
                website=website,
                is_active=True
            )
            .first()
        )
        
        return section.to_dict() if section else None