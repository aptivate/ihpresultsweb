def get_translation(language):
    if language.language == "French":
        import translations_fr
        return translations_fr
    else:
        import translations_en
        return translations_en

