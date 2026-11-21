from collections.abc import Callable

from parsy import alt  # type: ignore

from imagewriter.base.quality import Quality
from imagewriter.decoding.base import esc
from imagewriter.encoding.quality import SetQuality


def _map_scribe_quality(quality: Quality) -> Callable[[bytes], SetQuality]:
    return lambda _: SetQuality(quality, scribe_mode=True)


def _map_quality(quality: Quality) -> Callable[[bytes], SetQuality]:
    return lambda _: SetQuality(quality, scribe_mode=False)


set_quality = alt(
    esc("m").map(_map_scribe_quality(Quality.CORRESPONDENCE)),
    esc("M").map(_map_scribe_quality(Quality.NEAR_LETTER_QUALITY)),
    *[esc(f"a{quality.value}").map(_map_quality) for quality in Quality],
)
