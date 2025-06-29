from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock

class FeatureBlock(StructBlock):
    icon = ChoiceBlock(choices=[
        ("🧪", "Lab"),
        ("🥗", "Nutrition"),
        ("🤖", "AI"),
        ("💊", "Medication"),
    ])
    title = CharBlock(required=True)
    description = CharBlock(required=True)

    class Meta:
        icon = "plus"
        label = "Feature"

class HomePage(Page):
    hero_title = models.CharField(max_length=255, default="Your Personal Health Hub")
    hero_subtitle = models.CharField(max_length=255, default="Track, understand, and improve your health.")
    features = StreamField([
        ("feature", FeatureBlock())
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("features"),
    ]
