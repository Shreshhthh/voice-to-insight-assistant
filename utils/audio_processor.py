import os
import shutil
import re
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR,exist_ok = True)


def download_youtube_audio(url: str, output_dir: str = DOWNLOAD_DIR):
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "%(id)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "windowsfilenames": True,
        "overwrites": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise ValueError(f"Could not fetch metadata for URL: {url}")

        video_id = info.get("id")
        file_name = os.path.join(output_dir, f"{video_id}.wav")

    return file_name


def convert_file_to_wav(input_file: str)->str:
    """Convert an audio/video file to WAV format using pydub."""

    output_path = os.path.splitext(input_file)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

def process_input(source: str):
    if source.startswith("http://") or source.startswith('https://'):
        print("Downloading audio.....")
        wav_path = download_youtube_audio(source)
    else:
        print('converting to wav.....')
        wav_path = convert_file_to_wav(source)
    
    print("Chunking audio.....")
    chunks = chunk_audio(wav_path)
    return chunks