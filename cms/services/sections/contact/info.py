from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models.contact import ContactInfoSection, ContactScheduleField
from ....serializers.contact.info import ContactInfoSectionSerializer


class InfoService:

    @staticmethod
    def get(website):
        section = ContactInfoSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                "schedule_fields",
                queryset=ContactScheduleField.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        ).first()
        return ContactInfoSectionSerializer(section).data if section else None

    @staticmethod
    def get_for_admin(website):
        sections = ContactInfoSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "schedule_fields",
                queryset=ContactScheduleField.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return {
            "infoSections": [
                ContactInfoSectionSerializer(section).data for section in sections
            ]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            section = ContactInfoSection.objects.prefetch_related(
                Prefetch(
                    "schedule_fields",
                    queryset=ContactScheduleField.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return ContactInfoSectionSerializer(section).data
        except ContactInfoSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            schedule_fields_data = data.pop("schedule_fields", [])

            if data.get("is_active"):
                ContactInfoSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            section = ContactInfoSection.objects.create(website=website, **data)
            for field_data in schedule_fields_data:
                ContactScheduleField.objects.create(
                    section=section, **field_data
                )
            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = ContactInfoSection.objects.get(
                website=website, id=id, is_deleted=False
            )

            with transaction.atomic():
                schedule_fields_data = data.pop("schedule_fields", None)

                if data.get("is_active"):
                    ContactInfoSection.objects.filter(
                        website=website, is_active=True, is_deleted=False
                    ).exclude(id=id).update(is_active=False)

                for attr, value in data.items():
                    setattr(section_to_update, attr, value)

                section_to_update.save()

                if schedule_fields_data is None:
                    section_to_update = ContactInfoSection.objects.prefetch_related(
                        Prefetch(
                            "schedule_fields",
                            queryset=ContactScheduleField.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_fields = {
                    f.pk: f
                    for f in section_to_update.schedule_fields.filter(
                        is_deleted=False
                    )
                }
                sent_ids = []

                for field_data in schedule_fields_data:
                    field_id = field_data.get("id")
                    if field_id and field_id in existing_fields:
                        fld = existing_fields[field_id]
                        for attr, value in field_data.items():
                            if attr != "id":
                                setattr(fld, attr, value)
                        fld.save()
                        sent_ids.append(field_id)
                    else:
                        
                        new_fld = ContactScheduleField.objects.create(
                            section=section_to_update, **field_data
                        )
                        sent_ids.append(new_fld.pk)

                ContactScheduleField.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = ContactInfoSection.objects.prefetch_related(
                    Prefetch(
                        "schedule_fields",
                        queryset=ContactScheduleField.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update

        except ContactInfoSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = ContactInfoSection.objects.get(
                website=website, id=instance_id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except ContactInfoSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")
