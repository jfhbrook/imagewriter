from typing import Dict, Self

import ipywidgets as widgets

from imagewriter.language import Language

LANGUAGES: Dict[str, Language] = {language.value: language for language in Language}


class LanguageWidget(widgets.Dropdown):
    def __init__(self: Self, language: Language) -> None:
        super().__init__(
            options=list(LANGUAGES.keys()),
            value=language.value,
            description="Language:",
            disabled=False,
        )

    @property
    def language(self: Self) -> Language:
        value: str = self.value if self.value else "American"
        return LANGUAGES[value]

    @language.setter
    def language(self: Self, language: Language) -> None:
        self.value = language.value
