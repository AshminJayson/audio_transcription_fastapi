import os
import openai
from fastapi import FastAPI
from yt_dlp import YoutubeDL
import uvicorn
import whisper

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")


file_name = 'testing'
ydl_opts = {

    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "outtmpl": f'{file_name}.%(ext)s',
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

        model = whisper.load_model("base")
        result = model.transcribe(f"{file_name}.m4a")

        # audio_file = open(f'{file_name}.m4a', 'rb')
        # transcript = openai.Audio.transcribe('whisper-1', audio_file)

        # with open(f'{file_name}.txt', 'w') as f:
        #     f.write(str(result))
        segments = [{'start': i['start'], 'end': i['end'], 'text': i['text']}
                    for i in result['segments']]
        os.remove(f"{file_name}.m4a")
        return segments


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
