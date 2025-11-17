# # Introduccion a brightway - pt. 2
#
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion:
#
# https://docs.brightway.dev/en/latest/index.html

# Este notebook se ejecutara en una nueva sesion, por lo que necesitamos instalar las dependencias una vez mas.

# !pip install bw2calc>=2.1 -q # Paquete de brightway
# !pip install bw2data>=4.5 -q # Paquete de brightway
# !pip install bw2io>=0.9.11 -q # Paquete de brightway
# !pip install polars -q
# !pip install pypardiso -q
# !pip install seaborn>=0.13.2 -q

# <div class="alert alert-block alert-warning">
# ⚠️ Debes restaurar la sesion!
# </div>
#

# Debemos descarg un archivo de respaldo que contiene ecoinvent. Para ellos tenemos que autenticar nuestro usuario de **gmail** que fue creado anteriormente.

# +
from google.colab import auth
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
drive.CreateFile({'id': '1E3wPUOuRp13ucuNmq3557EuT3mszlmHB'}).GetContentFile('backup.tar.gz')
# -

# Verificamos
# !du -hs backup.tar.gz

import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print

# ### Importar el backup del proyecto
# Este modalidad no require mucha explicacion: El proyecto se carga nuevamente.

bi.restore_project_directory(
    'backup.tar.gz',  # nombre del archivo, creado celdas arriba
    project_name='proyecto_ei', # Se puede elegir un nombre nuevo para el proyecto
    overwrite_existing = False
    )

# ## Importar bases de datos comerciales
# Hemos aprendido a construir un modelo de ACV desde cero y de forma manual. Aunque esto resulta bastante util, en la realidad solemos combinar nuestros datos con aquellos provenientes de bases de datos comerciales. En esta seccion nos enfocaremos en la base de datos ecoinvent (v3.9), que es una de las mas utilizadas en el sector.
#
# En la actualidad hay dos maneras de importar los datos de ecoinvent en nuestro proyecto:
# - Leyendo los archivos ecospold2 crudos directamente del disco y convirtiendolos en una base de datos de brigthway.
# - Utilizando la herramienta `import_ecoinvent_release` que descarga la base de datos desde un servidor remoto.
#
# ### Importando ecoinvent (crudo) desde el disco
#
# Para este caso, es necesario haber descargado ecoinvent. Ecoinvent es distribuido en formato comprimido 7z, y contiene todas las actividades en formato ecospold2 (algo similar a XML). `bw2io` tiene funciones disenadas para interpretar la informacion, verificar que los `exchanges` sean correctos, y que los nodos de la biosfera existan en la base de datos 'biosphere3'.
#



# +
# Para importar, hay que seguir los siguentes pasos:
# 1. Leer los archivos XML e dejar que brigthway los interprete.
# db = bi.SingleOutputEcospold2Importer(dirpath='<datasets-folder>',db_name='ecoinvent39')

# +
# 2. Aplicar una serie de estrategias para asegurarse que no existe informacion corrupta y que la importacion es posible
# db.apply_strategies()

# +
# 3. Ecoinvent esta listo en la memoria pero aun no ha sido grabado en el disco.
# Hay que grabarlo en el disco.
# db.write_database()
# -

# Para verificar que ha sido importado correctamente, podemos repetir el ejercicio realizado con la base de datos 'biosphere3' de la anterior seccion.bd.databases

# +
# bd.databases # Lista de las bases de datos

# +
# ei = bd.Database('ecoinvent39')
# len(ei) # Muestra la cantidad de elementos
# -

# ### Importando ecoinvent desde un servidor remoto
# Para este caso utilizamos la funcion `bw2io.import_ecoinvent_release` que se encarga de 1) instalar una biosfera, 2) instalar los metodos de impacto mas actuales, y 3) instalar la base de datos ecoinvent.
# Como podran imaginar, requiere la autenticacion del usuario que debe poseer un cuenta de acceso ecoinvent

# +
# bw2io.import_ecoinvent_release(
#     version="3.9"
#     system_model="cutoff", # Otras opciones son: "consequential", "apos" y "EN15804"
#     username="xxxx", # Tu usuario
#     password="xxxx", # Tu clave
#     biosphere_name="biosphere" # Optional, puedes guardar la base de datos de la biosfera con otro nombre.
# )
# -


# ### Explorando Ecoinvent

bd.projects.set_current("proyecto_ei")
ei = bd.Database('ecoinvent-3.9.1-cutoff')
seleccionado = ei.random() # Explora las actividades
# Primero exploramos los keys de la actividad seleccionada
print(list(seleccionado.keys()))
# %%
# Podemos ver el contenido de todo el dataset.
print(seleccionado.as_dict())
# %%
# Como pueden notar, el contenido de la actividad ecoinvent es bastante rica. Existen campos fuera de `name`, `code`,`location` y `unit` que son nuevos para nosotros, lo que demuestra que brightway es lo suficientemente flexible al definir una actividad.
#
# Lo que vimos en la celda anterior describe a una actividad, pero aun no describe sus conexiones (`exchanges`). Para acceder a ellas, hay que utilizar las funciones `exchanges`, `technosphere` o `biosphere`, segun lo que se desee observar.

# `exchanges` retorna un objeto the brightway que no es nativo de python
type(seleccionado.exchanges())

