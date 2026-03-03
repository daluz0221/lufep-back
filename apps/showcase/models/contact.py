from typing import TYPE_CHECKING
from django.db import models  # type: ignore
from core.models import Website

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # type: ignore



def validate_allowed_fields(fields: list[str]) -> bool:
    """Validar que los campos permitidos sean los permitidos."""
    allowed_fields = ["name", "email", "subject"]
    return all(field in allowed_fields for field in fields)

class ContactPageBase(models.Model):
    """Base para secciones de la página Contacto (una activa por website)."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# ─── FORMULARIO ─────────────────────────────────────────────────────────────
class ContactFormSection(ContactPageBase):
    """Sección del formulario de contacto (FormContact.astro)."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    form_fields = models.JSONField(
        default=list,
        validators=[validate_allowed_fields],
        help_text="Array de campos a mostrar: name, email, subject",
    )

    subject_options: "RelatedManager[ContactFormSubjectOption]"


class ContactFormSubjectOption(models.Model):
    """Opción del select de asunto en el formulario."""
    section = models.ForeignKey(
        ContactFormSection, on_delete=models.CASCADE, related_name="subject_options"
    )
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]


# ─── INFO DE CONTACTO ──────────────────────────────────────────────────────
class ContactInfoSection(ContactPageBase):
    """Sección de información de contacto, mapa y horario (InfoContact.astro)."""
    phone = models.CharField(max_length=100, blank=True, null=True)
    phone_text = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    email_text = models.CharField(max_length=200, blank=True, null=True)
    map_text = models.CharField(max_length=200, default="Ubicación del negocio")
    schedule_title = models.CharField(max_length=200, default="Horario de Visitas")
    extra_text = models.TextField(blank=True, null=True)

    schedule_fields: "RelatedManager[ContactScheduleField]"


class ContactScheduleField(models.Model):
    """Línea del horario de visitas."""
    section = models.ForeignKey(
        ContactInfoSection, on_delete=models.CASCADE, related_name="schedule_fields"
    )
    title_time = models.CharField(max_length=200)
    title_period = models.CharField(max_length=200)
    extra_time = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]
