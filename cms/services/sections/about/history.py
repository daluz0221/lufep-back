from django.db import transaction  # type: ignore
from apps.showcase.models.about import AboutHistorySection
from ....serializers.about.history import AboutHistorySectionSerializer


class HistoryService:

    @staticmethod
    def get(website):
        section = AboutHistorySection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).first()
        return AboutHistorySectionSerializer(section).data if section else None

    @staticmethod
    def get_for_admin(website):
        sections = AboutHistorySection.objects.filter(website=website, is_deleted=False)
        return {
            "historySections": [
                AboutHistorySectionSerializer(section).data for section in sections
            ]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            section = AboutHistorySection.objects.get(website=website, id=id, is_deleted=False)
            return AboutHistorySectionSerializer(section).data
        except AboutHistorySection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create(website, data):
        with transaction.atomic():
            if data.get("is_active"):
                AboutHistorySection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            return AboutHistorySection.objects.create(website=website, **data)

    @staticmethod
    def update(website, id, data):
        try:
            section = AboutHistorySection.objects.get(website=website, id=id, is_deleted=False)
            with transaction.atomic():
                if data.get("is_active"):
                    AboutHistorySection.objects.filter(
                        website=website, is_active=True, is_deleted=False
                    ).exclude(id=id).update(is_active=False)
                for attr, value in data.items():
                    setattr(section, attr, value)
                section.save()
                return section
        except AboutHistorySection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete(website, id):
        try:
            section = AboutHistorySection.objects.get(website=website, id=id, is_deleted=False)
            section.is_deleted = True
            section.save()
        except AboutHistorySection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")