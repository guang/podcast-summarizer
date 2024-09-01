from pathlib import Path
from typing import List, Optional

import google.generativeai as genai
import instructor
from pydantic import BaseModel, Field

gem_client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",  # model defaults to "gemini-pro"
    ),
    mode=instructor.Mode.GEMINI_JSON,
)


class Segment(BaseModel):
    segment_title: str = Field(description="Segment title in a short sentence")
    description: str
    direct_quote: str
    timestamp: str = Field(description="The starting timestamp in the format HH:MM:SS")


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


def summarize_on_transcript(fp: Path):
    with open(fp, "r") as f:
        transcript = f.readlines()
    if len(transcript) < 5:
        raise ValueError(f"Error: Transcript file '{fp}' is empty.")

    segments = summarize(transcript)
    return segments
