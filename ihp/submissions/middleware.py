import models
import translations

class TranslationMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "language" in view_kwargs:
            language = models.Language.objects.get(language=view_kwargs["language"] or "English")
            translation = translations.get_translation(language)
            request.translation = translation
        return None
