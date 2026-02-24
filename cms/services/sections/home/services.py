from django.db import transaction #type: ignore

from apps.showcase.models import ServiceSection, Service

from ....serializers.home.services import SerivceSectionSerializer

class ServiceSectionService:
    
    @staticmethod
    def get(website):
        section = (
            ServiceSection.objects.filter(
                website=website,
                is_active=True,
                is_deleted=False
            )
            .prefetch_related("servicios")
            .first()
        )
        
        return section.to_dict() if section else None
    
    @staticmethod
    def get_for_admin(website):
        sections = ServiceSection.objects.filter(website=website, is_deleted=False).prefetch_related("servicios")
        return { "serviceSections": [section.to_dict() for section in sections] }
    
    
    @staticmethod
    def get_by_id(website, id):
        try:
            section = ServiceSection.objects.get(website=website, id=id, is_deleted=False)
            return SerivceSectionSerializer(section).data
        except ServiceSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
    
    
    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            
            services_data = data.pop("servicios", [])
            
            if data.get("is_active"):
                ServiceSection.objects.filter(website=website, is_active=True, is_deleted=False).update(is_active=False)
            
            section = ServiceSection.objects.create(website=website, **data)
            
            for service_data in services_data:
                Service.objects.create(
                    section=section,
                    **service_data
                )            
                
            return section
        
        
    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = ServiceSection.objects.get(website=website, id=id, is_deleted=False)
            with transaction.atomic():
                services_data = data.pop("servicios", None)
                if data.get("is_active"):
                    ServiceSection.objects.filter(website=website, is_active=True, is_deleted=False).exclude(id=id).update(is_active=False)
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)
                section_to_update.save()
                if services_data is None:
                    return section_to_update
                
                
                existing_services = {service.pk: service for service in section_to_update.servicios.filter(is_deleted=False)}
                sent_ids = []
                for service_data in services_data:
                    service_id = service_data.get("id")
                    if service_id and service_id in existing_services:
                        service = existing_services[service_id]
                        for attr, value in service_data.items():
                            setattr(service, attr, value)
                        service.save()
                        sent_ids.append(service_id)
                    
                    else:
                        #CREATE
                        new_service: Service = Service.objects.create(
                            section=section_to_update,
                            **service_data
                        )
                        sent_ids.append(new_service.pk)
                    
                # Soft-delete: marcar como eliminados los que el front ya no envía
                Service.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)
                
                return section_to_update                           
                            
                            
        except ServiceSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")
        
        
    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = ServiceSection.objects.get(website=website, id=instance_id, is_deleted=False)
            section.is_deleted = True
            section.save()
        except ServiceSection.DoesNotExist:
            raise Exception("Section not found")