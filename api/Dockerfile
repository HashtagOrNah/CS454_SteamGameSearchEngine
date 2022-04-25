FROM python:3.9-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY gameIndex ./gameIndex
COPY *.py ./
CMD gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api:app
