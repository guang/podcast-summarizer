from pathlib import Path

from podsum.summarize import (
    summarize_on_transcript,  # Import the function you want to test
)
from podsum.utils import pretty_print_summary


def test_summarize_on_transcript():
    summary = summarize_on_transcript(fp=Path("test_transcript.txt"))
    pretty_print_summary(summary)
    assert len(summary) > 3, "Shouldn't be less than 3 segments"
