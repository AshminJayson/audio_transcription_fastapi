import os
import openai
from fastapi import FastAPI
from yt_dlp import YoutubeDL
import uvicorn

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")


file_name = 'testing'
ydl_opts = {

    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "outtmpl": f'/{file_name}.%(ext)s',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
}


@app.get('/')
async def ping():
    return {'message': "go to /docs to view routes"}


@app.get('/get_transcription')
async def get_transcription(url):
    print(url)
    URL = [url]
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)
        audio_file = open(f'{file_name}.m4a', 'rb')
        transcript = openai.Audio.transcribe('whisper-1', audio_file)

        return transcript


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
