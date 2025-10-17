# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y usa logs legibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para TensorFlow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos e instálalos
COPY requirements_app.txt .
RUN pip install --no-cache-dir -r requirements_app.txt

# Copia el resto del código
COPY . .

# Expone el puerto de FastAPI
EXPOSE 8000

# Comando para iniciar la API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
