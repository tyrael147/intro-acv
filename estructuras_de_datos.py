# %% [markdown]
# # Introducción
# En esta primera sección introductoria aprenderemos los conceptos básicos de variables y tipos de datos en Python.
# Para ejecutar este archivo correctamente, asegúrate de instalar las dependencias necesarias ejecutando el siguiente codigo.

# %%
!pip install brightway25

# %% [markdown]
#
# Este cuaderno de Jupyter (`*.ipynb`) nos permite ejecutar código celda por celda de forma interactiva, a diferencia de los archivos Python (con extensión .py) donde el código se ejecuta en un solo paso ([más información aquí](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html)).
#

# %% [markdown]
# ## Variables
#
# Las variables son nombres simbólicos que apuntan a objetos en memoria.
# En otras palabras, están conectadas a un valor, que son los datos asociados a la variable respectiva.
# Las variables se pueden crear usando el operador de asignación (`=`).
#
# <div class="alert alert-block alert-info"><b>Consejo: </b>Ejecuta celdas con `Ctrl+Enter`, o ejecuta y avanza a la siguiente con `Shift+Enter`</div>
#
# <div class="alert alert-block alert-info"><b>Consejo: </b>Si no deseas ejecutar una línea, coméntala anteponiendo `#`</div>
#

# %%
# Esta línea es un comentario
# Asignamos un string a la variable 'message'
message = "¡Hola a todos!"
# Asignamos un entero a la variable 'number'
number = 42.0
print("El mensaje es: ", message)
print("El número es: ", number)

# %% [markdown]
# Podemos verificar los tipos de datos usando la función type(). Esta función devuelve la clase del objeto.

# %%
print("Tipo de 'message': ",type(message))
print("Tipo de 'number': ", type(number))

# %% [markdown]
# Tanto 'message' como 'number' tienen su propia dirección en la memoria del computador.
# Para acceder a esta dirección, podemos usar la función incorporada `id()`.
# Esta función devuelve la "identidad" de un objeto. Este `id` es un entero único que permanece constante durante la vida del intérprete.

# %%
id(message)

# %%
print('Dirección de "message": ', hex(id(message)))
print('Dirección de "number": ', hex(id(number)))

# %% [markdown]
# Si asignamos la variable 'message' a una nueva variable 'new_message', esta última apuntará a la dirección de los datos originales.

# %%
new_message = message # Reasignamos nuevamente
print('Dirección de "message": ', hex(id(message)))
print('Dirección de "new_message": ', hex(id(new_message)))


# %% [markdown]
# Al crear variables, debemos considerar ciertas reglas y convenciones.
# <div class="alert alert-block alert-warning"><b>Advertencia: </b>Los nombres solo pueden contener letras, números y guiones bajos. Pueden comenzar con letra o guión bajo, pero nunca con número</div>
#

# %%
1_message = "hola" # Esto no funciona

# %% [markdown]
# <div class="alert alert-block alert-warning"><b>Advertencia: </b>No se permiten espacios en los nombres.</div>
#

# %%
mi variable = 1 # Esto no funciona

# %%
mi_variable = 1 # Esto sí funciona

# %% [markdown]
# <div class="alert alert-block alert-warning"><b>Advertencia: </b>Existen palabras reservadas de Python que deben evitarse (ver aquí: https://docs.python.org/3/library/functions.html) </div>
#

# %%
# print = 12 # Esto debe evitarse
# print() # Esto no funcionaría

# %%
# from rich import print # arreglamos el error

# %%
print("hola mundo")

# %% [markdown]
# <div class="alert alert-block alert-info"><b>Consejo: </b>Usa nombres cortos pero descriptivos</div>
#

# %%
n="Juan" # No recomendado
nombre="Juan" # Mejor
longitud_del_nombre_de_la_persona = 23 # No recomendado
longitud_nombre = 23 # Mejor

# %%
print(longitud_nombre)

# %% [markdown]
# <div class="alert alert-block alert-danger"><b>¡Peligro!: </b>El error más común al programar son las faltas de tipográficas al llamar variables. Afortunadamente, Python ayuda a identificar estos errores</div>
#

# %%
mi_mensaje = "Este es mi mensaje"
print(mi_mnsaje) # Esto debería dar un NameError, 'mi_mensaje' no está definido por un error tipográfico.

# %% [markdown]
# # Tipos de datos básicos
# ## Cadenas de texto (Strings)
# Son secuencias de caracteres que se pueden crear usando comillas simples o dobles. Cualquier contenido dentro de comillas se considera una cadena.

# %%
from rich import print

# %%
print('Esto es una cadena')  
print("Esto también es una cadena")


# %% [markdown]
# Podemos incluir cualquier tipo de carácter en una cadena. Sin embargo, en algunos casos queremos dar un significado especial a un carácter o suprimir su significado.
# Para estas situaciones, usamos el carácter de escape `\` antes del carácter especial.

# %%
print("Esta es una comilla doble: \" ")

