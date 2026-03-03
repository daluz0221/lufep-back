from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore

from apps.showcase.models import ProductSection, Product

from ....serializers.home.products import ProductSectionSerializer


class ProductSectionService:

    @staticmethod
    def get(website):
        section = (
            ProductSection.objects.filter(
                website=website,
                is_active=True,
                is_deleted=False
            )
            .prefetch_related(
                Prefetch(
                    "products",
                    queryset=Product.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            )
            .first()
        )
        return section.to_dict() if section else None

    @staticmethod
    def get_for_admin(website):
        sections = ProductSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return {"productSections": [section.to_dict() for section in sections]}

    @staticmethod
    def get_by_id(website, id):
        try:
            section = ProductSection.objects.prefetch_related(
                Prefetch(
                    "products",
                    queryset=Product.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return ProductSectionSerializer(section).data
        except ProductSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            products_data = data.pop("products", [])

            if data.get("is_active"):
                ProductSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            section = ProductSection.objects.create(website=website, **data)

            for product_data in products_data:
                Product.objects.create(section=section, **product_data)

            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = ProductSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            with transaction.atomic():
                products_data = data.pop("products", None)
                if data.get("is_active"):
                    ProductSection.objects.filter(
                        website=website,
                        is_active=True,
                        is_deleted=False
                    ).exclude(id=id).update(is_active=False)
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)
                section_to_update.save()
                if products_data is None:
                    section_to_update = ProductSection.objects.prefetch_related(
                        Prefetch(
                            "products",
                            queryset=Product.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_products = {
                    p.pk: p
                    for p in section_to_update.products.filter(is_deleted=False)
                }
                sent_ids = []
                for product_data in products_data:
                    product_id = product_data.get("id")
                    if product_id and product_id in existing_products:
                        product = existing_products[product_id]
                        for attr, value in product_data.items():
                            setattr(product, attr, value)
                        product.save()
                        sent_ids.append(product_id)
                    else:
                        new_product = Product.objects.create(
                            section=section_to_update, **product_data
                        )
                        sent_ids.append(new_product.pk)

                Product.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = ProductSection.objects.prefetch_related(
                    Prefetch(
                        "products",
                        queryset=Product.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update
        except ProductSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = ProductSection.objects.get(
                website=website, id=instance_id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except ProductSection.DoesNotExist:
            raise Exception("Section not found")
