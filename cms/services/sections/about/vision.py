from apps.showcase.models.about import AboutVisionSection
from ....serializers.about.vision import AboutVisionSectionSerializer



class VisionService:
    
    @staticmethod
    def get(website):
        section = AboutVisionSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).first()
        return AboutVisionSectionSerializer(section).data if section else None
    
    