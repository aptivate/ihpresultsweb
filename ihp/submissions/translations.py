def get_translation(language):
    if language == "fr":
        import translations_fr
        return translations_fr
    else:
        import translations_en
        return translations_en

