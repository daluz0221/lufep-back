from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models import HowItWorksSection, HowItWorksStep
from ....serializers.home.how_it_works import HowItWorksSectionSerializer, HowItWorksStepSerializer



class StepsService:
    
    
    @staticmethod
    def get(website):
        section = (
            HowItWorksSection.objects.filter(
                website=website,
                is_active=True,
                is_deleted=False
            )
            .prefetch_related(
                Prefetch(
                    "steps",
                    queryset=HowItWorksStep.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            )
            .first()
        )
        return section.to_dict() if section else None

    @staticmethod
    def get_for_admin(website):
        sections = HowItWorksSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "steps",
                queryset=HowItWorksStep.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return { "howItWorksSections": [section.to_dict() for section in sections] }
    
    @staticmethod
    def get_by_id(website, id):
        try:
            section = HowItWorksSection.objects.prefetch_related(
                Prefetch(
                    "steps",
                    queryset=HowItWorksStep.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return HowItWorksSectionSerializer(section).data
        except HowItWorksSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
    
    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            steps_data = data.pop("steps", [])
            
            if data.get("is_active"):
                HowItWorksSection.objects.filter(website=website, is_active=True, is_deleted=False).update(is_active=False)
                
            section = HowItWorksSection.objects.create(website=website, **data)
            
            for step_data in steps_data:    
                HowItWorksStep.objects.create(
                    section=section,
                    **step_data
                )
                
            return section
        
        
    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = HowItWorksSection.objects.get(website=website, id=id, is_deleted=False)
            with transaction.atomic():
                steps_data = data.pop("steps", None)
                if data.get("is_active"):
                    HowItWorksSection.objects.filter(website=website, is_active=True, is_deleted=False).exclude(id=id).update(is_active=False)
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)
                section_to_update.save()
                if steps_data is None:
                    section_to_update = HowItWorksSection.objects.prefetch_related(
                        Prefetch(
                            "steps",
                            queryset=HowItWorksStep.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_steps = {step.pk: step for step in section_to_update.steps.filter(is_deleted=False)}
                sent_ids = []
                for step_data in steps_data:
                    step_id = step_data.get("id")
                    if step_id and step_id in existing_steps:
                        step = existing_steps[step_id]
                        for attr, value in step_data.items():
                            setattr(step, attr, value)
                        step.save()
                        sent_ids.append(step_id)
                    else:
                        #CREATE
                        new_step: HowItWorksStep = HowItWorksStep.objects.create(
                            section=section_to_update,
                            **step_data
                        )
                        sent_ids.append(new_step.pk)
                
                # Soft-delete: marcar como eliminados los que el front ya no envía
                HowItWorksStep.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = HowItWorksSection.objects.prefetch_related(
                    Prefetch(
                        "steps",
                        queryset=HowItWorksStep.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update
        except HowItWorksSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
        
    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = HowItWorksSection.objects.get(website=website, id=instance_id, is_deleted=False)
            section.is_deleted = True
            section.save()
        except HowItWorksSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")