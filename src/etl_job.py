#!/usr/bin/env python
# coding: utf-8

# # Preparación de Entorno

# In[1]:


# procesamiento_etl.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, desc
from pyspark.sql.types import FloatType
import os

# --- 1. Preparar el entorno y cargar datos ---
print("==================================================")
print("PASO 1: PREPARAR ENTORNO Y CARGAR DATOS")
print("==================================================")

# Leer la URL del master desde la variable de entorno
# master_url = os.getenv("SPARK_MASTER_URL", "local[*]")

spark = SparkSession.builder \
    .appName("EcommerceAnalysis") \
    .master("spark://spark-master:7077") \
    .config("spark.ui.port", "4041") \
    .getOrCreate()

spark.sparkContext.master
spark.sparkContext.uiWebUrl

print("Sesión de Spark creada exitosamente.")

# c. Cargar el archivo CSV en un DataFrame
# Asumimos que el archivo está en la ruta mapeada por el volumen
file_path = "/opt/spark/data/e-commerce_orders.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)
df = spark.read.option("delimiter", ";").csv(file_path, header=True, inferSchema=True)

print(f"Archivo '{file_path}' cargado.")
print(f"Esquema inferido:")
df.printSchema()
print("\nPrimeras 5 filas del DataFrame original:")
df.show(5)


# # Exploración y Limpieza

# In[2]:


# --- 2. Exploración y limpieza ---
print("\n\n==================================================")
print("PASO 2: EXPLORACIÓN Y LIMPIEZA")
print("==================================================")

# a. Visualizar las primeras filas (ya hecho arriba, pero podemos repetirlo para seguir la estructura)
print("Visualizando las primeras filas para exploración inicial:")
df.show(5)


# # validar y Eliminar Registros Nulos

# In[3]:


# b. Validar y eliminar registros nulos
print("Contando registros nulos por columna antes de la limpieza:")
from pyspark.sql.functions import isnan, when, count
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

# Eliminar filas con cualquier valor nulo
df_clean = df.na.drop()
print(f"Registros antes de la limpieza: {df.count()}")
print(f"Registros después de eliminar nulos: {df_clean.count()}")

# c. Asegurar que los tipos de dato sean correctos
# Vamos a forzar el tipo de 'price' a FloatType para asegurar la precisión
df_clean = df_clean.withColumn("price", col("price").cast(FloatType()))
print("Asegurando que la columna 'price' sea de tipo FloatType.")
print("Nuevo esquema:")
df_clean.printSchema()


# # Transformación y Metricas

# In[4]:


# --- 3. Transformaciones y métricas ---
print("\n\n==================================================")
print("PASO 3: TRANSFORMACIONES Y MÉTRICAS")
print("==================================================")

# a. Calcular el monto total y promedio de ventas
sales_metrics_df = df_clean.agg(
    sum("price").alias("Monto_Total_Ventas"),
    avg("price").alias("Precio_Promedio_Venta")
)

# Mostrar en consola
sales_metrics_row = sales_metrics_df.collect()[0]
print("--- Métricas Generales de Ventas ---")
print(f"Monto Total de Ventas: {sales_metrics_row['Monto_Total_Ventas']:.2f}")
print(f"Precio Promedio de Venta: {sales_metrics_row['Precio_Promedio_Venta']:.2f}")


# b. Contar la cantidad de pedidos por estado
print("\n--- Cantidad de Pedidos por Estado ---")
orders_by_status = df_clean.groupBy("Status").count().orderBy(desc("count"))
orders_by_status.show()


# c. Obtener el top 3 de clientes que más dinero gastaron
print("\n--- Top 3 Clientes por Gasto Total ---")
top_customers = df_clean.groupBy("customer_id") \
    .agg(sum("price").alias("Total_Gastado")) \
    .orderBy(desc("Total_Gastado")) \
    .limit(3)
top_customers.show()

# Opcional: Guardar los resultados en CSV como ya lo hacías
# Esto demuestra la parte "Load" del ETL
print("\n\n==================================================")
print("PASO 4: CARGA DE RESULTADOS (LOAD)")
print("==================================================")
print("Guardando resultados en el directorio /opt/spark/data/resultados/...")


# In[5]:


# Escritura en CSV

# sales_metrics_df.write.csv("/opt/spark/data/resultados/monto_promedio", mode="overwrite", header=True)
# orders_by_status.write.csv("/opt/spark/data/resultados/pedidos_por_estado", mode="overwrite", header=True)
# top_customers.write.csv("/opt/spark/data/resultados/top_clientes", mode="overwrite", header=True)
# # Spark divide el dataset en particiones pero con coalesce reduce a una partición. No es recomendado en Spark porque los dataframes son generalmente cientos de veces mas grandes y afecta el rendimiento
# df_clean.coalesce(1).write.csv("/opt/spark/data/resultados/limpio", mode="overwrite", header=True)

# print("Proceso ETL completado exitosamente.")


# In[6]:


#Cerramos explícitamente la sesión
spark.stop()

