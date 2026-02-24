from apps.showcase.models import FinalCTASection



class CTAService:
    
    
    
    @staticmethod
    def get(website):
        
        section = FinalCTASection.objects.filter(website=website, is_active=True, is_deleted=False).first()
        
        
        return section.to_dict() if section else None