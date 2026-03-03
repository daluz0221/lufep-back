from django.db import transaction  # type: ignore
from apps.showcase.models.products import ProductsIntroSection
from ....serializers.products.intro import ProductsIntroSectionSerializer


class IntroService:

    @staticmethod
    def get(website):
        section = ProductsIntroSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).first()
        return ProductsIntroSectionSerializer(section).data if section else None

    @staticmethod
    def get_for_admin(website):
        sections = ProductsIntroSection.objects.filter(
            website=website, is_deleted=False
        )
        return {
            "introSections": [
                ProductsIntroSectionSerializer(section).data for section in sections
            ]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            section = ProductsIntroSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            return ProductsIntroSectionSerializer(section).data
        except ProductsIntroSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create(website, data):
        with transaction.atomic():
            if data.get("is_active"):
                ProductsIntroSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)
            return ProductsIntroSection.objects.create(website=website, **data)

    @staticmethod
    def update(website, id, data):
        try:
            section = ProductsIntroSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            with transaction.atomic():
                if data.get("is_active"):
                    ProductsIntroSection.objects.filter(
                        website=website, is_active=True, is_deleted=False
                    ).exclude(id=id).update(is_active=False)
                for attr, value in data.items():
                    setattr(section, attr, value)
                section.save()
                return section
        except ProductsIntroSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete(website, id):
        try:
            section = ProductsIntroSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except ProductsIntroSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
