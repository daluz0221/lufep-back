from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models.about import AboutDifferentiatorsSection, AboutDifferentiator
from ....serializers.about.diferenciators import AboutDifferentiatorsSectionSerializer


class DiferenciatorService:

    @staticmethod
    def get(website):
        section = AboutDifferentiatorsSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                "differentiators",
                queryset=AboutDifferentiator.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        ).first()
        return AboutDifferentiatorsSectionSerializer(section).data if section else None

    @staticmethod
    def get_for_admin(website):
        sections = AboutDifferentiatorsSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "differentiators",
                queryset=AboutDifferentiator.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return {
            "differentiatorSections": [
                AboutDifferentiatorsSectionSerializer(section).data for section in sections
            ]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            section = AboutDifferentiatorsSection.objects.prefetch_related(
                Prefetch(
                    "differentiators",
                    queryset=AboutDifferentiator.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return AboutDifferentiatorsSectionSerializer(section).data
        except AboutDifferentiatorsSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            differentiators_data = data.pop("differentiators", [])

            if data.get("is_active"):
                AboutDifferentiatorsSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            section = AboutDifferentiatorsSection.objects.create(website=website, **data)
            for differentiator_data in differentiators_data:
                AboutDifferentiator.objects.create(section=section, **differentiator_data)
            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = AboutDifferentiatorsSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            
            with transaction.atomic():
                differentiators_data = data.pop("differentiators", None)

                if data.get("is_active"):
                    AboutDifferentiatorsSection.objects.filter(
                        website=website, is_active=True, is_deleted=False
                    ).exclude(id=id).update(is_active=False)

                for attr, value in data.items():
                    setattr(section_to_update, attr, value)

                section_to_update.save()

                if differentiators_data is None:
                    section_to_update = AboutDifferentiatorsSection.objects.prefetch_related(
                        Prefetch(
                            "differentiators",
                            queryset=AboutDifferentiator.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_differentiators = {
                    d.id: d
                    for d in section_to_update.differentiators.filter(is_deleted=False)
                }
                sent_ids = []
               
                for differentiator_data in differentiators_data:
                    differentiator_id = differentiator_data.get("id")
                    if differentiator_id and differentiator_id in existing_differentiators:
                        diff = existing_differentiators[differentiator_id]
                        for attr, value in differentiator_data.items():
                            setattr(diff, attr, value)
                        diff.save()
                        sent_ids.append(differentiator_id)
                    else:
                        #CREATE
                        
                        new_diff = AboutDifferentiator.objects.create(
                            section=section_to_update, **differentiator_data
                        )
                        sent_ids.append(new_diff.pk)
      
                AboutDifferentiator.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = AboutDifferentiatorsSection.objects.prefetch_related(
                    Prefetch(
                        "differentiators",
                        queryset=AboutDifferentiator.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update

        except AboutDifferentiatorsSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = AboutDifferentiatorsSection.objects.get(
                website=website, id=instance_id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except AboutDifferentiatorsSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")