from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models.about import AboutVisionSection, AboutVisionItem
from ....serializers.about.vision import AboutVisionSectionSerializer



class VisionService:
    
    @staticmethod
    def get(website):
        section = AboutVisionSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                "vision_items",
                queryset=AboutVisionItem.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        ).first()
        return AboutVisionSectionSerializer(section).data if section else None

    @staticmethod
    def get_for_admin(website):
        sections = AboutVisionSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "vision_items",
                queryset=AboutVisionItem.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return { "visionSections": [AboutVisionSectionSerializer(section).data for section in sections] }
    
    
    @staticmethod
    def get_by_id(website, id):
        try:
            section = AboutVisionSection.objects.prefetch_related(
                Prefetch(
                    "vision_items",
                    queryset=AboutVisionItem.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return AboutVisionSectionSerializer(section).data
        except AboutVisionSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
    
    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            vision_items_data = data.pop("vision_items", [])

            if data.get("is_active"):
                AboutVisionSection.objects.filter(website=website, is_active=True, is_deleted=False).update(is_active=False)
                
            section = AboutVisionSection.objects.create(website=website, **data)
            for vision_item_data in vision_items_data:
                AboutVisionItem.objects.create(section=section, **vision_item_data)
            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = AboutVisionSection.objects.get(website=website, id=id, is_deleted=False)
            
            with transaction.atomic():
                
                vision_items_data = data.pop("vision_items", None)
                
                if data.get("is_active"):
                    AboutVisionSection.objects.filter(website=website, is_active=True, is_deleted=False).exclude(id=id).update(is_active=False)
                
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)
                    
                section_to_update.save()
                
                if vision_items_data is None:
                    section_to_update = AboutVisionSection.objects.prefetch_related(
                        Prefetch(
                            "vision_items",
                            queryset=AboutVisionItem.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_vision_items = {vision_item.pk: vision_item for vision_item in section_to_update.vision_items.filter(is_deleted=False)}
                sent_ids = []
                
                for vision_item_data in vision_items_data:
                    vision_item_id = vision_item_data.get("id")
                    if vision_item_id and vision_item_id in existing_vision_items:
                        #UPDATE
                        vision_item = existing_vision_items[vision_item_id]
                        for attr, value in vision_item_data.items():
                            setattr(vision_item, attr, value)
                            vision_item.save()
                            sent_ids.append(vision_item_id)
                    else:
                        #CREATE
                        new_vision_item = AboutVisionItem.objects.create(section=section_to_update, **vision_item_data)
                        sent_ids.append(new_vision_item.pk)
                
                AboutVisionItem.objects.filter(section=section_to_update).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = AboutVisionSection.objects.prefetch_related(
                    Prefetch(
                        "vision_items",
                        queryset=AboutVisionItem.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update

        except AboutVisionSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
        
    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = AboutVisionSection.objects.get(website=website, id=instance_id, is_deleted=False)
            section.is_deleted = True
            section.save()
        except AboutVisionSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")