# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements_app.txt .
RUN pip install --no-cache-dir -r requirements_app.txt

COPY app ./app
COPY models ./models

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
