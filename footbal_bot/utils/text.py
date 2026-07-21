def normalize(text: str) -> str:
    """
    Türkçe karakterleri normalize eder.
    """

    replacements = str.maketrans({
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "İ": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    })

    return text.lower().translate(replacements).strip()