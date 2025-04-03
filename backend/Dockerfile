# Usar una imagen base de Python
FROM python:3.9-slim

# Crear el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto para FastAPI
EXPOSE 3000

# Ejecutar el servidor
CMD ["uvicorn", "mnist_server:app", "--host", "0.0.0.0", "--port", "3000"]
