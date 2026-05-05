FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir openpyxl pandas && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /src/data /src/exports

CMD ["python", "src/bot_main.py"]