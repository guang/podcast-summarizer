from pathlib import Path
from typing import List

import google.generativeai as genai
import instructor

from podsum.constants import DL_DIR
from podsum.schemas import Segment

gem_client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",  # model defaults to "gemini-pro"
    ),
    mode=instructor.Mode.GEMINI_JSON,
)


def summarize(transcript: str):
    segments = gem_client.chat.completions.create(
        max_tokens=8024,
        messages=[
            {
                "role": "system",
                "content": "Act as an expert researcher specializing in analyzing and extracting insights from long transcripts.",
            },
            {
                "role": "user",
                "content": f"""Generate segments from the following transcript that identify topics by theme. Each segment should have:
                    * A segment title that is descriptive, attention-grabbing, and memorable
                    * A brief description (about 1-2 sentences) explaining the content of the segment
                    * The starting timestamp in the format HH:MM:SS
                    * A direct quote that captures the essence of the segment
                    ---
                    \n\n\n{transcript}
                """,
            },
        ],
        response_model=List[Segment],
    )
    return segments


def summarize_on_transcript(episode_internal_id: str, dl_dir=Path(DL_DIR)):
    filename = f"{episode_internal_id}.txt"
    fp = dl_dir / filename

    print(f"Summarizing podcast from file {fp}")
    with open(fp, "r") as f:
        transcript = f.readlines()
    if len(transcript) < 5:
        raise ValueError(f"Error: Transcript file '{fp}' is empty.")

    segments = summarize(transcript)
    return segments
