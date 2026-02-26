from apps.showcase.models.about import AboutDifferentiatorsSection
from ....serializers.about.diferenciators import AboutDifferentiatorsSectionSerializer


class DiferenciatorService:
    
    @staticmethod
    def get(website):
        section = AboutDifferentiatorsSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).first()   
        return AboutDifferentiatorsSectionSerializer(section).data if section else None