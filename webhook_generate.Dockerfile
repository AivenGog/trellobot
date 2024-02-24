FROM python:3.11-slim-bookworm
WORKDIR /home/webhook_generate

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY webhook_generate.py config.py ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "webhook_generate.py"]