# Usa uma imagem oficial leve do Python
FROM python:3.10-slim

# Cria diretório e define como raiz do app
WORKDIR /app

# Copia tudo para dentro do container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Porta usada pelo Cloud Run
ENV PORT=8080

# Expõe a porta do container
EXPOSE 8080

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
