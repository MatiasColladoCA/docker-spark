[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/big-data-europe/Lobby)
[![Build Status](https://travis-ci.org/big-data-europe/docker-spark.svg?branch=master)](https://travis-ci.org/big-data-europe/docker-spark)
[![Twitter](https://img.shields.io/twitter/follow/BigData_Europe.svg?style=social)](https://twitter.com/BigData_Europe)
# Spark docker

Docker images to:
* Setup a standalone [Apache Spark](https://spark.apache.org/) cluster running one Spark Master and multiple Spark workers
* Build Spark applications in Java, Scala or Python to run on a Spark cluster

<details open>
<summary>Currently supported versions:</summary>

* Spark 3.3.0 for Hadoop 3.3 with OpenJDK 8 and Scala 2.12
* Spark 3.2.1 for Hadoop 3.2 with OpenJDK 8 and Scala 2.12
* Spark 3.2.0 for Hadoop 3.2 with OpenJDK 8 and Scala 2.12
* Spark 3.1.2 for Hadoop 3.2 with OpenJDK 8 and Scala 2.12
* Spark 3.1.1 for Hadoop 3.2 with OpenJDK 8 and Scala 2.12
* Spark 3.1.1 for Hadoop 3.2 with OpenJDK 11 and Scala 2.12
* Spark 3.0.2 for Hadoop 3.2 with OpenJDK 8 and Scala 2.12
* Spark 3.0.1 for Hadoop 3.2 with OpenJDK 8 and Scala 2.12
* Spark 3.0.0 for Hadoop 3.2 with OpenJDK 11 and Scala 2.12
* Spark 3.0.0 for Hadoop 3.2 with OpenJDK 8 and Scala 2.12
* Spark 2.4.5 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.4.4 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.4.3 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.4.1 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.4.0 for Hadoop 2.8 with OpenJDK 8 and Scala 2.12
* Spark 2.4.0 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.3.2 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.3.1 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.3.1 for Hadoop 2.8 with OpenJDK 8
* Spark 2.3.0 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.2.2 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.2.1 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.2.0 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.1.3 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.1.2 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.1.1 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.1.0 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.0.2 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.0.1 for Hadoop 2.7+ with OpenJDK 8
* Spark 2.0.0 for Hadoop 2.7+ with Hive support and OpenJDK 8
* Spark 2.0.0 for Hadoop 2.7+ with Hive support and OpenJDK 7
* Spark 1.6.2 for Hadoop 2.6 and later
* Spark 1.5.1 for Hadoop 2.6 and later

</details>

## Using Docker Compose

Add the following services to your `docker-compose.yml` to integrate a Spark master and Spark worker in [your BDE pipeline](https://github.com/big-data-europe/app-bde-pipeline):
```yml
version: '3'
services:
  spark-master:
    image: bde2020/spark-master:3.3.0-hadoop3.3
    container_name: spark-master
    ports:
      - "8080:8080"
      - "7077:7077"
    environment:
      - INIT_DAEMON_STEP=setup_spark
  spark-worker-1:
    image: bde2020/spark-worker:3.3.0-hadoop3.3
    container_name: spark-worker-1
    depends_on:
      - spark-master
    ports:
      - "8081:8081"
    environment:
      - "SPARK_MASTER=spark://spark-master:7077"
  spark-worker-2:
    image: bde2020/spark-worker:3.3.0-hadoop3.3
    container_name: spark-worker-2
    depends_on:
      - spark-master
    ports:
      - "8082:8081"
    environment:
      - "SPARK_MASTER=spark://spark-master:7077"
  spark-history-server:
      image: bde2020/spark-history-server:3.3.0-hadoop3.3
      container_name: spark-history-server
      depends_on:
        - spark-master
      ports:
        - "18081:18081"
      volumes:
        - /tmp/spark-events-local:/tmp/spark-events
```
Make sure to fill in the `INIT_DAEMON_STEP` as configured in your pipeline.

## Running Docker containers without the init daemon
### Spark Master
To start a Spark master:

    docker run --name spark-master -h spark-master -d bde2020/spark-master:3.3.0-hadoop3.3

### Spark Worker
To start a Spark worker:

    docker run --name spark-worker-1 --link spark-master:spark-master -d bde2020/spark-worker:3.3.0-hadoop3.3

## Launch a Spark application
Building and running your Spark application on top of the Spark cluster is as simple as extending a template Docker image. Check the template's README for further documentation.
* [Maven template](template/maven)
* [Python template](template/python)
* [Sbt template](template/sbt)

## Kubernetes deployment
The BDE Spark images can also be used in a Kubernetes enviroment.

To deploy a simple Spark standalone cluster issue

`kubectl apply -f https://raw.githubusercontent.com/big-data-europe/docker-spark/master/k8s-spark-cluster.yaml`

This will setup a Spark standalone cluster with one master and a worker on every available node using the default namespace and resources. The master is reachable in the same namespace at `spark://spark-master:7077`.
It will also setup a headless service so spark clients can be reachable from the workers using hostname `spark-client`.

Then to use `spark-shell` issue

`kubectl run spark-base --rm -it --labels="app=spark-client" --image bde2020/spark-base:3.3.0-hadoop3.3 -- bash ./spark/bin/spark-shell --master spark://spark-master:7077 --conf spark.driver.host=spark-client`

To use `spark-submit` issue for example

`kubectl run spark-base --rm -it --labels="app=spark-client" --image bde2020/spark-base:3.3.0-hadoop3.3 -- bash ./spark/bin/spark-submit --class CLASS_TO_RUN --master spark://spark-master:7077 --deploy-mode client --conf spark.driver.host=spark-client URL_TO_YOUR_APP`

You can use your own image packed with Spark and your application but when deployed it must be reachable from the workers.
One way to achieve this is by creating a headless service for your pod and then use `--conf spark.driver.host=YOUR_HEADLESS_SERVICE` whenever you submit your application.




# USAR

sudo docker exec -it spark-client \
  /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    /opt/spark/data/procesamiento_etl.py


Ejecutar el mismo script midiendo tiempo de ejecución (puedo comentar un worker en el docker compose)

sudo time docker exec spark-client \
  /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    /opt/spark/data/procesamiento_etl.py


Opción B: Ver los logs en tiempo real (muy recomendado para depurar)

Si quieres ver la salida del script mientras se ejecuta, puedes "seguir" los logs.

En una terminal, lanza el script:

`docker exec -it spark-client spark-submit --master spark://spark-master:7077 /opt/spark/data/procesamiento_etl.py`

Inmediatamente después, abre una segunda terminal y ejecuta este comando:
bash

`docker logs -f spark-client`

El flag -f (de follow) te mostrará los logs en tiempo real, a medida que se generan. Verás los print() y los show() apareciendo en tu pantalla. Puedes detenerlo con Ctrl+C.

















Análisis de tu Flujo Actual (docker-compose up + docker exec)
Este enfoque tiene varias fortalezas que lo hacen una práctica sólida:

Separación de Responsabilidades (Separation of Concerns):
docker-compose up -d: Su única responsabilidad es levantar y mantener la infraestructura (el clúster de Spark, la red, los volúmenes). Es un comando idempotente y declarativo.
docker exec ... spark-submit: Su única responsabilidad es ejecutar la lógica de negocio (tu aplicación ETL) sobre esa infraestructura ya existente.
Esta separación es un principio de diseño de software y de sistemas excelente. Te permite levantar el clúster una vez y ejecutar el trabajo múltiples veces con diferentes parámetros si es necesario, sin tener que reiniciar toda la infraestructura.
Claridad y Control:
Tienes control total y explícito sobre cuándo se ejecuta tu aplicación. No hay "magia" ni ejecuciones automáticas inesperadas.
Es ideal para depuración. Puedes levantar el clúster, entrar en el contenedor spark-client con bash, inspeccionar archivos, y luego ejecutar el spark-submit manualmente cuando estés listo.
Flexibilidad:
Puedes modificar fácilmente los parámetros de spark-submit en cada ejecución (por ejemplo, cambiar la memoria del driver, añadir --conf, etc.) sin tener que modificar el docker-compose.yml. Esto es mucho más ágil para el desarrollo.
Estándar de la Industria para Desarrollo:
Este patrón de "levantar infraestructura + ejecutar tarea" es el estándar de facto para muchos entornos de desarrollo local. Es exactamente como un desarrollador interactuaría con un clúster remoto vía SSH, pero encapsulado en Docker.
Conclusión del análisis: Para un entorno de desarrollo local, pruebas y depuración, tu método no solo es profesional, sino que es preferible a alternativas más automatizadas que ocultarían la ejecución.


















PROMPT PARA IA


Claro, aquí tienes un prompt detallado y estructurado que puedes usar para que una IA (como GPT-4, Claude, etc.) comprenda a fondo tu proyecto, su arquitectura y el camino que seguiste para llegar a la solución.

---

### Prompt para la IA

**Rol:** Actúa como un Arquitecto de Datos y DevOps senior con amplia experiencia en Apache Spark y Docker.

**Objetivo:** Necesito que comprendas en detalle un proyecto de procesamiento de datos que he construido. Analiza la estructura, la configuración, la lógica de la aplicación y, lo más importante, los problemas de configuración que se resolvieron para llegar a un clúster funcional. Tu comprensión debe ser lo suficientemente profunda como para poder responder preguntas, sugerir mejoras o generar documentación técnica sobre este proyecto.

---

#### **1. Resumen del Proyecto**

He creado un entorno de desarrollo local para un pipeline ETL (Extraer, Transformar, Cargar) utilizando Apache Spark. Todo el entorno está orquestado con Docker Compose y se ejecuta en un clúster de Spark con una arquitectura master-worker, todo contenido en mi máquina local.

#### **2. Estructura del Proyecto**

La estructura de archivos y directorios es la siguiente:

```
mi-proyecto-spark/
├── docker-compose.yml
├── Dockerfile
├── procesamiento_etl.py
├── data/
│   ├── e-commerce_orders.csv  # Datos de entrada
│   └── resultados/            # Directorio de salida (creado por la app)
│       ├── pedidos_por_estado/
│       ├── top_clientes/
│       └── estadisticas_ventas/
└── spark-events/              # Logs para el History Server
```

#### **3. Detalles de los Componentes Clave**

**a) `docker-compose.yml`**
Este archivo orquesta 5 servicios en una red Docker aislada (`spark-net`):

*   **`spark-master`**: Contenedor que ejecuta el proceso master de Spark. **Importante**: Inicialmente usaba una imagen diferente (`apache/spark-py`), pero se corrigió para usar la misma imagen que los workers (construida localmente) para garantizar la compatibilidad de versiones.
*   **`spark-worker-1` y `spark-worker-2`**: Dos contenedores que actúan como workers. Se les asignan 2 cores y 2GB de RAM cada uno. **Corrección crítica aplicada**: Se añadió la variable de entorno `SPARK_WORKER_DIR=/tmp` para resolver un error `AccessDeniedException`, ya que el usuario del contenedor no podía escribir en el directorio por defecto de Spark.
*   **`spark-client`**: Un contenedor "utilitario" desde donde se envían las aplicaciones al clúster usando `spark-submit`. No ejecuta un worker, solo actúa como driver de la aplicación.
*   **`spark-history-server`**: Un servicio que lee los logs de eventos de Spark (`spark-events`) y proporciona una UI web en `http://localhost:18080` para inspeccionar aplicaciones que ya han finalizado.
*   **Volúmenes**:
    *   `./data:/opt/spark/data`: Mapea los datos de entrada y salida entre mi máquina local y los contenedores.
    *   `./spark-events:/tmp/spark-events`: Mapea el directorio de logs de eventos para el History Server.

**b) `Dockerfile`**
Define una imagen Docker personalizada basada en `apache/spark:v3.5.0`. Utiliza `ONBUILD` para instalar automáticamente las dependencias de Python (`requirements.txt`) y copiar el código de la aplicación al contenedor. Esto asegura que el master, los workers y el cliente tengan un entorno idéntico.

**c) `procesamiento_etl.py`**
Esta es la aplicación PySpark que realiza el ETL:
1.  **Extract**: Lee un archivo CSV (`e-commerce_orders.csv`) desde el volumen compartido.
2.  **Transform**:
    *   Limpia los datos eliminando registros nulos.
    *   Corrige los tipos de datos (e.g., `Price` a `FloatType`).
    *   Realiza agregaciones: calcula estadísticas de ventas, cuenta pedidos por estado y encuentra el top 3 de clientes.
3.  **Load**:
    *   Imprime resultados intermedios en la consola (usando `print()` y `df.show()`). Esta salida va a los logs del contenedor `spark-client`.
    *   Escribe los resultados finales en formato CSV en el directorio `/opt/spark/data/resultados/`, que se refleja en mi máquina local.
    *   **Corrección aplicada**: Se eliminó la llamada explícita a `spark.stop()` para evitar que el SparkContext se cerrara antes de que las operaciones de escritura (que son "lazy") se completaran.

#### **4. El Viaje de Depuración (Problemas y Soluciones)**

Este es el contexto más importante para entender por qué la configuración final es como es:

1.  **Problema 1: Workers no se registraban.**
    *   **Síntoma**: La UI del Master en `localhost:8080` no mostraba workers. Las aplicaciones se quedaban en estado `WAITING`.
    *   **Causa Raíz**: Incompatibilidad de imágenes. El master usaba `apache/spark-py` y los workers usaban una imagen construida desde `apache/spark:v3.5.0`.
    *   **Solución**: Unificar todos los servicios de Spark (master, workers, client) para que usaran la misma imagen construida localmente (`build: .`).

2.  **Problema 2: Los workers fallaban al iniciar.**
    *   **Síntoma**: Los logs de los workers mostraban `java.nio.file.AccessDeniedException: /opt/spark/work`.
    *   **Causa Raíz**: El proceso de Spark dentro del contenedor se ejecutaba como un usuario no-root y no tenía permisos para crear su directorio de trabajo en `/opt/spark`.
    *   **Solución**: Añadir la variable de entorno `SPARK_WORKER_DIR=/tmp` a los workers para que usen un directorio con permisos de escritura.

3.  **Problema 3: La aplicación fallaba durante la escritura.**
    *   **Síntoma**: Los logs mostraban `Stage cancelled because SparkContext was shut down`.
    *   **Causa Raíz**: La llamada a `spark.stop()` al final del script cerraba el contexto inmediatamente, cancelando las tareas de escritura que Spark había planificado pero aún no ejecutado (evaluación perezosa).
    *   **Solución**: Eliminar la línea `spark.stop()` y dejar que Spark gestione el ciclo de vida del contexto hasta que todas las tareas se completen.

---

**Tarea:**
Basado en esta información completa, prepárate para:
*   Explicar el flujo de datos de extremo a extremo.
*   Justificar cada decisión de configuración en el `docker-compose.yml`.
*   Proponer posibles mejoras (ej: añadir más workers, cambiar el gestor de recursos, etc.).
*   Generar un archivo `README.md` para este proyecto.