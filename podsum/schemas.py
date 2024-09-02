from pydantic import BaseModel, Field


class PodcastURL(BaseModel):
    url: str


class EpisodeInternalID(BaseModel):
    id: str


class Test(BaseModel):
    name: str


class Segment(BaseModel):
    segment_title: str = Field(description="Segment title in a short sentence")
    description: str
    direct_quote: str
    timestamp: str = Field(description="The starting timestamp in the format HH:MM:SS")
