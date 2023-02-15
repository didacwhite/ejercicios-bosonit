1. Dado un número entero, determine si es par o impar.

    ```Scala
    def esPar(num: Int): Boolean = {
      if (num % 2 == 0) {
        return true
      } else {
        return false
      }
    }

    scala> val prueba1 = 1
    prueba1: Int = 1

    scala> esPar(prueba1)
    res0: Boolean = false

    ```

2. Dado una lista de enteros, calcule la suma de todos los elementos en la lista.

    ```Scala
    scala> val lista = List(1, 2, 3, 4, 5)
    lista: List[Int] = List(1, 2, 3, 4, 5)

    scala> var sum = 0
    sum: Int = 0

    scala> lista.foreach(sum += _)

    scala> sum
    res2: Int = 15
    ```

3. Dada la cadena "Anita lava la tina", determine si es un palíndromo (es decir, si se lee igual al derecho y al revés).

    > Como la cadena ofrecida es solo palíndromo si no tenemos en cuenta los espacios, vamos a incluír a la función que creemos que primero elimine los espacios. De paso también nos aseguramos que obvie los signos de puntuación y que no sea sensible a mayúsculas

    ```Scala
    def esPalindromo(cadena: String): Boolean = {
      val cadenaSinEspacios = cadena.replaceAll("\\s+", "")
      val cadenaSinSignos = cadenaSinEspacios.replaceAll("[^a-zA-Z0-9]", "")
      val cadenaMinusculas = cadenaSinSignos.toLowerCase
      val cadenaInvertida = cadenaMinusculas.reverse
      if (cadenaMinusculas == cadenaInvertida) {
        return true
      } else {
        return false
      }
    }

    scala> println(esPalindromo("Anita lava la tina")) // imprime "true"
    true

    scala> println(esPalindromo("A Santa at NASA!")) // imprime "true"
    true

    scala> println(esPalindromo("hola mundo"))
    false

    ```

4. Dado una lista de cadenas, devuelva una nueva lista que contenga solo las cadenas únicas (sin duplicados).

    ```Scala
    val lista1 = List("perro", "gato", "conejo", "perro", "pájaro", "gato")
    val lista2 = List("manzana", "pera", "naranja", "kiwi", "manzana", "plátano", "pera", "naranja")

    def eliminarDuplicados(lista: List[String]): List[String] = {
      return lista.toSet.toList
    }

    scala> println(eliminarDuplicados(lista1))
    List(perro, gato, conejo, pájaro)

    scala> println(eliminarDuplicados(lista2))
    List(manzana, pera, kiwi, plátano, naranja)
    ```

5. Dado un número entero, calcule su factorial (es decir, el producto de todos los números enteros desde 1 hasta el número dado).

    ```Scala
    def factorial(n: Int): Int = {
      if (n <= 1) 1
      else n * factorial(n - 1)
    }
    scala> factorial(3)
    res9: Int = 6

    scala> factorial(10)
    res10: Int = 3628800
    ```

6. Dado una lista de números, devuelva el número máximo de la lista.

    ```Scala
    scala> println(lista.max)
    5
    ```

7. Dado una lista de números, devuelva el número mínimo de la lista.

    ```Scala
    scala> println(lista.min)
    1
    ```

8. Dado una cadena, devuelva una nueva cadena en la que se hayan eliminado todas las vocales.

    ```Scala
    val input = "Hola, mundo!"
    val output = input.replaceAll("[aeiou]", "")
    output: String = Hl, mnd!
    ```

9.  Dado una lista de números, devuelva una nueva lista con los números ordenados de menor a mayor.

    ```Scala
    val lista = List(3, 5, 7, 12, 9, 2)

    val sortedNumbers = lista.sortWith(_ < _)

    scala> println(sortedNumbers)
    List(2, 3, 5, 7, 9, 12)
    ```

10. Define una clase Persona que tenga los atributos nombre y edad, y un método esMayorEdad que devuelva true si la persona tiene 18 años o más y false en caso contrario. Luego, crea una instancia de la clase Persona y usa el método esMayorEdad para verificar si la persona es mayor de edad. 

    ```Scala
    class Persona(val nombre: String, val edad: Int) {
      def esMayorEdad(): Boolean = {
        return edad >= 18
      }
    }
    val persona = new Persona("Juan", 25)
    
    scala> println(persona.esMayorEdad())
    true

    ```