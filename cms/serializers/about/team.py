from rest_framework import serializers # type: ignore
from apps.showcase.models.about import AboutTeamSection, AboutTeamMember


class AboutTeamMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = AboutTeamMember
        fields = [
            "id",
            "name",
            "role",
            "image",
            "order",
        ]
        
class AboutTeamSectionSerializer(serializers.ModelSerializer):
    members = AboutTeamMemberSerializer(many=True)
    class Meta:
        model = AboutTeamSection
        fields = [
            "id",
            "title",
            "members",
            "is_active",
            "order",
        ]