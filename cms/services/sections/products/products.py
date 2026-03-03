from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models.products import ProductsItem, ProductsItemInclude
from ....serializers.products.product import ProductsItemSerializer


class ProductsItemService:

    @staticmethod
    def get(website):
        items = ProductsItem.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                "includes",
                queryset=ProductsItemInclude.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        ).order_by("order")
        return [ProductsItemSerializer(item).data for item in items]

    @staticmethod
    def get_for_admin(website):
        items = ProductsItem.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "includes",
                queryset=ProductsItemInclude.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        ).order_by("order")
        return {
            "productItems": [ProductsItemSerializer(item).data for item in items]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            item = ProductsItem.objects.prefetch_related(
                Prefetch(
                    "includes",
                    queryset=ProductsItemInclude.objects.filter(is_deleted=False),
                )
            ).get(website=website, id=id, is_deleted=False)
            return ProductsItemSerializer(item).data
        except ProductsItem.DoesNotExist:
            raise Exception(f"Producto with id {id} not found")

    @staticmethod
    def create(website, data):
        with transaction.atomic():
            includes_data = data.pop("includes", [])

            if data.get("is_active"):
                ProductsItem.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            item = ProductsItem.objects.create(website=website, **data)
            for include_data in includes_data:
                ProductsItemInclude.objects.create(product=item, **include_data)
            return item

    @staticmethod
    def update(website, id, data):
        try:
            item_to_update = ProductsItem.objects.get(
                website=website, id=id, is_deleted=False
            )

            with transaction.atomic():
                includes_data = data.pop("includes", None)

                if data.get("is_active"):
                    ProductsItem.objects.filter(
                        website=website, is_active=True, is_deleted=False
                    ).exclude(id=id).update(is_active=False)

                for attr, value in data.items():
                    setattr(item_to_update, attr, value)

                item_to_update.save()

                if includes_data is None:
                    item_to_update = ProductsItem.objects.prefetch_related(
                        Prefetch(
                            "includes",
                            queryset=ProductsItemInclude.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=item_to_update.pk)
                    return item_to_update

                existing_includes = {
                    i.pk: i
                    for i in item_to_update.includes.filter(is_deleted=False)
                }
                sent_ids = []

                for include_data in includes_data:
                    include_id = include_data.get("id")
                    if include_id and include_id in existing_includes:
                        inc = existing_includes[include_id]
                        for attr, value in include_data.items():
                            if attr != "id":
                                setattr(inc, attr, value)
                        inc.save()
                        sent_ids.append(include_id)
                    else:
                        new_include_data = ProductsItemInclude.objects.create(
                            product=item_to_update, **include_data
                        )
                        sent_ids.append(new_include_data.pk)

                ProductsItemInclude.objects.filter(
                    product=item_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                item_to_update = ProductsItem.objects.prefetch_related(
                    Prefetch(
                        "includes",
                        queryset=ProductsItemInclude.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=item_to_update.pk)
                return item_to_update

        except ProductsItem.DoesNotExist:
            raise Exception(f"Producto with id {id} not found")

    @staticmethod
    def delete(website, id):
        try:
            item = ProductsItem.objects.get(
                website=website, id=id, is_deleted=False
            )
            item.is_deleted = True
            item.save()
        except ProductsItem.DoesNotExist:
            raise Exception(f"Producto with id {id} not found")