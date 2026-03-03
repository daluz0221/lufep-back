from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models.contact import ContactFormSection, ContactFormSubjectOption
from ....serializers.contact.form import ContactFormSectionSerializer


class FormService:

    @staticmethod
    def get(website):
        section = ContactFormSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                "subject_options",
                queryset=ContactFormSubjectOption.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        ).first()
        return ContactFormSectionSerializer(section).data if section else None

    @staticmethod
    def get_for_admin(website):
        sections = ContactFormSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "subject_options",
                queryset=ContactFormSubjectOption.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return {
            "formSections": [
                ContactFormSectionSerializer(section).data for section in sections
            ]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            section = ContactFormSection.objects.prefetch_related(
                Prefetch(
                    "subject_options",
                    queryset=ContactFormSubjectOption.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return ContactFormSectionSerializer(section).data
        except ContactFormSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            subject_options_data = data.pop("subject_options", [])

            if data.get("is_active"):
                ContactFormSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            section = ContactFormSection.objects.create(website=website, **data)
            for option_data in subject_options_data:

                ContactFormSubjectOption.objects.create(
                    section=section, **option_data
                )
            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = ContactFormSection.objects.get(
                website=website, id=id, is_deleted=False
            )

            with transaction.atomic():
                subject_options_data = data.pop("subject_options", None)

                if data.get("is_active"):
                    ContactFormSection.objects.filter(
                        website=website, is_active=True, is_deleted=False
                    ).exclude(id=id).update(is_active=False)

                for attr, value in data.items():
                    setattr(section_to_update, attr, value)

                section_to_update.save()

                if subject_options_data is None:
                    section_to_update = ContactFormSection.objects.prefetch_related(
                        Prefetch(
                            "subject_options",
                            queryset=ContactFormSubjectOption.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_options = {
                    o.pk: o
                    for o in section_to_update.subject_options.filter(
                        is_deleted=False
                    )
                }
                sent_ids = []

                for option_data in subject_options_data:
                    option_id = option_data.get("id")
                    if option_id and option_id in existing_options:
                        opt = existing_options[option_id]
                        for attr, value in option_data.items():
                            if attr != "id":
                                setattr(opt, attr, value)
                        opt.save()
                        sent_ids.append(option_id)
                    else:
                        
                        new_opt = ContactFormSubjectOption.objects.create(
                            section=section_to_update, **option_data
                        )
                        sent_ids.append(new_opt.pk)

                ContactFormSubjectOption.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = ContactFormSection.objects.prefetch_related(
                    Prefetch(
                        "subject_options",
                        queryset=ContactFormSubjectOption.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update

        except ContactFormSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = ContactFormSection.objects.get(
                website=website, id=instance_id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except ContactFormSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")
