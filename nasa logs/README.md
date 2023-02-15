Cargamos el archivo `access_log_Jul95` como archivo de texto utilizando expresiones regulares

Antes de nada, importamos las funciones de spark.sql (en spark-shell no hace falta)
```scala
import org.apache.spark.sql.functions._
```

```scala
val logs = spark.read.text("file:///C:/Users/didac.blanco/Documents/recursos/BIG DATA/repo ejercicios/nasa logs/logs")
```
Esta carpeta no existe en git debido al peso de los archivos

realizamos la extracción mediante regex:
```scala
val regex = "^([^ ]+) - - \\[(\\d{2}/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2}).*?\\] \"(.*?) (.*?)(HTTP/.*?) *?\" (.+?) (.*+)"
val df = logs.select(
    regexp_extract($"value", regex, 1).alias("host"),
    regexp_extract($"value", regex, 2).alias("date"),
    regexp_extract($"value", regex, 3).alias("method"),
    regexp_extract($"value", regex, 4).alias("resource"),
    regexp_extract($"value", regex, 5).alias("protocol"),
    regexp_extract($"value", regex, 6).alias("status"),
    regexp_extract($"value", regex, 7).alias("size")
)
```
```scala
val dfWithMonth = df.withColumn("month", regexp_extract($"date", "\\d{2}/(\\w{3})/\\d{4}:\\d{2}:\\d{2}:\\d{2}", 1))

val monthNumber: String => Int = {
    case "Jan" => 1
    case "Feb" => 2
    case "Mar" => 3
    case "Apr" => 4
    case "May" => 5
    case "Jun" => 6
    case "Jul" => 7
    case "Aug" => 8
    case "Sep" => 9
    case "Oct" => 10
    case "Nov" => 11
    case "Dec" => 12
    case _ => 0
  }
val monthToNumber = udf(monthNumber)
val dfWithMonthNumber = dfWithMonth.withColumn("monthNumber", monthToNumber($"month"))
dfWithMonthNumber.show()
val dfWithDay = dfWithMonthNumber.withColumn("day", regexp_extract($"date", "^(\\d{2})/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2}", 1))
```

- ¿Cuáles son los distintos protocolos web utilizados? Agrúpalos.
```scala
val groupedProtocols = df.select("protocol").groupBy("protocol").agg(count("*").alias("count"))
groupedProtocols.show(truncate=false)
```
```
+--------------------+-------+
|            protocol|  count|
+--------------------+-------+
|                    |   4884|
|           HTTP/V1.0|    279|
|            HTTP/1.0|3455200|
|HTTP/1.0From:  <b...|   1235|
|HTTP/1.0 200 OKDa...|      2|
|              HTTP/*|     13|
+--------------------+-------+
```
- ¿Cuáles son los códigos de estado más comunes en la web? Agrúpalos y ordénalos 
para ver cuál es el más común.
```scala
val groupedStatus = df.select("status").groupBy("status").agg(count("*").alias("count")).orderBy("count")
groupedStatus.show()
```
```
+------+-------+
|status|  count|
+------+-------+
|   501|     41|
|   500|     65|
|   403|    225|
|      |   4884|
|   404|  20700|
|   302|  73030|
|   304| 266773|
|   200|3095895|
+------+-------+
```
- ¿Y los métodos de petición (verbos) más utilizados?
```scala
val groupedMethods = df.select("method").groupBy("method").agg(count("*").alias("count")).orderBy("count")
groupedMethods.show()
```
```
+------+-------+
|method|  count|
+------+-------+
|  POST|    222|
|      |   4884|
|  HEAD|   7917|
|   GET|3448590|
+------+-------+
```
- ¿Qué recurso tuvo la mayor transferencia de bytes de la página web?
```scala
val totalBytes = df.groupBy("resource").agg(sum("size").alias("total_bytes")).orderBy(desc("total_bytes"))
totalBytes.show(1, truncate=false)
```
```
+--------------------------------------------------+-------------+
|resource                                          |total_bytes  |
+--------------------------------------------------+-------------+
|/shuttle/missions/sts-71/movies/sts-71-launch.mpg |3.194115706E9|
+--------------------------------------------------+-------------+
```
- Además, queremos saber que recurso de nuestra web es el que más tráfico recibe. Es 
decir, el recurso con más registros en nuestro log.
```scala
val resourceCount = df.groupBy("resource").agg(count("*").alias("count")).orderBy(desc("count"))
resourceCount.show(1,false)
```
```
+---------------------------+------+
|resource                   |count |
+---------------------------+------+
|/images/NASA-logosmall.gif |208362|
+---------------------------+------+
```
- ¿Qué días la web recibió más tráfico?

