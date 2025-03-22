# %% [markdown]
# # Introducción a brightway - pt. 1
#
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion: 
#
# https://docs.brightway.dev/en/latest/index.html

# %% [markdown]
# ## Instala las brightway y las dependencias necesarias

# %%
# !pip install bw2calc==2.0.dev17 -q # Paquete de brightway
# !pip install bw2data==4.4.3 -q # Paquete de brightway
# !pip install bw2io==0.9.dev41 -q # Paquete de brightway
# !pip install polars==0.20.15 -q 
# !pip install pypardiso -q
# !pip install scipy==1.12.0 -q
# !pip install seaborn==0.13.2 -q

# %% [markdown]
# <div class="alert alert-block alert-warning">
# ⚠️ Debes restaurar la sesion!
# </div>
#

# %% [markdown]
# ## Configura tu proyecto brightway
# Debido al gran tamano de las bases de datos utilizadas en ACV, brightway require grabar cierta informacion en disco. 
# Por esta razon, cada vez que se crea un proyecto nuevo es necesario configurarlo.
#
# El primer paso consiste en importar las dependencias necesarias:
# %%
import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print

# %% [markdown]
# Podemos ver la lista de proyectos existentes utilizando el modulo `bw2data`:

# %%
print('bw2data version: ',bd.__version__)
print('bw2io version: ',bi.__version__)
print('bw2calc version: ',bc.__version__)

# %%
bd.projects

# %% [markdown]
# Cualquier entorno de ejecucion de python que importe al paquete `bw2data` estara configurado con el proyecto ``default`` por defecto.
#

# %%
bd.projects.current

# %% [markdown]
# En caso que desee cambiar de proyecto, la funcion `bw2data.set_current(<el-nombre-de-tu-proyecto>)` permite elegir un proyecto existente. En el caso que el proyecto no exista, esta funcion creara un proyecto nuevo.

# %%
bd.projects.set_current('nuevo_proyecto')

# %%
# Puede ver que 'nuevo_proyecto' aparece ahora en la lista de proyectos.
bd.projects

# %% [markdown]
# <div class="alert alert-block alert-warning">
# ⚠️ Todas las modificaciones realizadas por los distintos modulos de brightway se realizan EXCLUSIVAMENTE en el contexto del proyecto. Por ello es importante verificar que trabaja con el proyecto correcto.
# </div>
#

# %% [markdown]
# Para guardar registro de los proyectos y distinta informacion necesaria, `bw2data` grabara algunos archivos en el disco. Pueden existir casos (muy excepcionales) en los que necesites acceder a estos archivos de manera directa. Para ello puedes localizarlos utilizando la funcion `bw2data.projects.dir`

# %% [markdown]
# En caso desees realizar una copia del proyecto actual, puedes utilizar `bw2data.projects.copy_project`

# %%
bd.projects.copy_project(new_name="nuevo_proyecto_2")

# %%
# Verificamos
bd.projects

# %% [markdown]
# En caso desees eliminar un proyecto, puedes utilizar la funcion `bw2data.projects.delete_dir`

# %%
# El argumento `delete_dir` es booleano e indica 
# si tambien se desea eliminar la carpeta que contiene los datos del proyecto.
bd.projects.delete_project(name='nuevo_proyecto', delete_dir=True)


# %% [markdown]
# 🚧 **Manos a la obra**:
# - Crea un nuevo proyecto llamado 'peru25'
# - Crea una copia de 'peru25' llamada 'peru25-prueba'
# - Activa el proyecto 'peru25'
#

# %%
# Inserta el codigo aqui

# %% [markdown]
# ## Creando una nueva biosfera
# Brightway esta fuertemente (pero no estrictamente) ligado a los modelos y esquemas utilizados por ecoinvent.
# Por esto, los metodos de impacto y flujos ambientales (biosfera) son aquellos proporcionados por ecoinvent a traves de su servicio ecoquery. 
# Aunque los metodos son desarrollados por grupos de investigacion independientes, ecoinvent los centraliza y modifica a fin de que sean compatibles y listos para conectarse con su base de datos.

# %% [markdown]
# Lo primero que haremos sera crear una biosfera (a la ecoinvent) y los multiples metodos de impacto disponibles por defecto.
# Para esto, el paquete `bw2io` cuenta con una funcion llama `bw2setup`, asi:

# %%
bd.projects

# %%
bd.projects.set_current('example_project')
bd.databases

# %%
# bi.bw2setup()

# %% [markdown]
# El mensaje de la celda de arriba nos dice que `bw2io` ha creado una base de datos llamada 'biosphere3' que contiene 4709 nodos (flujos ambientales).
# Adicionalmente, 762 metodos de impacto nuevos han sido creados.
#

