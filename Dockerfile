FROM python:3.14-slim

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/exports

CMD ["python", "bot_main.py"]