# Usar la imagen base de Nginx
FROM nginx:alpine

# Copiar el archivo de configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos del frontend al directorio raíz de Nginx
COPY . /usr/share/nginx/html

# Exponer el puerto para el frontend
EXPOSE 80

# Iniciar el servidor Nginx
CMD ["nginx", "-g", "daemon off;"]
