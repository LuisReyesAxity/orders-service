# Imagen base de Python
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias
COPY pyproject.toml .
COPY poetry.lock .

# Instalar dependencias
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copiar el código
COPY src/ ./src/
COPY main.py .

# Exponer el puerto
EXPOSE 8000

# Comando para arrancar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]