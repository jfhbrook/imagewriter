from parsy import alt  # type: ignore

from imagewriter.decoding.base import esc_command
from imagewriter.encoding.paper import SetPaperOutSensor

set_paper_out_sensor = alt(
    esc_command(SetPaperOutSensor(True)), esc_command(SetPaperOutSensor(False))
)
