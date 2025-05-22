# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y luego instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación al contenedor
COPY . .

# Expone el puerto 8888
EXPOSE 8888

# Comando para arrancar el servidor con Uvicorn en el puerto 8888
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