# %% [markdown]
# <div class="alert alert-block alert-info">
# Diferentes grupos de investigacion actualizan constanmente distintos metodos de impacto. Por ello, cada version de `bw2io` puede presentar nuevos metodos de impacto. Puedes ver la version de bw2io asi: `bw2io.__version__`
# </div>

# %% [markdown]
# La biosfera esta ahora almacenada en una base de datos. En la jerga de brightway, una base de datos no es mas que un objeto que permite acceder a los nodos contenidos en este. Podemos ver las bases de datos contenidas en este proyecto de la siguiente manera:

# %%
# La base de datos 'biosphere3' tiene ese nombre por defecto. 
bd.databases

# %% [markdown]
# Podemos manipular la biosfera asignando la base de datos a una nueva variable `biosfera` de la siguiente forma:

# %%
biosfera = bd.Database('biosphere3')

# %% [markdown]
# Por ahora no exploraremos a detalle esta base de datos. Si embargo utilizaremos la funcion `random` que nos permite muestrear un nodo aleatorio para ver de que trata el contenido.

# %%
# Ejecuta esta celda multiples veces y veras que siempre tienes respuestas diferentes.
biosfera.random()


# %% [markdown]
# De manera similar, podemos explorar los diferentes metodos que fueron instalados previamente. En brightway, los metodos presentados como una combinacion de tres elementos: 
# > (<'Nombre del metodo'>, <'Categoria de impacto'>, <'Indicador'>)

# %%
bd.methods 
# Hay que 'convertir' bw2data.methods en una lista para poder ver todos los metodos disponibles
# list(bd.methods) 

# %% [markdown]
# Buscar un metodo en una lista tan extensa puede ser muy problematico. 
# Para facilitar la busqueda de una metodo en especifico, podemos utilizar el poder de python.

# %%
# bw2data.methods es un objeto sobre el que se puede iterar
# Por ejemplo, busquemos un metodo relacionado con el cambio climatico
for nombre, categoria, indicator in bd.methods:
    if categoria == 'climate change':
        print((nombre, categoria, indicator))

# %% [markdown]
# ## Manipular bases de datos
# En la seccion anterior, dejamos que `bw2io.bw2setup` cree una base de datos nueva llamada 'biosphere3'. Una base de datos contiene nodos, ya sean de la biosfera o de la tecnosfera. En otros software, los nodos de la biosfera suelen ser llamados Elementary Flow y los de la tecnosfera, Activities. En brightway, se utiliza el concepto general de 'nodo' a cualquier elemento que este contenido en una base de datos. Este puede ser un flujo elemental o un actividad de la tecnosfera.
#
# En este sentido, una nueva base de datos puede ser creada de la siguiente manera:
#

# %%
# Primero, se asigna una instancia de base de datos a una variable
# Esta informacion esta en la memoria de la computadora pero no grabado en el disco
mi_db = bd.Database('mi_base_de_datos')

#Segundo, se registra la base de datos para que sea grabada en el disco
mi_db.register()

# %% [markdown]
# Podemos verificar que ahora existen 2 bases de datos, la biosfera creada por `bw2io` y `mi_base_de_datos`, creada por nosotros.

# %%
bd.databases

# %% [markdown]
# En muchas situaciones, puede que sea necesario realizar una copia de una base de datos. Esto puede realizarse de la siguiente forma:

# %%
new_database = bd.Database('biosphere3').copy('new_biosphere')

# %% [markdown]
# Para borrar una base de datos, solo hay que imaginar que `bd.databases` tiene las mismas propiedades que un diccionario de python y utilizar `del`
#

# %%
if 'new_biosphere' in bd.databases:
    del bd.databases['new_biosphere']

# %% [markdown]
# ## Manipular Actividades
# Una de las funcionalidades de brightway mas importantes es la creacion de actividades (o nodos, en general).
# Se puede crear una actividad utilizando la funcion `new_activity`, perteneciente a los objetos de base de datos. En este caso, se puede indicar cualquier cantidad de argumentos pero incluyendo SIEMPRE los argumentos `code`, `name`, `unit` y `location`. Estos cuatro argumentos son obligatorios porque es lo minimo requerido para tener actividades unicas. 
#

# %%
bd.projects

# %%
bd.databases

# %%
if 'mi_base_de_datos' in bd.databases: # es una buena practica para siempre comenzar en un lienzo en blanco
    del bd.databases['mi_base_de_datos']



