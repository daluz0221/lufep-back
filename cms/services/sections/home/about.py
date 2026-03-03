from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models import AboutSection, AboutMetric
from ....serializers.home.about import AboutSectionSerializer


class AboutService:
    @staticmethod
    def get(website):
        section = (
            AboutSection.objects.filter(
                website=website,
                is_active=True,
                is_deleted=False
            )
            .prefetch_related(
                Prefetch(
                    "metrics",
                    queryset=AboutMetric.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            )
            .first()
        )
        return section.to_dict() if section else None

    @staticmethod
    def get_for_admin(website):
        sections = AboutSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "metrics",
                queryset=AboutMetric.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return {"aboutSections": [section.to_dict() for section in sections]}

    @staticmethod
    def get_by_id(website, id):
        try:
            section = AboutSection.objects.prefetch_related(
                Prefetch(
                    "metrics",
                    queryset=AboutMetric.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return AboutSectionSerializer(section).data
        except AboutSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            metrics_data = data.pop("metrics", [])

            if data.get("is_active"):
                AboutSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            section = AboutSection.objects.create(website=website, **data)

            for metric_data in metrics_data:
                AboutMetric.objects.create(section=section, **metric_data)

            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = AboutSection.objects.get(
                website=website, id=id, is_deleted=False
            )
            with transaction.atomic():
                metrics_data = data.pop("metrics", None)
                if data.get("is_active"):
                    AboutSection.objects.filter(
                        website=website,
                        is_active=True,
                        is_deleted=False
                    ).exclude(id=id).update(is_active=False)
                for attr, value in data.items():
                    setattr(section_to_update, attr, value)
                section_to_update.save()
                if metrics_data is None:
                    section_to_update = AboutSection.objects.prefetch_related(
                        Prefetch(
                            "metrics",
                            queryset=AboutMetric.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_metrics = {
                    m.pk: m
                    for m in section_to_update.metrics.filter(is_deleted=False)
                }
                sent_ids = []
                for metric_data in metrics_data:
                    metric_id = metric_data.get("id")
                    if metric_id and metric_id in existing_metrics:
                        metric = existing_metrics[metric_id]
                        for attr, value in metric_data.items():
                            setattr(metric, attr, value)
                        metric.save()
                        sent_ids.append(metric_id)
                    else:
                        new_metric = AboutMetric.objects.create(
                            section=section_to_update, **metric_data
                        )
                        sent_ids.append(new_metric.pk)

                AboutMetric.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = AboutSection.objects.prefetch_related(
                    Prefetch(
                        "metrics",
                        queryset=AboutMetric.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update
        except AboutSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = AboutSection.objects.get(
                website=website, id=instance_id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except AboutSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")
