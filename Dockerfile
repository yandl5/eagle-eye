# Usar imagem Python leve
FROM python:3.11-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências do sistema que algumas libs podem precisar
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para aproveitar cache no build)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código para dentro do container
COPY eagle-eye.py .

# Expor a porta usada pelo serviço SOAP
EXPOSE 8000

# Rodar o servidor SOAP
CMD ["python", "eagle-eye.py"]
