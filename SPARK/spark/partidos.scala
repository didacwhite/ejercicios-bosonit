val sqlContext = spark.sqlContext
import sqlContext.implicits._
import org.apache.spark.sql.Row
import org.apache.spark.sql.types.{StructType,StructField,StringType}
val filePath = "C:\\Users\\didac.blanco\\Desktop\\BIT\\data\\DataSetPartidos.txt"
var data=sc.textFile(filePath)
val schemaString = "idPartido::temporada::jornada::EquipoLocal::EquipoVisitante::golesLocal::golesVisitante::fecha::timestamp"
val schema = StructType(schemaString.split("::").map(fieldName => StructField(fieldName, StringType, true)))
val rows = data.map(_.split("::")).map(p=>Row(p(0),p(1),p(2),p(3).toString,p(4).toString,p(5).toString,p(6).toString,p(7),p(8).trim))

val dfPartidos = sqlContext.createDataFrame(rows, schema)
dfPartidos.createOrReplaceTempView("partidos")

val results = sqlContext.sql("SELECT temporada, jornada FROM partidos")
results.show()