# %%
db = bd.Database('mi_base_de_datos')
db.register()
activity_ejemplo = db.new_activity(code='codigo-unico', name='nombre-no-unico', unit='unidad', location='PE')
activity_ejemplo.save() # Este paso es SIEMPRE necesario para grabar la informacion en el disco
print(list(db))

# %% [markdown]
# Esta actividad se encuentra ahora registrada en el disco y puede accederse utilizando su identificar `code` y la funcion `get`. Es importante aclarar que `code` es unico solo para la base de datos.

# %%
actividad = db.get('codigo-unico')
print(actividad)

# %% [markdown]
# Informacion mas detallada de esta actividad puede verse con la funcion `as_dict`, que devuelve un diccionary de python.

# %%
actividad.as_dict()

# %% [markdown]
# En caso deseado, la actividad puede borrarse utilizando la funcion `delete`.
#

# %%
actividad.delete()

# %% [markdown]
# Siguiendo el ejemplo de la bicicleta, podemos ta crear todos los nodos (tecnosfera y biosfera).

# %%
data = {
    'code': 'bici',
    'name': 'produccion bici',
    'location': 'PE',
    'unit': 'piece'
}

bike = db.new_activity(**data)
bike.save()

data = {
    'code': 'CF',
    'name': 'carbon fibre',
    'unit': 'kilogram',
    'location': 'CN'
}

cf = db.new_activity(**data)
cf.save()

ng = db.new_activity(
    name="Nat Gas", 
    code='ng', 
    location='NO', 
    unit='MJ'
)

ng.save()

print(list(db))


# %%
# Creamos un nodo en la biosfera
co2 = bd.Database('biosphere3').new_activity(
    name="Carbon Dioxide", 
    code='co2', 
    categories=('air',),
    type='emission',
)

co2.save()


# %%
# # En caso quiera borrar todos los nodos de `db`
# co2.delete()
# for i in db:
    # i.delete()

# %% [markdown]
# Ya contamos con todos los nodos, sin embargo estos estan desconectados.
# Sin una red conectada, no podemos hacer el computo del ACV. Para esto, tenemos que crear las 'conexiones/interacciones' entre todos los nodos. En brightway, estos se llaman 'exchanges', y pueden ser creados de la siguiente manera con la funcion `new_exchange`:
#

# %%

bike.new_exchange(
    amount=2.5, 
    type='technosphere',
    input=cf
).save()

cf.new_exchange(
    amount=237, 
    type='technosphere',
    input=ng,
).save()

cf.new_exchange(
    amount=26.6, 
    type='biosphere',
    input=co2,
).save()

# %% [markdown]
# Podemos ahora crear un metodo nuevo que solo tenga un factor de caracterizacion:

# %%
ipcc = bd.Method(('IPCC',)) # Si no existe, lo crea
ipcc.write([
    (co2.key, {'amount': 1}),
])

# %% [markdown]
# El paquete `bw2calc` contiene las herramientas para realizar los calculos, como la clase LCA:

# %%
lca = bc.LCA({bike:1},method=('IPCC',)) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida
lca.lcia() # Calcula los impactos 
print("El impacto es: ", lca.score)

# %% [markdown]
# 🚧 **Manos a la obra**:
# - Se ha descubierto que la produccion de fibra de carbono emite 0.23 kg de monoxido dinitrogeno al aire $N_{2}O$ por cada kilogramo de fibra de carbono producido.
# - El factor de caracterizacion del $N_{2}O$ es 276.9
# - En cuanto ha aumentado el impacto ?  


# %%
# Creamos un nodo en la biosfera
n2o = bd.Database('biosphere3').new_activity(
    name="Nitrous oxide", 
    code='n2o', 
    categories=('air',),
    type='emission',
)

n2o.save()

cf.new_exchange(
    amount=0.23, 
    type='biosphere',
    input=n2o,
).save()

# %%
ipcc = bd.Method(('IPCC',))
factors = ipcc.load()
factors.append(((n2o.key),{'amount': 276.9}))
ipcc.write(factors)

# %%
ipcc.load()

# %%
lca_nuevo = bc.LCA({bike:1},method=('IPCC',)) # Instancia la clase
lca_nuevo.lci() # calcula el inventario de ciclo de vida
lca_nuevo.lcia() # Calcula los impactos 
print("El impacto ahora es: ", lca_nuevo.score)

print(f"El impacto aumento en: {(lca_nuevo.score-lca.score)*100/lca.score} %")

# %%

