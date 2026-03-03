from rest_framework import serializers #type: ignore
from apps.showcase.models.home import HowItWorksSection, HowItWorksStep


class HowItWorksStepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = HowItWorksStep
        fields = [
            "id",
            "title",
            "description",
            "order",
        ]


class HowItWorksSectionSerializer(serializers.ModelSerializer):
    steps = HowItWorksStepSerializer(many=True)

    class Meta:
        model = HowItWorksSection
        fields = [
            "id",
            "title",
            "steps",
            "is_active",
            "order",
        ]