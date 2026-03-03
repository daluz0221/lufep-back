from rest_framework import serializers  # type: ignore
from apps.showcase.models.contact import ContactInfoSection, ContactScheduleField


class ContactScheduleFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = ContactScheduleField
        fields = ["id", "title_time", "title_period", "extra_time", "order"]


class ContactInfoSectionSerializer(serializers.ModelSerializer):
    schedule_fields = ContactScheduleFieldSerializer(many=True)

    class Meta:
        model = ContactInfoSection
        fields = [
            "id",
            "phone",
            "phone_text",
            "email",
            "email_text",
            "map_text",
            "schedule_title",
            "extra_text",
            "schedule_fields",
            "is_active",
            "order",
        ]
