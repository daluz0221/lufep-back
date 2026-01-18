from apps.showcase.models import TestimonialSection



class TestimonialsService:
    
    
    
    @staticmethod
    def get(website):
        section = (
            TestimonialSection.objects.filter(
                website=website,
                is_active=True
            ).prefetch_related("testimonials")
            .first()
        )
        
        
        return section.to_dict() if section else None