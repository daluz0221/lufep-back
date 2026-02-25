# apps/showcase/models/about.py
from typing import TYPE_CHECKING
from django.db import models #type: ignore
from core.models import Website

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager #type: ignore

class AboutPageBase(models.Model):
    """Base para secciones de la página About (una activa por website)."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# ─── INTRO ───────────────────────────────────────────────────────────────
class AboutIntroSection(AboutPageBase):
    title = models.CharField(max_length=200)
    highlight_word = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()

   


# ─── HISTORIA ────────────────────────────────────────────────────────────
class AboutHistorySection(AboutPageBase):
    title = models.CharField(max_length=200, default="Nuestra Historia")
    image = models.CharField(max_length=500)
    image_alt = models.CharField(max_length=200, default="")
    
    content = models.TextField()  

    


# ─── VISIÓN (Misión / Visión / Valores) ──────────────────────────────────
class AboutVisionSection(AboutPageBase):
    title = models.CharField(max_length=200, blank=True)  # Opcional, el front no lo usa

    # Relación con los 3 bloques
    vision_items: "RelatedManager[AboutVisionItem]"

    


class AboutVisionItem(models.Model):
    section = models.ForeignKey(
        AboutVisionSection, on_delete=models.CASCADE, related_name="vision_items"
    )
    title = models.CharField(max_length=100)  # "Misión", "Visión", "Valores"
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

   


# ─── DIFERENCIADORES ─────────────────────────────────────────────────────
class AboutDifferentiatorsSection(AboutPageBase):
    title = models.CharField(max_length=200, default="¿Por qué elegirnos?")
    differentiators: "RelatedManager[AboutDifferentiator]"

    


class AboutDifferentiator(models.Model):
    section = models.ForeignKey(
        AboutDifferentiatorsSection, on_delete=models.CASCADE, related_name="differentiators"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    


# ─── EQUIPO ──────────────────────────────────────────────────────────────
class AboutTeamSection(AboutPageBase):
    title = models.CharField(max_length=200, default="El Equipo Detrás")
    members: "RelatedManager[AboutTeamMember]"

    


class AboutTeamMember(models.Model):
    section = models.ForeignKey(
        AboutTeamSection, on_delete=models.CASCADE, related_name="members"
    )
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    image = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    