# %%
# Escapando comillas simples
print("Las comillas dobles (\") son importantes para construir cadenas")

# %%
print("Esta es la letra \t tabulador")

# %% [markdown]
# Existen otras secuencias de escape con significados especiales en Python:
#
# | Secuencia Escape  | 	Significado                 |
# |--------------------|-------------------------------|
# | \a               |	Carácter de campana ASCII (BEL) |
# | \b |	Carácter de retroceso ASCII (BS) |
# |\f |	Carácter de avance de página ASCII (FF)|
# |\n | Carácter de salto de línea ASCII (LF)|
# |\N{<nombre>} |	Carácter Unicode con <nombre> especificado|
# |\r | 	Carácter de retorno de carro ASCII (CR)|
# |\t 	| Tabulación horizontal ASCII (TAB)|
# |\uxxxx 	| Carácter Unicode con valor hexadecimal de 16 bits|
# |\Uxxxxxxxx 	| Carácter Unicode con valor hexadecimal de 32 bits|
# |\v | 	Tabulación vertical ASCII (VT)|
# |\ooo |	Carácter con valor octal|
# |\xhh 	| Carácter con valor hexadecimal|
#

# %%
print("Tendremos una nueva línea \ndespués de la línea inicial")  # Dos líneas

# %%
print("Esto introduce el \ttabulador en la cadena")  # Se introduce una tabulación

# %%
print("\x61")  # Hexadecimal

# %%
print("\N{White Smiling Face}")  # Unicode por nombre

# %%
happy = "\N{White Smiling Face}"

# %%
print("Porque yo soy...", happy)

# %% [markdown]
# Podemos usar comillas simples y dobles para crear cadenas que contengan comillas internas.

# %%
print("Y la policía dijo: '¡Deténgase allí, tonto!'")

# %%
print('Y la policía dijo: "¡Deténgase allí, tonto!"')

# %% [markdown]
# Podemos formatear cadenas insertando datos de variables usando f-strings (f de formato). Útil para crear cadenas complejas.

# %%
candidate = "Gustavo"
score = 100.2
print(f"El candidato {candidate} obtuvo una puntuación de: {score}")

# %%
print(f"Porque yo soy {happy}")

# %% [markdown]
# Podemos obtener la longitud de una cadena con `len` y acceder a caracteres con corchetes `[]`

# %%
my_string = 'Esta es mi increíble cadena'
print(len(my_string))
print(my_string[3])  # Acceder al carácter en índice 3

# %% [markdown]
# Los corchetes también sirven para rebanar cadenas, misma lógica que en listas.

# %%
print(my_string[6:])  # Desde índice 6 hasta el final

# %%
print(my_string[-9:])  # Desde la posición 9 contando desde el final

# %% [markdown]
# Podemos usar operadores `in` y `not in` para verificar contención

# %%
long_string = "Abel, Luis y María vinieron a la fiesta"
print("Luis" in long_string)
print("Roberta" in long_string)

# %% [markdown]
# Operadores como `+` y `*` permiten concatenación y repetición:

# %%
# Concatenación
first_string="La respuesta es "
second_string = "cuarenta y dos (42)"
third_string = "... Confía en mí"
answer = first_string + second_string + third_string + " !!!"
print(answer)

# %%
# Repetición
first_string  = "Y él simplemente dijo... "
second_string = "JA " * 6  # JA JA JA JA JA JA
repeated = first_string + second_string
print(repeated)

# %%
car = "esto"
type(car)

# %% [markdown]
# Los strings son objetos de clase `str` con métodos propios.
#
# example = "hola a mi pequeño mundo"
# example_version_2 = (example.title())
# print(example_version_2)

# %%
message = "¡Hola MUNDO!, Me siento avergonzado"
print(message)
print(message.title())  # Capitalizar cada palabra
print(message.upper())  # Mayúsculas
print(message.lower())  # Minúsculas
print(message.swapcase())  # Invertir mayúsculas/minúsculas
print(message.startswith("Hola"))  # Verificar inicio
print(message.startswith("hola"))

# %%
# Eliminar espacios en blanco o prefijos
message = "   https://helloworld.com   "
print(message.strip())  # Eliminar espacios

# %%
# Métodos encadenados
message = "   https://helloworld.com   "
print(message.strip().removeprefix('https://'))

# %%
# Reemplazar subcadenas
message = "BMW es una marca de vehículos"
print(message.replace("BMW", "VW"))

# %%
# Dividir cadenas usando separadores
message = "Augusto,Julia,Karl"
print(message.split(","))

# %%
# Unir elementos de una lista
message = "Augusto,Julia,Karl"
message_separated = message.split(",")
print(f"{happy}".join(message_separated))

