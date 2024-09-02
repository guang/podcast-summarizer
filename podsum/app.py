from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from podsum.schemas import EpisodeInternalID, PodcastURL, Segment, Test
from podsum.summarize import summarize_on_transcript
from podsum.transcribe import transcribe_podcast_from_url

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/transcribe/", response_model=EpisodeInternalID)
async def transcribe_podcast(url_request: PodcastURL):
    try:
        episode_internal_id = transcribe_podcast_from_url(url_request.url)
        return EpisodeInternalID(id=episode_internal_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/summarize/", response_model=list[Segment])
async def summarize_podcast(episode_internal_id: EpisodeInternalID):
    try:
        summary = summarize_on_transcript(episode_internal_id.id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
