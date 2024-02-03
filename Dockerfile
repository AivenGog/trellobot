FROM python:3.11-slim-bookworm
WORKDIR /home
COPY --chmod=755 webhook_generate.py trellobot.py requirements.txt config.py docker-entrypoint.sh ./

RUN pip install -r requirements.txt
ARG PORT
HEALTHCHECK --start-period=5s --interval=5m --timeout=5s \
  CMD curl -I -f http://localhost:PORT || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]