# Databricks notebook source
STORAGE_ACCOUNT = 'aulafiaead'
CONTAINER = 'grupo7'
BLOB_STORAGE_KEY = 'QDKbVST0U3yAaEI4HN9DFwYTB3jGO6xb4Kk5r59UFYOzXrkrVLESZKmrKzPZ/eEsDLV8Fw5XxybA+ASt4EZ2zA=='

spark.conf.set(f"fs.azure.account.key.{STORAGE_ACCOUNT}.blob.core.windows.net", BLOB_STORAGE_KEY)

dfacidentes2022 = spark.read.format('csv').options(header='true', inferSchema='true', delimiter=';', encoding='ISO-8859-1').load(f'wasbs://{CONTAINER}@{STORAGE_ACCOUNT}.blob.core.windows.net/raw/acidentes2022.csv')

dfdatatran2022 = spark.read.format('csv').options(header='true', inferSchema='true', delimiter=';', encoding='ISO-8859-1').load(f'wasbs://{CONTAINER}@{STORAGE_ACCOUNT}.blob.core.windows.net/raw/datatran2022.csv')

# COMMAND ----------

dfacidentes2022.display()

# COMMAND ----------

dfacidentes2022.write.format('delta').option("encoding", "ISO-8859-1").mode('overwrite').saveAsTable('acidentes', path='/FileStore/tables/acidentes')

dfdatatran2022.write.format('delta').option("encoding", "ISO-8859-1").mode('overwrite').saveAsTable('datatran', path='/FileStore/tables/datatran')

# COMMAND ----------

display(dbutils.fs.ls("/FileStore/tables/"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM acidentes a right join datatran b on a.id = b.id
# MAGIC --SELECT count(*) FROM datatran

# COMMAND ----------

import pyspark.sql.functions as fn

dfacidentes = spark.read.format('delta').load('/FileStore/tables/acidentes')
dfdatatran = spark.read.format('delta').load('/FileStore/tables/datatran')

# COMMAND ----------

dfacidentes.display()

# COMMAND ----------

dfdatatran.display()

# COMMAND ----------

dfjoin = dfacidentes.join(dfdatatran, on="id", how="inner").select(dfacidentes.municipio, dfacidentes.data_inversa, dfacidentes.causa_acidente, dfacidentes.tipo_acidente)

# COMMAND ----------

dfjoin.count()

# COMMAND ----------

dfmunic = dfjoin.groupBy("municipio").count().orderBy("count", ascending=False)

# COMMAND ----------

dfmunic.display()

# COMMAND ----------

dfjoin.groupBy("tipo_acidente").count().agg("mortos").orderBy("count", ascending=False).display()
