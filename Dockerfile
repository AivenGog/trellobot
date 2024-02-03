FROM python:3.11-slim-bookworm
WORKDIR /home
COPY webhook_generate.py trellobot.py requirements.txt config.py docker-entrypoint.sh ./
RUN chmod 755 *.py docker-entrypoint.sh

RUN pip install -r requirements.txt
HEALTHCHECK --interval=5m --timeout=5s \
  CMD curl -I -f http://localhost:$PORT || exit 1

SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["./docker-entrypoint.sh"]