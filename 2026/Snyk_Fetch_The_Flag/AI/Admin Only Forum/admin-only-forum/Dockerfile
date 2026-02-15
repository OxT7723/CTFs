FROM python:3.11-slim
WORKDIR /app
RUN mkdir -p /data
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
EXPOSE 5000
CMD ["python", "app.py"]