Como todos son del mismo mes, solo comparamos días:
```scala
val dayCount = dfWithDay.select($"day",$"monthNumber".alias("month")).groupBy("day","month").agg(count("*").alias("count")).orderBy(desc("count"))
dayCount.show()
```
```
+---+-----+------+
|day|month| count|
+---+-----+------+
| 13|    7|134134|
| 06|    7|100836|
| 05|    7| 94446|
| 12|    7| 92398|
| 31|    8| 90035|
| 03|    7| 89508|
| 07|    7| 87140|
| 14|    7| 83944|
| 30|    8| 80554|
| 11|    7| 80328|
| 17|    7| 74876|
| 10|    7| 72730|
| 19|    7| 72599|
| 04|    7| 70369|
| 29|    8| 67859|
| 20|    7| 66489|
| 01|    7| 64557|
| 21|    7| 64499|
| 24|    7| 64150|
| 18|    7| 64100|
+---+-----+------+
```
- ¿Cuáles son los hosts más frecuentes?
```scala
val hostCount = df.select("host").groupBy("host").agg(count("*").alias("count")).orderBy(desc("count"))
hostCount.show()
```
```
+--------------------+-----+
|                host|count|
+--------------------+-----+
|piweba3y.prodigy.com|21988|
|piweba4y.prodigy.com|16437|
|piweba1y.prodigy.com|12825|
|  edams.ksc.nasa.gov|11962|
|        163.206.89.4| 9697|
|         news.ti.com| 8161|
|www-d1.proxy.aol.com| 8047|
|  alyssa.prodigy.com| 8037|
| siltb10.orl.mmc.com| 7573|
|www-a2.proxy.aol.com| 7516|
|www-b2.proxy.aol.com| 7266|
|piweba2y.prodigy.com| 7246|
|www-b3.proxy.aol.com| 7218|
|www-d4.proxy.aol.com| 7211|
|www-b5.proxy.aol.com| 7080|
|www-d2.proxy.aol.com| 6984|
|www-b4.proxy.aol.com| 6972|
|www-d3.proxy.aol.com| 6895|
|    webgate1.mot.com| 6749|
|  e659229.boeing.com| 6720|
+--------------------+-----+
```
- ¿A qué horas se produce el mayor número de tráfico en la web?
```scala
val hourCount = df.select(regexp_extract($"date", "^\\d{2}/\\w{3}/\\d{4}:(\\d{2}):\\d{2}:\\d{2}", 1).alias("hour")).groupBy("hour").agg(count("*").alias("count")).orderBy(desc("count"))
hourCount.show(1)
```
```
+----+------+
|hour| count|
+----+------+
|  15|230373|
+----+------+
```
- ¿Cuál es el número de errores 404 que ha habido cada día?
```scala
val day404Count = dfWithDay.select($"day",$"monthNumber".alias("month")).filter("status = 404").groupBy("day","month").agg(count("*").alias("count")).orderBy(desc("count"))
day404Count.show(62)
```
```df
+---+-----+-----+
|day|month|count|
+---+-----+-----+
| 19|    7|  636|
| 06|    7|  633|
| 07|    7|  568|
| 30|    8|  568|
| 13|    7|  531|
| 07|    8|  526|
| 31|    8|  525|
| 05|    7|  492|
| 03|    7|  473|
| 11|    7|  470|
| 12|    7|  466|
| 18|    7|  465|
| 25|    7|  459|
| 20|    7|  427|
| 24|    8|  419|
| 25|    8|  414|
| 29|    8|  411|
| 14|    7|  408|
| 28|    8|  406|
| 17|    7|  404|
| 10|    7|  392|
| 08|    8|  386|
| 06|    8|  371|
| 27|    8|  370|
| 26|    8|  362|
| 04|    7|  355|
| 04|    8|  343|
| 09|    7|  342|
| 23|    8|  338|
| 27|    7|  333|
| 21|    7|  332|
| 26|    7|  324|
| 24|    7|  324|
| 15|    8|  322|
| 01|    7|  315|
| 10|    8|  312|
| 20|    8|  312|
| 21|    8|  303|
| 08|    7|  302|
| 03|    8|  300|
| 02|    7|  291|
| 22|    8|  284|
| 14|    8|  283|
| 09|    8|  277|
| 17|    8|  267|
| 11|    8|  260|
| 16|    8|  257|
| 16|    7|  256|
| 15|    7|  253|
| 18|    8|  247|
| 01|    8|  242|
| 05|    8|  232|
| 23|    7|  230|
| 13|    8|  214|
| 19|    8|  203|
| 12|    8|  191|
| 22|    7|  181|
| 28|    7|   93|
+---+-----+-----+
```