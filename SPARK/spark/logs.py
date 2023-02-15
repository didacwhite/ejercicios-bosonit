logs = sc.textFile("C:\\Users\\didac.blanco\\Desktop\\BIT\\data\\weblogs")
idRDD = logs.map(lambda line: (line.split(" ")[2], 1))
sumRDD = idRDD.reduceByKey(lambda x, y: x+y)