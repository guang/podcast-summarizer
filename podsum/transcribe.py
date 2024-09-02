import hashlib
import subprocess
from pathlib import Path

import requests
from fake_useragent import UserAgent
from pydub import AudioSegment

from podsum.constants import DL_DIR

WHISPER_PATHS = {
    "exec": "/Users/guangyang/whisper.cpp/main",
    "model": "/Users/guangyang/whisper.cpp/models/ggml-small.en.bin",
}
WHISPER_DEFAULT_SR = 16000


def transcribe_podcast_from_url(
    url: str,
    dl_dir=Path(DL_DIR),
):
    episode_internal_id = hashlib.md5(url.encode("utf-8")).hexdigest()
    filename = f"{episode_internal_id}.mp3"
    fp = dl_dir / filename
    if fp.exists():
        print("MP3 file already exists with fp:", fp)
        transcribe_podcast_from_file(fp)
        return episode_internal_id

    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    try:
        # send header first to check for redirect
        header_response = requests.head(url, allow_redirects=True, headers=headers)
        final_url = header_response.url
        response = requests.get(final_url)
        response.raise_for_status()
        with open(fp, "wb") as file:
            file.write(response.content)
        print("MP3 file downloaded successfully with fp:", fp)
        transcribe_podcast_from_file(fp)
        return episode_internal_id
    except requests.RequestException as e:
        raise ValueError(f"Error downloading MP3 from {url}", e)


def transcribe_podcast_from_file(fp: Path, whisper_paths=WHISPER_PATHS):
    print(f"Transcribing podcast from file {fp}")
    transcript_fp = fp.with_suffix(".txt")
    if transcript_fp.exists():
        print("Transcript file already exists with fp:", transcript_fp)
        return transcript_fp
    ext = fp.suffix
    if ext == ".mp3":
        audio = AudioSegment.from_mp3(fp)
        audio = audio.set_frame_rate(WHISPER_DEFAULT_SR)
        audio.export(fp.with_suffix(".wav"), format="wav")
        fp = fp.with_suffix(".wav")
        ext = fp.suffix
    else:
        raise ValueError(f"Only .mp3 files are supported, got {ext}")
    try:
        completed_process = subprocess.run(
            [
                whisper_paths["exec"],
                "nt",
                "-t",
                "20",
                "-p",
                "5",
                "-otxt",
                "-of",
                str(fp.stem),
                "-m",
                whisper_paths["model"],
                "-f",
                str(fp),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return_code = completed_process.returncode
        stdout_output = completed_process.stdout.decode("utf-8")
        stderr_output = completed_process.stderr.decode("utf-8")
        # Print the return code and output
        print("Return code:", return_code)
        print("Standard output: (preview)")
        print(stdout_output[:1000])
        print("Standard error:")
        print(stderr_output)
        with open(transcript_fp, "wb") as file:
            file.write(stdout_output.encode("utf-8"))

    except subprocess.CalledProcessError as e:
        raise ValueError("Error running whisper: ", e)
