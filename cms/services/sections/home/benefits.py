from django.db import transaction #type: ignore

from apps.showcase.models import BenefitsSection, Benefit
from ....serializers.home.benefits import BenefitsSectionSerializer



class BenefitsService:
    
    @staticmethod
    def get(website):
        section = (
            BenefitsSection.objects.filter(
                website=website,
                is_active=True,
                is_deleted=False
            )
            .prefetch_related("benefits")
            .first()
        )
        
        return section.to_dict() if section else None
    
    @staticmethod
    def get_for_admin(website):
        
        sections = BenefitsSection.objects.filter(website=website, is_deleted=False).prefetch_related("benefits")
        
        return { "benefitsSections": [section.to_dict() for section in sections] }


    @staticmethod
    def create(website, data):
        with transaction.atomic():

            benefits_data = data.pop("benefits", [])
            
            if data.get("is_active"):
                BenefitsSection.objects.filter(website=website, is_active=True, is_deleted=False).update(is_active=False)
                
            section = BenefitsSection.objects.create(website=website, **data)
            
            for benefit_data in benefits_data:
                Benefit.objects.create(
                    section=section,
                    **benefit_data
                )
            
            return section

    @staticmethod
    def get_by_id(website, benefit_id):
        try:
            section = BenefitsSection.objects.get(website=website, id=benefit_id, is_deleted=False)
            return BenefitsSectionSerializer(section).data
        except BenefitsSection.DoesNotExist:
            raise Exception(f"Sección with id {benefit_id} not found")
        
    @staticmethod
    def update_section(website, id, data):
 
        try:
            section_to_update = BenefitsSection.objects.get(
                website=website,
                id=id,
                is_deleted=False
            )
            
            with transaction.atomic():
                benefits_data = data.pop("benefits", None)
          
                
                if data.get("is_active"):
                    BenefitsSection.objects.filter(
                        website=website,
                        is_active=True,
                        is_deleted=False
                    ).exclude(id=id).update(is_active=False)
                    
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)


                section_to_update.save()
                
                if benefits_data is None:
                    return section_to_update
                
                
                existing_benefits = {benefit.pk: benefit for benefit in section_to_update.benefits.filter(is_deleted=False)}
          
                sent_ids = []
                
                for benefit_data in benefits_data:
                    benefit_id = benefit_data.get("id")
            
                    
                    if benefit_id and benefit_id in existing_benefits:
                        #UPDATE
                        benefit = existing_benefits[benefit_id]
                        
                        for attr, value in benefit_data.items():
                            setattr(benefit, attr, value)
                        
                        benefit.save()
                        sent_ids.append(benefit_id)
                    
                    else:
                        # CREATE
                        new_benefit: Benefit = Benefit.objects.create(
                             section=section_to_update,
                            **benefit_data
                        )
                        sent_ids.append(new_benefit.pk)
                
                # Soft-delete: marcar como eliminados los que el front ya no envía
                Benefit.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)
                
                        
                return section_to_update
            
            
            
        except BenefitsSection.DoesNotExist:
         
            raise Exception( f"Hero with ud {id} not found")
        
        
    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = BenefitsSection.objects.get(
                website=website,
                id=instance_id,
                is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except BenefitsSection.DoesNotExist:
            raise Exception("Section not found")
            