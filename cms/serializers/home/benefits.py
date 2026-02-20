from rest_framework import serializers
from apps.showcase.models.home import BenefitsSection, Benefit


class BenefitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Benefit
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "order"
        ] 


class BenefitsSectionSerializer(serializers.ModelSerializer):
    
    benefits = BenefitSerializer(many=True)
    
    class Meta:
        model = BenefitsSection
        fields = [
            "id",
            "title",
            "subtitle",
            "benefits",
            "is_active",
            "order"
        ]
        
   