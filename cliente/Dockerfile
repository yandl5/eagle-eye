FROM python:3.13-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY . .
COPY template/ ./templates/

EXPOSE 5000

CMD ["python", "main.py"]
