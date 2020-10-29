from modeltranslation.translator import register, TranslationOptions

from .models import Business


@register(Business)
class BusinessTranslationOptions(TranslationOptions):
    fields = ("slogan", "description")
