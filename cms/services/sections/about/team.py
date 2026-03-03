from django.db import transaction  # type: ignore
from django.db.models import Prefetch  # type: ignore
from apps.showcase.models.about import AboutTeamSection, AboutTeamMember
from ....serializers.about.team import AboutTeamSectionSerializer


class TeamService:

    @staticmethod
    def get(website):
        section = AboutTeamSection.objects.filter(
            website=website,
            is_active=True,
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                "members",
                queryset=AboutTeamMember.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        ).first()
        return AboutTeamSectionSerializer(section).data if section else None

    @staticmethod
    def get_for_admin(website):
        sections = AboutTeamSection.objects.filter(
            website=website, is_deleted=False
        ).prefetch_related(
            Prefetch(
                "members",
                queryset=AboutTeamMember.objects.filter(
                    is_deleted=False
                ).order_by("order"),
            )
        )
        return {
            "teamSections": [
                AboutTeamSectionSerializer(section).data for section in sections
            ]
        }

    @staticmethod
    def get_by_id(website, id):
        try:
            section = AboutTeamSection.objects.prefetch_related(
                Prefetch(
                    "members",
                    queryset=AboutTeamMember.objects.filter(
                        is_deleted=False
                    ).order_by("order"),
                )
            ).get(website=website, id=id, is_deleted=False)
            return AboutTeamSectionSerializer(section).data
        except AboutTeamSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def create_section(website, data):
        with transaction.atomic():
            members_data = data.pop("members", [])

            if data.get("is_active"):
                AboutTeamSection.objects.filter(
                    website=website, is_active=True, is_deleted=False
                ).update(is_active=False)

            section = AboutTeamSection.objects.create(website=website, **data)
            for member_data in members_data:
                AboutTeamMember.objects.create(section=section, **member_data)
            return section

    @staticmethod
    def update_section(website, id, data):
        try:
            section_to_update = AboutTeamSection.objects.get(
                website=website, id=id, is_deleted=False
            )

            with transaction.atomic():
                members_data = data.pop("members", None)

                if data.get("is_active"):
                    AboutTeamSection.objects.filter(
                        website=website, is_active=True, is_deleted=False
                    ).exclude(id=id).update(is_active=False)

                for attr, value in data.items():
                    setattr(section_to_update, attr, value)

                section_to_update.save()

                if members_data is None:
                    section_to_update = AboutTeamSection.objects.prefetch_related(
                        Prefetch(
                            "members",
                            queryset=AboutTeamMember.objects.filter(
                                is_deleted=False
                            ).order_by("order"),
                        )
                    ).get(pk=section_to_update.pk)
                    return section_to_update

                existing_members = {
                    m.pk: m
                    for m in section_to_update.members.filter(is_deleted=False)
                }
                sent_ids = []

                for member_data in members_data:
                    member_id = member_data.get("id")
                    if member_id and member_id in existing_members:
                        member = existing_members[member_id]
                        for attr, value in member_data.items():
                            setattr(member, attr, value)
                        member.save()
                        sent_ids.append(member_id)
                    else:
                        new_member = AboutTeamMember.objects.create(
                            section=section_to_update, **member_data
                        )
                        sent_ids.append(new_member.pk)

                AboutTeamMember.objects.filter(
                    section=section_to_update
                ).exclude(id__in=sent_ids).update(is_deleted=True)

                section_to_update = AboutTeamSection.objects.prefetch_related(
                    Prefetch(
                        "members",
                        queryset=AboutTeamMember.objects.filter(
                            is_deleted=False
                        ).order_by("order"),
                    )
                ).get(pk=section_to_update.pk)
                return section_to_update

        except AboutTeamSection.DoesNotExist:
            raise Exception(f"Sección with id {id} not found")

    @staticmethod
    def delete_section(website, instance_id):
        try:
            section = AboutTeamSection.objects.get(
                website=website, id=instance_id, is_deleted=False
            )
            section.is_deleted = True
            section.save()
        except AboutTeamSection.DoesNotExist:
            raise Exception(f"Sección with id {instance_id} not found")