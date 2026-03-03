from typing import TYPE_CHECKING
from django.db import models  # type: ignore
from core.models import Website

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # type: ignore


class ProductsPageBase(models.Model):
    """Base para secciones de la página Productos (una activa por website)."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# ─── INTRO ───────────────────────────────────────────────────────────────────
class ProductsIntroSection(ProductsPageBase):
    """Sección de encabezado de la página de productos (IntroProducts.astro)."""
    title = models.CharField(max_length=200)
    description = models.TextField()





# ─── PRODUCTO INDIVIDUAL ──────────────────────────────────────────────────────
class ProductsItem(ProductsPageBase):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    imageUrl = models.CharField(max_length=500)
    imageAlt = models.CharField(max_length=200, default="")
    forWho = models.TextField(
        help_text="Texto del bloque '¿Para quién es?' de cada producto."
    )
    includes: "RelatedManager[ProductsItemInclude]"

# ─── ÍTEMS DE "¿QUÉ INCLUYE?" ────────────────────────────────────────────────
class ProductsItemInclude(models.Model):
    """Cada línea de la lista '¿Qué incluye?' de un producto."""
    product = models.ForeignKey(
        ProductsItem, on_delete=models.CASCADE, related_name="includes"
    )

    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]
