FROM ubuntu
FROM python:3.9

WORKDIR /code

RUN apt update && apt install ffmpeg -y
RUN pip install --no-cache-dir --upgrade git+https://github.com/openai/whisper.git fastapi[all] yt-dlp openai

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
