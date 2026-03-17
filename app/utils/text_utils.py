import re
import unicodedata

from app.utils.constants import SPECIALTY_ALIASES


def normalize_text(text: str | None) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-\/]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_normalized_phrase(text: str, phrase: str) -> bool:
    normalized_text = normalize_text(text)
    normalized_phrase = normalize_text(phrase)
    if not normalized_phrase:
        return False
    return normalized_phrase in normalized_text


def unique_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    output = []

    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)

    return output


def normalize_specialty_name(name: str) -> str:
    return SPECIALTY_ALIASES.get(name, name)