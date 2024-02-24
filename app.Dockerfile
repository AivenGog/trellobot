FROM python:3.11-slim-bookworm
WORKDIR /home

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY trellobot.py config.py ./

ENTRYPOINT ["python", "-u", "trellobot.py"]