# %% [markdown]
# ## Exportar bases de datos y proyectos
# En la seccion anterior aprendimos a crear bases de datos de manera automatica ('biosphere3') y de manera manual ('mi_base_de_datos'). 
# En situaciones convencionales, es normal que necesitemos compartir nuestros modelos de inventario, ya sea durante el trabajo colaborativo o para reportar nuestro trabajo a revisores, colegas y cualquier por razones de transparencia.
# Para esto, bw2io ofrece una serie de herramientas que pueden usarse para exportar los modelos en diferentes formatos. 
# Por un tema de popularidad, en esta seccion nos enfocaremos en 3 herramientas:
# - Exportar una base de datos a excel
# - Exportar una base de datos a csv (dataframe)
# - Exportar un proyecto como archivo comprimido de respaldo.

# %% [markdown]
# ###  Exportar a excel
# Brightway utiliza un template para leer y exportar bases de datos en formato excel. Es conveniente para distribuir versiones finales del inventario. No es muy bueno almacenando informacion anidad. No permite 'trackear' los cambios debido a que *.xlsx no es un formato de texto.

# %%
import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print
# Primero que nada, verifiquen que esten en el proyecto adecuado
bd.projects.current

# %%
# Si no es el proyecto adecuado, ya saben que hacer
bd.projects.set_current('example_project')

 # %%
 # bi.export.excel.write_lci_excel??

# %%
# dirpath es el argumento que controla en que ubicacion se exportara el archivo. 
# En sistemas operativos tipo UNIX (Linux, MacOS), '.' significa 'aqui'.
directorio = bi.export.excel.write_lci_excel(database_name='mi_base_de_datos',dirpath='.')

# %% [markdown]
# ###  Exportar a csv
# Brightway permite convertir los nodos (actividades) y aristas (exchanges) en DataFrames de [pandas](https://pandas.pydata.org/).
# Un DataFrame es un estructura de datos tabular que es muy usada en analisis y ciencia de datos, y puede ser exportada directamente como archivo CSV.
#

# %%
db.nodes_to_dataframe() # Solo los nodos

# %%
db.edges_to_dataframe() # Solo aristas

# %%
# La funcion `to_csv` es propia de pandas, no de brightway
db.nodes_to_dataframe().to_csv('mis-nodos.csv')
db.edges_to_dataframe().to_csv('mis-aristas.csv')

# %% [markdown]
# ###  Exportar proyecto completo como backup
# La ultima opcion mas comun es la de exportar el proyecto completo en forma de archivo comprimido. Esto suele hacer cuando se desea guardar copias de todas las bases de datos de un proyecto. La desventaja es que el archivo resultado puede ser pesado y no es adecuado si no se tienen los permisos para compartir bases de datos comerciales.

# %%
bi.backup_project_directory('example_project',dir_backup='.')

# %% [markdown]
# ## Importar bases de datos privadas
# Esta seccion es una continuacion natural de la anterior ya que simplemente aprenderemos a importar los archivos que fueron exportados previamente. Asumiremos, nuevamente, que excel, csv, y backup.tar.gz son los unicos formatos que nos interesan.
#
# ### Importar un archivo de excel

# %%
importador = bi.ExcelImporter('lci-mi_base_de_datos.xlsx')
importador.apply_strategies()
importador.match_database(fields=('name', 'code', 'unit', 'location'))  # Conecta nodos del archivo excel
importador.match_database('biosphere3', fields=('name','unit','categories')) # Conecta nodos con la base de datos biosphere3
importador.statistics()
importador.write_excel()

# %%
importador.match_database('biosphere3', fields=('name','unit','categories')) # Conecta nodos con la base de datos biosphere3
importador.statistics()

# %%
importador.write_database()
bd.databases # La base de datos se ha importado correctamente

# %%

# %% [markdown]
# ### Repliquemos los resultados
# Ahora podemos 'simular' un ejercicio de reproducibilidad, y realizar el calculo de los impactos una vez mas.

# %%
db = bd.Database('mi_base_de_datos')
bicicleta = db.get('bici') # seleccionamos la actividad que tiene codigo 'bici', la definimos en la seccion anterior

# %%
lca = bc.LCA({bicicleta:1},method=('IPCC',)) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida
lca.lcia() # Calcula los impactos 
print("El impacto es: ", lca.score) # Es el mismo 🎉

# %% [markdown]
# 🚧 **Manos a la obra**:
# - Un colega ha encontrado un error en tu modelo. La cantidad de Gas Natural consumida por la fibra de carbono no es 237, sino 23.7
# - Descarga el archivo de excel `lci-mi_base_de_datos.xlsx` a tu computadora personal y modifica el valor manualmente.
# - Importa el archivo excel modificado y vuelve a calcular el ACV. Cuanto ha cambiado el impacto final?

# %%
# Tu codigo aqui