# Si deseamos leerlo al estilo de una lista, hay que convertirlo en una lista.
for exchange in seleccionado.exchanges():
    print(exchange)
# print(list(seleccionado.exchanges()))

# Si deseamos solo la tecnosfera, usamos la funcion correspondiente
for exchange in seleccionado.technosphere():
    print(exchange)
# print(list(seleccionado.technosphere()))

# La impresion realizada en la celda de arriba nos muestra la informacion necesaria para poder construir las matrices. Sin embargo, brightway nos permite manipular el `exchange` y acceder a su metadata.

# Seleccionamos el segundo `exchange`de la lista
exchange = list(seleccionado.technosphere())[1]
print(exchange.as_dict())

# ## Opciones de busqueda
# Como podran imaginar, manipular una base de datos con tantas actividades (~21k) es bastante complicado. Podemos utilizar funciones nativas de python para realizar una busqueda.

for x in ei:
  if x['name'] == 'transport, freight, lorry >32 metric ton, EURO5':
    print(x)

# truck = [x for x in ei if x['name'] == 'transport, freight, lorry >32 metric ton, EURO5'][0]
# truck

# Esta manera de buscar es mas 'pythonic'. Sin embargo, tambien puedes usar el buscador de brightway a traves de la funcion `search`.

ei.search('transport, freight RoW >32 EURO5')

ei.search?? # La funcion search prioriza algunos campos para hacer el filtro.

# # Introduccion a brightway - pt. 3
#
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion:
#
# https://docs.brightway.dev/en/latest/index.html

# ## Explorando las matrices
# Ahora que sabemos como crear un actividad y metodos desde cero. Podemos concentrarnos en manipular las actividades que estan presentes en ecoinvent.
# Para esta parte usaremos un proyecto que hemos preparado para ustedes que contiene una biosfera y tecnosfera compatible con ecoinvent v3.9

import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print


# Tenemos dos bases de datos
bd.databases

# seleccionamos la base de datos ecoinvent y una actividad que tomaremos de ejemplo
ei = bd.Database("ecoinvent-3.9.1-cutoff")
harina = ei.search('fishmeal PE 65-67')[0]
harina

# Elegimos un metodo que ya esta instalado y hace un LCA pero nos detenemos en la etapa de LCI
method=('IPCC 2021', 'climate change', 'global warming potential (GWP100)')
lca = bc.LCA({harina:1},method=method) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida


# Recordemos que ecoinvent tiene 21238 actividades
# Entonces que dimensiones deberia tener la matriz de la tecnosfera?
lca.technosphere_matrix.toarray().shape

# Que dimensiones deberia tener el vector s?
lca.supply_array

# Si quisiera saber cuanto de 'anchoveta pescada en embarcaciones de madera'
# se requiere en TOTAL para producir 1 kg de harina de pescado...
anchoveta = ei.search('anchovy PE wooden')[1]
anchoveta

# el lca.activity_dict me permite ubicar una actividad en la matriz.
lca.supply_array[lca.activity_dict[anchoveta.id]]

# Ahora continuamos con el LCIA
lca.lcia() # Calcula los impactos
print("El impacto es: ", lca.score)

# ## Analisis de contribuciones
# Para entender las distintas contribuciones, tenemos que seguir utilizando el objeto LCA.
# Este objeto mantiene los resultados del ACV en memoria

# ### Procesos mas importantes
# Para listar los procesos que generan mas impactos utilizaremos el paquete `bw2analyzer` y `pandas`.

# +
import pandas as pd
import bw2analyzer as ba
# ba.ContributionAnalysis().annotated_top_processes(lca=lca) # dificil de visulizar
# ba.ContributionAnalysis.annotated_top_processes??

# +

pd.DataFrame(
    [(x, y, z["name"]) for x, y, z in ba.ContributionAnalysis().annotated_top_processes(lca=lca)],
    columns=["score", "quantity", "name"]
)
# -

# ### Emisiones mas importantes
# De manera similar, podemos obtener el ranking de flujos ambiental que generan mayores impactos

import pandas as pd
import bw2analyzer as ba
pd.DataFrame(
    [(x, y, z["name"]) for x, y, z in ba.ContributionAnalysis().annotated_top_emissions(lca=lca)],
    columns=["score", "quantity", "name"]
)


# La importancia de las emisiones en el impacto tiene que ver con la cantidad y con los factores de caracterizacion.
# Podemos listar estos factores para revisarlos

for key, cf in bd.Method(method).load():
    # print(key, cf)
    print(bd.get_node(id=key), "CF: ",cf)


# ## Analisis de incertidumbre
# Realizar simulaciones de Monte Carlo es tan facil que requiere modificar una sola linea de la clase LCA.

# +
lca = bc.LCA(
    {harina:1},
    method=method,
    use_distributions=True # Esto es nuevo
) # Instancia la clase

# El objeto LCA es ahora un 'generator'.
# Es decir que podemos iterarlo las veces que necesitemos



# +
# Avanzamos un paso
next(lca)

results= []
# iteramos 50 veces, es decir muestreamos 100 veces.
for i in range(50):
    lca.lci()
    lca.lcia()
    results.append(lca.score)
    next(lca)
# -

# Tenemos una lista de resultados
# que, en promedio deberia aproximarse a 0.44
results

# Podemos utilizar el paquete `seaborn` para visualizar la dispersion de los impactos
import seaborn as sns
sns.histplot(results)



