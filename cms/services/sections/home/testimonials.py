from django.db import transaction  # type: ignore
from apps.showcase.models import TestimonialSection
from apps.showcase.models.home import Testimonial, TertimonialMetric
from ....serializers.home.testimonials import TestimonialSectionSerializer


class TestimonialsService:
    @staticmethod
    def get(website):
        section = (
            TestimonialSection.objects.filter(
                website=website,
                is_active=True,
                is_deleted=False
            )
            .prefetch_related("testimonials", "metrics")
            .first()
        )
        return section.to_dict() if section else None

    @staticmethod
    def get_for_admin(website):
        sections = TestimonialSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related("testimonials", "metrics")
        return {
            "testimonialSections": [section.to_dict() for section in sections]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            section = TestimonialSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            return TestimonialSectionSerializer(section).data
        except TestimonialSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            testimonials_data = data.pop("testimonials", [])
            metrics_data = data.pop("metrics", [])

            if data.get("is_active"):
                TestimonialSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            section = TestimonialSection.objects.create(website=website, **data)

            for testimonial_data in testimonials_data:
                Testimonial.objects.create(section=section, **testimonial_data)
            for metric_data in metrics_data:
                TertimonialMetric.objects.create(section=section, **metric_data)

            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = TestimonialSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            with transaction.atomic():
                testimonials_data = data.pop("testimonials", None)
                metrics_data = data.pop("metrics", None)

                if data.get("is_active"):
                    TestimonialSection.objects.filter(
                        website=website,
                        is_active=True,
                        is_deleted=False
                    ).exclude(id=id).update(is_active=False)

                for attr, value in data.items():
                    setattr(section_to_update, attr, value)
                section_to_update.save()

                if testimonials_data is not None:
                    existing_testimonials = {
                        t.pk: t
                        for t in section_to_update.testimonials.filter(
                            is_deleted=False
                        )
                    }
                    sent_ids = []
                    for item_data in testimonials_data:
                        item_id = item_data.get("id")
                        if item_id and item_id in existing_testimonials:
                            item = existing_testimonials[item_id]
                            for attr, value in item_data.items():
                                setattr(item, attr, value)
                            item.save()
                            sent_ids.append(item_id)
                        else:
                            new_item = Testimonial.objects.create(
                                section=section_to_update, **item_data
                            )
                            sent_ids.append(new_item.pk)
                    Testimonial.objects.filter(
                        section=section_to_update
                    ).exclude(id__in=sent_ids).update(is_deleted=True)

                if metrics_data is not None:
                    existing_metrics = {
                        m.pk: m
                        for m in section_to_update.metrics.filter(
                            is_deleted=False
                        )
                    }
                    sent_ids = []
                    for item_data in metrics_data:
                        item_id = item_data.get("id")
                        if item_id and item_id in existing_metrics:
                            item = existing_metrics[item_id]
                            for attr, value in item_data.items():
                                setattr(item, attr, value)
                            item.save()
                            sent_ids.append(item_id)
                        else:
                            new_item = TertimonialMetric.objects.create(
                                section=section_to_update, **item_data
                            )
                            sent_ids.append(new_item.pk)
                    TertimonialMetric.objects.filter(
                        section=section_to_update
                    ).exclude(id__in=sent_ids).update(is_deleted=True)

                return section_to_update
        except TestimonialSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = TestimonialSection.objects.get(
                website=website, id=instance_id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except TestimonialSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")
