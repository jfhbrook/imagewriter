from typing import Dict, Self

import ipywidgets as widgets

from imagewriter.language import Language

LANGUAGES: Dict[str, Language] = {language.value: language for language in Language}


class LanguageWidget(widgets.Dropdown):
    def __init__(self: Self, language: Language) -> None:
        super().__init__(
            options=list(LANGUAGES.keys()),
            value=self._start_value(language),
            description="Language:",
            disabled=False,
        )

    def _start_value(self: Self, language: Language) -> str:
        return language.value

    @property
    def language(self: Self) -> Language:
        value: str = self.value if self.value else "American"
        return LANGUAGES[value]
