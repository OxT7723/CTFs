FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       bash \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r guest \
    && useradd -r -m -g guest -s /bin/bash guest

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/
COPY flag.txt /app/
COPY static /app/static/
COPY templates /app/templates/
COPY commands /app/commands/


RUN chmod +x /app/commands/*.sh || true \
    && for f in /app/commands/*.sh; do \
         base=$(basename "$f" .sh); \
         ln -sf "$f" "/usr/local/bin/$base"; \
       done

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chown -R guest:guest /app \
    && if [ -f /app/flag.txt ]; then chown guest:guest /app/flag.txt && chmod 400 /app/flag.txt; fi

ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

USER guest

CMD ["python", "app.py"]
