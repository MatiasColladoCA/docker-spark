
# Análisis de Datos de Ventas con Docker y Apache Spark

Este proyecto demuestra la implementación de un pipeline de datos ETL (Extraer, Transformar, Cargar) utilizando un clúster de Apache Spark orquestado con Docker. El diseño se centra en la reproducibilidad, la escalabilidad y la separación de responsabilidades, siguiendo las mejores prácticas de la ingeniería de software moderna para crear un entorno de análisis de datos robusto y profesional.

## Arquitectura General

La solución se compone de varios servicios orquestados mediante Docker Compose, cada uno con un rol específico dentro del ecosistema de procesamiento de datos:

-   **Spark Master:** Nodo maestro que gestiona los recursos del clúster y coordina la ejecución de tareas.
-   **Spark Workers (Heterogéneos):** Nodos trabajadores que ejecutan las tareas. Se configuran como "ligeros" y "pesados" para optimizar el uso de recursos según la carga de trabajo.
-   **History Server:** Almacena y muestra la interfaz de usuario (UI) de aplicaciones Spark ya finalizadas, crucial para el análisis post-ejecución y la depuración.
-   **Jupyter Lab:** Entorno de desarrollo interactivo. Se utiliza para prototipar, explorar datos y depurar el código PySpark. **No actúa como driver en producción.**
-   **Submit Node:** Contenedor ligero diseñado exclusivamente para lanzar aplicaciones Spark en el clúster mediante el comando `spark-submit`, separando el entorno de desarrollo del de ejecución.

## Características Clave

-   **Entorno Reproducible y Portátil:** Gracias a la contenerización con Docker, el entorno puede ser replicado exactamente en cualquier máquina con Docker instalado.
-   **Arquitectura Escalable y Modular:** El uso de plantillas YAML y un archivo `.env` permite ajustar fácilmente el número de workers y sus recursos (CPU, memoria) sin modificar el archivo de orquestación.
-   **Separación de Responsabilidades:** Se distingue claramente entre el entorno de desarrollo (Jupyter Lab) y el de ejecución (Submit Node), una práctica estándar en la industria.
-   **Observabilidad Completa:** Se exponen las UIs del Spark Master y del History Server para monitorear en tiempo real y analizar ejecuciones pasadas.

## Requisitos Previos

-   [Docker](https://www.docker.com/get-started/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Configuración y Ejecución

Sigue estos pasos para poner en marcha el entorno de análisis de datos.

1.  **Clonar el Repositorio**
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2.  **Configurar Variables de Entorno**
    Copia el archivo de plantilla `.env.example` a `.env` y ajústalo según los recursos de tu máquina.
    ```bash
    cp .env.example .env
    ```
    Edita el archivo `.env` para definir el número de réplicas y los recursos para los workers:
    ```env
    LIGHT_REPLICAS=2
    LIGHT_MEMORY=2g
    LIGHT_CORES=1

    HEAVY_REPLICAS=1
    HEAVY_MEMORY=4g
    HEAVY_CORES=2
    ```

3.  **Levantar el Entorno**
    Ejecuta el siguiente comando para construir las imágenes y levantar todos los contenedores en modo detached (segundo plano):
    ```bash
    docker-compose up --build -d
    ```

4.  **Acceder a las Interfaces**
    Una vez que los contenedores estén en ejecución, puedes acceder a las siguientes herramientas:
    -   **Jupyter Lab:** `http://localhost:8888`
    -   **Spark Master UI:** `http://localhost:8080`
    -   **History Server UI:** `http://localhost:18080`

## Estructura del Proyecto

```
.
├── data/                     # Directorio para archivos de datos de entrada (CSV).
├── docker/                   # Contiene los Dockerfiles para las imágenes.
│   ├── Dockerfile            # Dockerfile para Spark, Workers, etc.
│   └── Dockerfile.jupyter    # Dockerfile específico para Jupyter Lab.
│   └── requirements.txt      # Requerimientos para instalar desde Dockerfile.
├── spark-events/             # Directorio para los eventos de Spark (usado por el History Server).
├── src/                      # Directorio para notebooks y scripts de PySpark.
│   ├── procesamiento_etl.ipynb
│   └── etl_job.py
├── .env                      # Archivo de configuración de variables de entorno.
├── .env.example              # Plantilla para el archivo .env.
├── docker-compose.yml        # Archivo de orquestación de los contenedores.
└── README.md                 # Este archivo.
```

## Guía de Uso

### 1. Desarrollo Interactivo (Jupyter Lab)

Accede a `http://localhost:8888` para abrir Jupyter Lab. Desde aquí, puedes:
- Crear y ejecutar notebooks (`.ipynb`) para explorar los datos en `./data`.
- Prototipar y depurar tu lógica de ETL de forma interactiva.
- El notebook se conectará al clúster Spark (`spark://spark-master:7077`) para distribuir las tareas.

### 2. Ejecución en Producción (`spark-submit`)

Una forma alternativa de convertir el `ipynb` a un `py` si no es usando la interfaz gráfica de Jupyter, es desde la terminal, posicionado en el directorio del notebook:

```bash
jupyter nbconvert --to python procesamiento_etl.ipynb
```

Cuando tu lógica esté lista, guárdala como un script de Python (ej. `src/procesamiento_etl.py`). Luego, lánzala al clúster de forma robusta usando el `submit-node`.

Desde tu terminal local, ejecuta el siguiente comando:

```bash
docker-compose exec submit-node spark-submit \
  --master spark://spark-master:7077 \
  --name "Produccion-ETL-Ventas" \
  /home/jupyter/notebooks/procesamiento_etl.py
```

Este comando ejecutará el script dentro del contenedor `submit-node`, que a su vez enviará la aplicación al clúster Spark para su ejecución distribuida.

## Solución de Problemas (Troubleshooting)

### La UI de la Aplicación Spark no es accesible desde el Spark Master

Si al hacer clic en una aplicación en ejecución en `http://localhost:8080` la UI del driver no carga, es un problema de configuración de red.

**Solución:**
Asegúrate de que en el código de tu script Python (o notebook) la `SparkSession` esté configurada para ser accesible externamente:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MiApp") \
    .master("spark://spark-master:7077") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .getOrCreate()
```

Además, verifica que tu `docker-compose.yml` tenga la configuración correcta en el servicio `jupyter-lab`:
```yaml
environment:
  - SPARK_DRIVER_HOST=host.docker.internal
```


## Autores

-   **[Antonella Capadona](https://github.com/Resnick7)**
-   **[Matías Collado](https://github.com/MatiasColladoCA)**