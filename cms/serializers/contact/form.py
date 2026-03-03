from rest_framework import serializers  # type: ignore
from apps.showcase.models.contact import ContactFormSection, ContactFormSubjectOption


class ContactFormSubjectOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = ContactFormSubjectOption
        fields = ["id", "text", "order"]


class ContactFormSectionSerializer(serializers.ModelSerializer):
    subject_options = ContactFormSubjectOptionSerializer(many=True)

    class Meta:
        model = ContactFormSection
        fields = [
            "id",
            "title",
            "description",
            "form_fields",
            "subject_options",
            "is_active",
            "order",
        ]
