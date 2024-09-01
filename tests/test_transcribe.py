import uuid

from podsum.transcribe import transcribe_podcast_from_url


def test_transcribe_podcast_from_url():
    url = "https://audio.listennotes.com/e/p/cc49ef69c924438297f8cd1dc0b60f7e/"
    # url = "https://audio.listennotes.com/e/p/1353d34350f04600a6f28f57fa672d89/" # short

    # Generate a random UUID and use it as a string
    episode_internal_id = str(uuid.uuid4())

    transcript_fp = transcribe_podcast_from_url(
        url=url,
        episode_internal_id=episode_internal_id,
    )
    assert transcript_fp.exists()
    # transcript_fp.unlink()
