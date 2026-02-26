from apps.showcase.models.about import AboutTeamSection
from ....serializers.about.team import AboutTeamSectionSerializer


class TeamService:
    
    @staticmethod
    def get(website):
        section = AboutTeamSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).first()
        return AboutTeamSectionSerializer(section).data if section else None