# %% [markdown]
# ### Ejercicio:
# #### Tu software recibe mensajes con datos de clientes en formato incorrecto:
#
#     https://database.com/user/augustom,AugUSto Martin, 23, Approved,,
#     https://database.com/user/juliasch,JuLIA SchmidT, 67, rejected,,
#     https://database.com/user/kmarx,Karl Marx, 42, rejected,,
#
# #### Se necesita procesar en este formato:
#
#     message:  augustom,augustomartin,23,approved
#     message:  juliasch,juliaschmidt,67,rejected
#     message:  kmarx,karlmarx,42,rejected
#
# #### __Tarea__: Usar métodos de `str` para corregir los mensajes.

# %% [markdown]
# Completa el código


# %% [markdown]
# ## Números
# Enteros y flotantes. Operadores aritméticos: `+`, `-`, `*`, `/`, etc.

# %%
2 * 3 + 2  # Expresión que retorna 8

# %%
# Variables con números
pi = 3.1416
radio = 2
print(2 * pi * radio )

# %% [markdown]
# Operadores aritméticos:
# |Operador |	Nombre      |	Ejemplo|
# |---------|-------------|---------|
# |+ 	    |Suma         |	x + y 	|
# |- 	    |Resta        |	x - y   |
# |* 	    |Multiplicación |x * y |
# |/ 	    |División     |	x / y 	|
# |% 	    |Módulo       |	x % y 	|
# |** 	    |Exponenciación |	x ** |
# |// 	    |División entera |	x // y|

