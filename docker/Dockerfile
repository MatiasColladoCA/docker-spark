# =================================================================
# Dockerfile para Proyecto Spark
# Basado en Apache Spark 4.0.1 con Python 3
# =================================================================

# 1. Usar la nueva imagen oficial de Spark como base
FROM apache/spark:4.0.1-scala2.13-java17-ubuntu

# 2. Cambiar a root para instalar TODAS las dependencias (sistema y Python)
USER root

# 3. Instalar pip para Python 3
RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 4. Crear el directorio de trabajo y copiar los archivos de dependencias
#    Hacemos esto como root para evitar problemas de permisos en la copia.
WORKDIR /opt/spark-app
COPY requirements.txt .

# 5. Instalar las dependencias de Python como root
RUN pip3 install -r requirements.txt

# 6. Cambiar el propietario del directorio de trabajo al usuario 'spark'
#    y luego cambiar a ese usuario para ejecutar la aplicación.
RUN chown -R spark:spark /opt/spark-app
USER spark

# 7. Copiar el resto del código fuente.
#    Como el directorio ya pertenece a 'spark', no necesitamos --chown.
COPY . .

# 8. Establecer un comando por defecto
CMD ["sleep", "infinity"]