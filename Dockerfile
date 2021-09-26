FROM ubuntu

RUN apt update

RUN apt install ffmpeg

CMD ["python3", "main.py"]
