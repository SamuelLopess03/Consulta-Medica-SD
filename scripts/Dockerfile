FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["python", "init_system.py"]