# %%
print('Suma: ', 2+3)
print('Resta: ',2-3)
print('Multiplicación: ',2*3)
print('División: ',2/3)
print('Módulo: ',10%3)
print('Exponenciación: ',2**3)
print('División entera: ',10//3)

# %%
# Funciones incorporadas para números
print("Redondear: ", round(3.5))
print("Valor absoluto: ", abs(-3.8))
print("Potencia: ", pow(2,3))

# %% [markdown]
# ### Ejercicio:
# #### __Tarea__: Calcular la longitud de arco de un ángulo
# #### Resultado esperado:
# #### Diámetro del círculo: 9
# #### Ángulo: 45
# #### Longitud de arco: 3.5357142857142856

# %% [markdown]
# ## Listas
#
# Las listas son estructuras de datos que permiten almacenar conjuntos de información en un solo lugar.
# - Una lista es una colección de elementos en un __orden particular__.
# - Una lista puede contener cualquier tipo de objeto, desde números, cadenas, hasta clases más complejas, o incluso otras listas.
# - En Python, las listas se crean utilizando el operador de corchetes `[]`, la función `list()`, o una list comprehension.
# - Las listas pueden aumentar o disminuir de tamaño dinámicamente.


# %%
my_list = [1,2,3,4]
print(my_list)
print("Tipo de objeto: ", type(my_list))

# %%
# Constructor list()
print(list([1,2,3,4]))
print(list("Hello World!"))

# %%
# Listas con múltiples tipos
print([1, 2.0, 'Juan'])

# %%
# Indexación y rebanado
my_list = [1,34,56,6,93,12,45,67]
print(my_list[2])
print(my_list[5:])
print(my_list[-2:])

# %% [markdown]
# Una vez accedidos, los valores de una lista pueden utilizarse en otras funciones
#

# %%
brands = ["BMW", "VW", "Renault"]
print(f"La marca que más me gusta es {brands[2]}")

# %% [markdown]
# Elementos nuevos pueden agregarse a una lista utilizando el metodo `.append()`.

# %%
# Añadir elementos
brands = ["BMW", "VW"]
print(f'Marcas antes de append: {brands}')
brands.append('Renault')
print(f'Marcas despues de append: {brands}')


# %% [markdown]
# Los elementos de una lista pueden modificarse después de acceder al elemento mediante el operador de corchetes y asignar un nuevo valor a dicho elemento.

# %%
brands = ["BMW", "VW", "Renault"]
brands[0] = 'Porsche'
print(brands)

# %%
# Usando del
brands = ["BMW", "VW", "Renault"]
print('Antes de del: ', brands)
del brands[0]
print('Despues de del: ', brands)

# %%
# Usando pop()
# pop(i) extrae los elementos de indice `i` y devuelve y el valor correspondiente.
brands = ["BMW", "VW", "Renault"]
print('Antes de pop: ', brands)
popped_brand = brands.pop(0)
print('Marca removida: ', popped_brand)
print('Despues de pop: ', brands)


# %%
# Los elementos de la lista pueden tambien removerse con `remove()`.
brands = ["BMW", "VW", "Renault"]
print('Antes de remove: ', brands)
brands.remove('BMW')
print('Despues de remove: ', brands)

# %% [markdown]
# <div class="alert alert-block alert-warning"><b>Advertencia: </b>El método remove() elimina solo la primera ocurrencia del valor especificado. </div>

# %%
brands = ["BMW", "VW", "Renault","BMW","BMW"]
print('Antes remove: ', brands)
brands.remove('BMW')
print('Despues remove: ', brands)

# %% [markdown]
# Como se indicó inicialmente, una lista es una secuencia ordenada. Sin embargo, podemos decidir cómo ordenar los elementos de esta secuencia utilizando la función sorted().

# %%
# Ordenar lista
brands = ["BMW", "VW", "renault","BMW","BMW"]
print('Before sorting: ', brands)
brands.sort()
print('After sorting: ', brands)
brands.sort(reverse=True)
print('After sorting (reverse): ', brands)

# %% [markdown]
# Similar al caso de las cadenas, podemos usar los operadores + y * en listas. Bueno, esto es obviamente posible porque las cadenas son objetos similares a listas (listas de caracteres). Esto sucede debido a algo llamado duck-typing, que permite usar los mismos métodos tanto en str como en list.

# %%
# Operadores en listas
brands_EU = ["BMW", "VW", "RENAULT","BMW","BMW"]
brands_USA= ["GMC","TESLA"]
all_brands = brands_EU + brands_USA
print(f"Todas las marcas: {all_brands}")

brands_USA= ["GMC","TESLA"]
print(f"Todas las marcas: {brands_USA * 2}")

# %% [markdown]
# En algunas situaciones, es posible que queramos crear una copia de una lista y modificarla sin afectar el contenido de la lista original.

# %% [markdown]
# Podemos hacer primero una copia `shallow` (shallow copy), que crea una nueva lista que contiene las referencias a los objetos presentes en la lista original. Esto se puede hacer de las siguientes maneras:
# * Usando el operador de rebanado [:] (ya lo conoces)
# * Usando el método `.copy()`
# * Usando el método `copy()` del módulo `copy`

# %%
# Utilizando [:]
brands_EU = ["BMW", "VW", "RENAULT"]
print(brands_EU[:])

# %%
brands_EU = ["BMW", "VW", "RENAULT"]
brands_USA = ["TESLA", "FORD"]
brands_cars = [brands_EU, brands_USA]
print(brands_cars) # Lista de listas

# %%
# Usando el metodo .copy()
brands_cars_copied = brands_cars.copy()
print(brands_cars_copied)

# %%
#Se puede utilizar el metodo copy del modulo copy
from copy import copy
brands_cars_copied = copy(brands_cars)

print('`brands_cars` id: ',hex(id(brands_cars)))
print('`brands_cars_copied`: ',hex(id(brands_cars_copied)))


# %% [markdown]
# Verifiquemos si el primer elemento de cada lista. ¿Se refieren al mismo objeto?

# %%
# Ejecuta: 
print(id(brands_cars[0])) 
print(id(brands_cars_copied[0])) 
# Si, se refieren al mismo objeto.

# %% [markdown]
# Cuando queremos hacer una copia completa de una lista, necesitaremos hacer una copia profunda (deep copy). Este enfoque crea copias de cada elemento del objeto de manera recursiva.

# %%
from copy import deepcopy

brands_EU = ["BMW", "VW", "RENAULT"]
brands_USA = ["TESLA", "FORD"]
brands_cars = [brands_EU, brands_USA]

brands_cars_deep_copied = deepcopy(brands_cars)

# Verificamos el id de las listas
print('`brands_cars` id: ',hex(id(brands_cars)))
print('`brands_cars_deep_copied`: ',hex(id(brands_cars_deep_copied)))

# Verificamos el id del primer objeto en las listas.

print('`brands_cars[0]` id: ',hex(id(brands_cars[0])))
print('`brands_cars_deep_copied[0]` id: ',hex(id(brands_cars_deep_copied[0])))

# %% [markdown]
# # Iteraciones (for loops)
# Como se mencionó anteriormente, una lista es una secuencia de objetos en un orden particular. En Python, comúnmente queremos recorrer cada elemento de esta lista y ejecutar tareas. El recorrido de la lista se puede realizar utilizando diferentes construcciones, las más comunes son los bucles for y las comprensiones de listas.

# %% [markdown]
# #### Usando bucles `for`
# La palabra clave `for` se puede utilizar para iterar sobre una secuencia un número fijo de veces. Esta palabra clave siempre debe usarse en combinación con un objeto iterable. `for` itera sobre los miembros de la secuencia __en orden__, ejecutando el bloque de código cada vez. La palabra clave `for` se usa en combinación con la palabra clave `in`.

# %%
brands_EU = ["BMW", "VW", "RENAULT","CITROEN","FIAT"]
# El patron es el siguiente `for` <variable> `in` <secuencia>: <bloque de codigo>
for brand in brands_EU:
    print(brand)

# %%
# Podemos iterar a traves de cualquier secuencia 
# We can iterate through any sequence
for letter in brands_EU[2]:
    print(letter)

# %% [markdown]
# Podemos construir iteraciones anidadas si es necesario. Necesitamos repetir el patrón \` `for` \<variable\> `in` \<secuencia\>: \<bloque de código\> \`, teniendo cuidado con la indentación, que define el alcance del bucle `for`.

# %%
for brand in brands_EU: # 5 elements
    my_variable = 'happy'
    print(f"This is the brand: {brand}")
    # Repetimos el patron
    for letter in brand: 
        print(f"This is a letter: {letter}")
        ...

# %% [markdown]
# En algunas situaciones, también queremos conocer la ubicación del índice de la variable actual. Para esto, podemos usar la función incorporada `enumerate()`, que toma un iterable y devuelve un iterador que produce una tupla de dos elementos cuando se solicita.

# %%
brands_EU = ["BMW", "VW", "RENAULT","CITROEN","FIAT"]
# El patron es `for` <variable> `in` <sequence>: <code block>
for index, brand in enumerate(brands_EU): # enumerate() devuelve dos objetos: el indice y el valor.

    print(f"Esta es la marca: {brand} ubicada en el lugar: {index}")

# %% [markdown]
# <div class="alert alert-block alert-warning"><b>Advertencia: </b>enumerate() crea un iterador que devuelve dos objetos después de cada ciclo. A diferencia de una secuencia, donde todos los elementos de la secuencia ya están en memoria, un iterador produce valores progresivamente, bajo demanda. </div>

# %% [markdown]
# El bucle `for` iterará hasta agotar la lista. En algunos casos, es posible que queramos detener la iteración después de que se cumpla alguna condición. Para esto, usamos la palabra clave `break`.

# %%
brands_EU = ["BMW", "VW", "RENAULT","CITROEN","FIAT"]

for brand in brands_EU:

    print(f"Esta es una marca: {brand}")

    if brand == "RENAULT": # Condition introduced
        print("Condicion alcanzada, deteniendo el bucle")
        break
    # we repeat the pattern
    for letter in brand:
        print(f"Esta es una letra: {letter}")

# %% [markdown]
# <div class="alert alert-block alert-info"><b>Consejo: </b>La palabra clave `if` se utiliza para introducir una condición. El patrón es `if` < expresión > : < bloque de código >. El < bloque de código > se ejecutará solo si la expresión es `True`. </div>

# %%
# Ejemplo
if 3>2:
    print("Todo en orden")

# %% [markdown]
# De manera similar al caso anterior, podemos omitir el bloque de código si se cumple alguna condición sin detener toda la iteración. Para esto, usamos la palabra clave `continue`.
#

# %%
brands_EU = ["BMW", "VW", "RENAULT", "CITROEN", "FIAT"]

for brand in brands_EU:

    if brand == "RENAULT":  # Condición introducida
        print("Condición cumplida, omitiendo esta marca")
        continue
    print(f"Esta es la marca: {brand}")

# %% [markdown]
# <div class="alert alert-block alert-info"><b>Consejo: </b>La estructura del bucle `for` está presente en muchos lenguajes de programación con sintaxis diferentes. En otros lenguajes de programación, es posible que necesites definir expresiones para controlar el valor del siguiente ciclo o una expresión para determinar si el ciclo ha terminado. En Python, esto se controla construyendo la secuencia apropiada. </div>

# %% [markdown]
# #### Usando comprensión de listas para iterar
# Las comprensiones de listas son una construcción particular de Python y nos permiten iterar a través de listas con una sola línea de código. La principal diferencia con respecto a los bucles `for` es que las comprensiones de listas están diseñadas para crear una lista a través de la iteración de otra lista. 
#
# Una comprensión de lista combina el bucle `for` y la creación de nuevos elementos en una sola línea. Esta es una forma avanzada de construir listas, pero probablemente las encontrarás en muchos archivos de Python.
#

# %%
# Bucle for y métodos incorporados para modificar listas
brands_EU = ["BMW", "VW", "RENAULT", "CITROEN", "FIAT"]
selected = []

for brand in brands_EU:
    if 'W' in brand:  # Condición introducida
        selected.append(brand)

print(f"Esta es la nueva lista: {selected}")


# %%
# Usando comprensión de listas

# El patrón es [<variable_1> for <variable_1> in <una secuencia> <condición>]
selected = [brand for brand in brands_EU if 'R' in brand]

print(f"Esta es la nueva lista: {selected}")



# %%

# Usando comprensión de listas

# El patrón es [<variable_1> for <variable_1> in <una secuencia> <condición>]
selected = [brand for brand in brands_EU if 'R' in brand]

# También podemos hacer iteraciones anidadas con comprensión de listas
brands_EU = ["BMW", "VW", "RENAULT"]
brands_USA = ["GMC", "TESLA", "FORD"]
all_brands = [brands_EU, brands_USA]
print(f"Todas las marcas: {all_brands}")

# Usando bucles for
selected = []
for brand_list in all_brands:
    for brand in brand_list:
        if "L" in brand:
            selected.append(brand)
print('Usando bucles for: ', selected)

# Usando comprensión de listas
selected_1 = [brand for brand_list in all_brands for brand in brand_list if "L" in brand]

print('Usando comprensión de listas: ', selected_1)

# %% [markdown]
# ## Diccionarios  
#
# Los diccionarios son estructuras de datos que nos permiten conectar piezas de información relacionada. Cualquier cosa que pueda emparejarse puede almacenarse como un diccionario. Los diccionarios son estructuras de datos importantes en Python porque pueden almacenar datos anidados casi ilimitados.  
#
#

# %%
# Un diccionario es una colección de pares clave-valor.  
# Cada clave es única, y el valor puede ser de cualquier tipo de dato (int, string, lista, etc.)  

# Ejemplo: Crear un diccionario  
persona = {  
    "nombre": "John",  
    "edad": 30,  
    "ciudad": "Nueva York",  
}  

# Imprimir el diccionario  
print(persona)  

# %%
# Podemos acceder a los valores en un diccionario usando la clave  
# En este caso, la clave es 'nombre'  
print(persona["nombre"])  

# %%
# También podemos usar el método `get()` para acceder a los valores  
print(persona.get("nombre"))  

# %%
# Si la clave no existe, `get()` devuelve None en lugar de generar un error  
type(persona.get("país"))

# %%
# Añadir un nuevo par clave-valor  
persona["comida_favorita"] = "pizza"  
print(persona)  # Ahora el diccionario incluye la clave 'país'  

# %%
# Actualizar un valor existente  
persona["edad"] = 42  
print(persona)  # El valor de 'edad' se actualiza a 42  

# %%
# Usar la palabra clave `del`  
del persona["ciudad"]  
print(persona)  # 'ciudad' se elimina del diccionario

# %%
# Usar `pop()` para eliminar y devolver el valor  
edad = persona.pop("edad")  
print(persona)  # 'edad' se elimina  
print(f"Edad eliminada: {edad}")  # Salida: Edad eliminada: 31  

# %%
# Verificar si una clave existe en un diccionario  

# Usar la palabra clave `in`  
print("nombre" in persona)  # True  
print("ciudad" in persona)  # False 

# %%
# Recorrer un diccionario  

# Iterar a través de las claves  
for clave in persona:  
    print(clave) 

# %%
# Iterar a través de los valores  
for valor in persona.values():  
    print(valor)  # Imprime todos los valores 

# %%
# Iterar a través de pares clave-valor  
for clave, valor in persona.items():  
    print(f"La respuesta es: {clave}: {valor}")  # Imprime pares clave-valor  

# %%
# También podemos aplicar una comprensión de diccionario  

# Crear un nuevo diccionario donde las claves son números y los valores son sus cuadrados  
cuadrados = {(x): f"mi número es {x}" for x in range(5)}  
print(cuadrados)  

# %%
# Diccionarios anidados (diccionarios dentro de diccionarios)  

# Un diccionario que contiene otro diccionario como valor  
diccionario_anidado = {  
    "persona1": {"nombre": "Alice", "edad": 25},  
    "persona2": {"nombre": "Bob", "edad": 28}  
}  

# Acceder a un diccionario anidado  
# print(diccionario_anidado["persona1"]["nombre"])  

for clave, valor in diccionario_anidado.items():  
    print(f"El nombre de nuestro cliente es {valor['nombre']}")  


# %%

# Métodos de diccionario  

# `keys()` devuelve todas las claves como un objeto dict_keys  
print(persona.keys())

# `values()` devuelve todos los valores como un objeto dict_values  
print(persona.values())

# `items()` devuelve todos los pares clave-valor como un objeto dict_items  
print(persona.items())  

# Usar `update()` para fusionar otro diccionario en el actual  
persona.update({"género": "Masculino", "ciudad": "Nueva York"})  
print(persona)

# %%
# Usar el operador de desempaquetado `**` para fusionar diccionarios  
nueva_informacion = {1: ["Leer", "Viajar"]}  
persona = {  
    "nombre": "John",  
    "edad": 30,  
    "ciudad": "Nueva York",  
}  
diccionario_fusionado = {**persona, **nueva_informacion}  
print(diccionario_fusionado)


# %% [markdown]
# ## Tuplas
# Una tupla es una colección ordenada e inmutable de elementos. Son similares a las listas, pero a diferencia de las listas, no se pueden modificar una vez creadas.
#

# %%
# Ejemplo: Crear una tupla
mi_tupla = (1, 2, 3, 4)
print(mi_tupla)
# %%
# Acceder a elementos en una tupla

# Puedes acceder a los elementos de una tupla por índice (indexación basada en 0)
print(mi_tupla[0])  
print(mi_tupla[2])  

# La indexación negativa comienza desde el final
print(mi_tupla[-1]) 
# %%
# Rebanar una tupla

# Rebanar devuelve una nueva tupla con un subconjunto de los elementos
print(mi_tupla[1:3])  

# Rebanar con indexación negativa
print(mi_tupla[-3:-1])
# %%
# Las tuplas son inmutables, lo que significa que sus elementos no se pueden cambiar después de su creación

# Intentar modificar un elemento resultará en un error
mi_tupla[0] = 10  

# %%
# Concatenar y repetir tuplas

# Concatenar dos tuplas
tupla1 = (1, 2)
tupla2 = (3, 4)
tupla_combinada = tupla1 + tupla2
print(tupla_combinada)  

# Repetir una tupla
tupla_repetida = (5, 6) * 3
print(tupla_repetida)  
# %%
# Verificar la longitud de una tupla

# Usar la función len() para obtener el número de elementos en una tupla
print(len(mi_tupla))  
# %%
mi_tupla


# %%
# Verificar si un elemento existe en una tupla

# Usar la palabra clave `in`
print(3 in mi_tupla) 
print(10 in mi_tupla) 
# %%
# Iterar a través de una tupla

# Usar un bucle for para iterar sobre los elementos
for elemento in mi_tupla:
    print(elemento)  # Imprime cada elemento de la tupla
# %%
mi_tupla

# %%
# Desempaquetar una tupla

# Puedes desempaquetar los elementos de una tupla en variables
a, b, c, d = mi_tupla
print(a, b, c, d)  

# Puedes usar un guion bajo `_` para ignorar un valor específico
x, _, y, _ = mi_tupla
print(x, y) 
# %%
# Convertir otros tipos de datos a tuplas

# Puedes convertir listas, cadenas y otros tipos iterables a tuplas
mi_lista = [1, 2, 3]
tupla_desde_lista = tuple(mi_lista)
print(tupla_desde_lista)  

# Convertir una cadena a una tupla
tupla_desde_cadena = tuple("hola")
print(tupla_desde_cadena) 
# %%
# Contar y encontrar el índice de elementos en una tupla

# `count()` devuelve cuántas veces aparece un elemento específico en una tupla
print(mi_tupla.count(3))  

# `index()` devuelve el índice de la primera aparición de un elemento específico
print(mi_tupla.index(3))
# %%
# Crear una tupla vacía

# Una tupla vacía se puede crear usando paréntesis vacíos
tupla_vacia = ()
print(tupla_vacia) 

# Puedes crear una tupla con un solo elemento añadiendo una coma al final
tupla_un_elemento = (1,)
print(tupla_un_elemento) 

# %% [markdown]
# # Funciones
#
# El concepto de funciones en Python es análogo al concepto de funciones en matemáticas.
#
#  $$ z = f(x,y)$$

# %% [markdown]
# En Python, las funciones son más versátiles y genéricas que las funciones matemáticas. De hecho, contienen bloques de código reutilizables que pueden realizar una tarea específica.
# Ayudan a organizar el código, reducir la redundancia y mejorar la modularidad.

# %% [markdown]
# Sintaxis básica
# ```python
# def nombre_de_la_función(<tus-parámetros>):
#     <tu bloque de código aquí>
#     return <un valor de salida>      # Declaración de retorno opcional
# ```
# - **`def`**: Palabra clave para definir una función
# - **\<tus-parámetros\>**: Entradas de la función (opcional)
# - **`return`**: Devuelve un valor (opcional; por defecto es `None`)

# %%
# Una función básica necesita usar indentación para indicar el alcance
def saludar():
    return "¡Hola, Mundo!"

mensaje = saludar()  # Llamada a la función
print(mensaje)

# %%
def sumar(a, b):
    """Devuelve la suma de dos números""" 
    return a + b

resultado = sumar(3, 5)
print(f"3 + 5 = {resultado}")

# %%
sumar(2,1)


# %%
# Podemos crear parámetros por defecto usando el operador =
def potencia(base, exponente=2):
    """Devuelve la base elevada al exponente (por defecto: al cuadrado)"""
    return base ** exponente
print(potencia(2))

# %%
print(potencia(2,5))


# %%
# Los argumentos se pasan a cada parámetro correspondiente usando el operador de asignación
def info_persona(nombre, edad, ciudad):
    print(f"{nombre}, {edad} años, vive en {ciudad}")

info_persona(edad=30, ciudad="París", nombre="Alicia")  # El orden no importa

# %% [markdown]
# En Python podemos recibir argumentos de manera flexible usando `*args` y `**kwargs`.
#

# %%
def imprimir_args(*args, **kwargs):
    print("Argumentos posicionales:", args)
    print("Argumentos de palabra clave:", kwargs)

imprimir_args(1, 'a', nombre="Juan", edad=25, a=1, b=3)

# %%
def validar(*args, **pizza):
    if 'cuenta' in pizza:
        print(f'Acceso concedido a: {pizza['cuenta']}')
    else:
        print("No válido")

validar(1, nombre="Juan", edad=25, a=1, b=3, cuenta='Gustavo', tamaño='L')


# %% [markdown]
# Una función puede devolver uno o más valores cuando se define `return`, de lo contrario devuelve `None`

# %% [markdown]
# Sobre argumentos y parámetros:
#
# - **Parámetros Requeridos**: Deben pasarse durante la llamada a la función
# - **Parámetros por Defecto**: Tienen valores predeterminados si no se proporcionan
# - **Argumentos de Palabra Clave**: Especificados por el nombre del parámetro
# - **Argumentos de Longitud Variable**: `*args` (tuplas) y `**kwargs` (diccionarios)

# %%
# Llama a la función imprimir_args() con los argumentos de tu elección y asigna la salida a una variable llamada 'a'

# %%
# Si es necesario, podemos devolver múltiples salidas, pero puede ser necesario desempaquetarlas al asignarlas a variables

def mi_función(a, b):
    suma_personalizada = a + b
    resta = a - b
    multiplicación = a * b
    soluciones = [suma_personalizada, resta, multiplicación]
    return soluciones




# %% [markdown]
# # Condicionales `If`
# La sentencia `if` ejecuta bloques de código basados en condiciones booleanas.
#
# **Sintaxis:**
# ```python
# if condición:
#     # bloque de código indentado
# ```
#
# **Reglas clave:**
# - Dos puntos `:` obligatorios después de la condición
# - Bloques de código definidos por indentación (se recomiendan 4 espacios)
# - Operadores de comparación: `>`, `<`, `==`, `!=`, `>=`, `<=`

# %%
temperatura = 30
if temperatura > 25:
    print("¡Es un día caluroso!")
    print("¡Mantente hidratado!")

# %% [markdown]
# ## Sentencia If-Else
# Proporciona caminos de ejecución alternativos:
# ```python
# if condición:
#     # caso verdadero
# else:
#     # caso falso
# ```

# %%
edad = 12
if edad >= 18:
    print("Eres elegible para votar")
else:
    print("Aún no eres elegible para votar")
    años_faltantes = 18 - edad
    print(f"Vuelve en {años_faltantes} año{'s' if años_faltantes > 1 else ''}")

# %% [markdown]
# ## Sentencias Elif (Else If)
# Maneja múltiples condiciones exclusivas:
# ```python
# if cond1:
#     ...
# elif cond2:
#     ...
# else:
#     ...
# ```

# %%
puntuación = 82
if puntuación >= 90:
    calificación = "A"
elif puntuación >= 80:
    calificación = "B"
elif puntuación >= 70:
    calificación = "C"
elif puntuación >= 60:
    calificación = "D"
else:
    calificación = "F"
print(f"Puntuación: {puntuación} -> Calificación: {calificación}")

# %% [markdown]
# ## Veracidad y Evaluación Booleana
# Python evalúa valores no booleanos en condiciones:
# - **Falsy:** `None`, `0`, colecciones vacías (`""`, `[]`, `{}`, etc.), False
# - **Truthy:** Todos los demás valores, True

# %%
nombre_usuario = 4
if nombre_usuario:
    print(f"Bienvenido {nombre_usuario}")
else:
    print("Usuario invitado")

# %% [markdown]
# ## Operadores Lógicos
# Combina condiciones con:
# - `and`: Ambos deben ser verdaderos
# - `or`: Al menos uno debe ser verdadero
# - `not`: Invierte el valor booleano

# %%
edad = 45
tiene_licencia = False
if (edad >= 18) or (tiene_licencia):
    print("Puedes conducir un coche")
else:
    print("No se permite conducir")

# %% [markdown]
# ## Sentencias If Anidadas
# Las sentencias if pueden contener otras sentencias if

# %%
saldo_cuenta = 11500
es_premium = 1
if saldo_cuenta > 0:
    print("Cuenta activa")
    if es_premium:
        print("Beneficios premium activados")
        if es_premium and saldo_cuenta > 2000:
            print("Felicidades, has ganado un premio")
    else:
        print("Cuenta estándar")
else:
    print("Cuenta suspendida")

# %% [markdown]
# ## Operador Ternario
# Expresión condicional compacta:
# ```python
# resultado = valor_verdadero if condición else valor_falso
# ```

# %%
costo = 99
var = 24 if costo < 15 else 56
print(var)

# %%
temperatura = 28
estado = "Caluroso" if temperatura > 25 else "Fresco"
print(f"Estado: {estado}")

# %% [markdown]
# ## Errores Comunes
# 1. Usar `=` en lugar de `==`
# 2. Olvidar los dos puntos `:`
# 3. Indentación incorrecta
# 4. Condiciones demasiado complejas

# %%
# Ejemplo de error común
x = 5
if x == 10:  # Comparación correcta
    print("x es 10")

# %% [markdown]
# ## Ejemplo Práctico: Control de Acceso de Usuario
# Implementación del mundo real combinando múltiples conceptos

# %%
usuario = {
    "nombre_usuario": "admin",
    "está_activo": True,
    "intentos_de_inicio": 2,
    "rol": "admin"
}

if usuario["está_activo"]:
    if usuario["intentos_de_inicio"] < 3:
        if usuario["rol"] == "admin":
            print("Panel de administrador")
        elif usuario["rol"] == "editor":
            print("Panel de editor")
        else:
            print("Perfil de usuario")
    else:
        print("Cuenta bloqueada")
else:
    print("Cuenta desactivada")



# %%
