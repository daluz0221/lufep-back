from django.db import transaction

from apps.showcase.models import BenefitsSection, Benefit
from ....serializers.home.benefits import BenefitsSectionSerializer



class BenefitsService:
    
    @staticmethod
    def get(website):
        section = (
            BenefitsSection.objects.filter(
                website=website,
                is_active=True
            )
            .prefetch_related("benefits")
            .first()
        )
        
        return section.to_dict() if section else None
    
    @staticmethod
    def get_for_admin(website):
        
        sections = BenefitsSection.objects.filter(website=website).prefetch_related("benefits")
        
        return { "benefitsSections": [section.to_dict() for section in sections] }


    @staticmethod
    def create(website, data):
        with transaction.atomic():

            benefits_data = data.pop("benefits", [])
            
            if data.get("is_active"):
                BenefitsSection.objects.filter(website=website, is_active=True).update(is_active=False)
                
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
            section = BenefitsSection.objects.get(website=website, id=benefit_id)
            return BenefitsSectionSerializer(section).data
        except BenefitsSection.DoesNotExist:
            raise Exception(f"Sección with id {benefit_id} not found")
        
    @staticmethod
    def update_section(website, id, data):
 
        try:
            section_to_update = BenefitsSection.objects.get(
                website=website,
                id=id
            )
            
            with transaction.atomic():
                benefits_data = data.pop("benefits", None)
          
                
                if data.get("is_active"):
                    BenefitsSection.objects.filter(
                        website=website,
                        is_active=True
                    ).exclude(id=id).update(is_active=False)
                    
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)


                section_to_update.save()
                
                if benefits_data is None:
                    return section_to_update
                
                
                existing_benefits = {benefit.pk: benefit for benefit in section_to_update.benefits.all()}
          
                sent_ids = []
                
                for benefit_data in benefits_data:
                    benefit_id = benefit_data.get("id")
                    print(benefit_data)
                    
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
                
                #DELETE los que no vengan
                # for benefit_id, benefit in existing_benefits.items():
                #     if benefit_id not in sent_ids:
                #         benefit.delete()
                Benefit.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).delete()
                
                        
                return section_to_update
            
            
            
        except BenefitsSection.DoesNotExist:
         
            raise Exception( f"Hero with ud {id} not found")
        
        
    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = BenefitsSection.objects.get(
                website=website,
                id=instance_id
            )
            section.delete()
        except BenefitsSection.DoesNotExist:
            raise Exception("Section not found")
            