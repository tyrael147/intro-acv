# %%
# Instalamos las dependencias necesarias
# !pip install bw2calc -q # Paquete de brightway
# !pip install bw2data -q # Paquete de brightway
# !pip install bw2io -q # Paquete de brightway
# !pip install bw2analyzer # Paquete de brightway
# !pip install pandas -q
# !pip install pypardiso -q
# !pip install mermaid-py -q # Este paquete permite construir diagramas. Lo usaré para el reporte.
# !pip install seaborn -q


# %% [markdown]
# Debemos descargar un archivo de respaldo que contiene BAFU. Para ello tenemos que autenticar nuestro usuario de **gmail** que fue creado anteriormente.

# %%
from google.colab import auth
from oauth2client.client import GoogleCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
drive.CreateFile({"id": "1t3qNmOuOgCvT9B6dEmnJVzEspCHspDAT"}).GetContentFile(
    "backup.tar.gz"
)

# %% [markdown]
# Verificamos

# %%
# !du -hs backup.tar.gz

# %%
import bw2calc as bc
import bw2data as bd
import bw2io as bi
import pandas as pd
import bw2analyzer as ba
from rich import print

# %% [markdown]
# ### Importar el backup del proyecto
# Esta modalidad no requiere mucha explicación: El proyecto se carga nuevamente.

# %%
bi.restore_project_directory(
    "backup.tar.gz",  # nombre del archivo, creado celdas arriba
    project_name="proyecto_bafu",  # Se puede elegir un nombre nuevo para el proyecto
    overwrite_existing=True,
)
# %%
# Seleccionamos el proyecto correspondiente y asignamos las bases de datos a cada variable
bd.projects.set_current("proyecto_bafu")
bafu_db = bd.Database("bafu")
# Set the current project
bio = bd.Database("biosphere3")

# %% [markdown]
# ### Explorando BAFU

# %%
bd.projects.set_current("proyecto_bafu")
seleccionado = bafu_db.random() # Explora las actividades
print("Proceso aleatorio seleccionado: ",seleccionado)
# Primero exploramos los keys de la actividad seleccionada
print(list(seleccionado.keys()))

# %%
# Podemos ver el contenido de todo el dataset.
print(seleccionado.as_dict())

# %% [markdown]
# Como pueden notar, el contenido de la actividad BAFU es bastante rica. Existen campos fuera de `name`, `code`,`location` y `unit` que son nuevos para nosotros, lo que demuestra que brightway es lo suficientemente flexible al definir una actividad.
#
# Lo que vimos en la celda anterior describe a una actividad, pero aun no describe sus conexiones (`exchanges`). Para acceder a ellas, hay que utilizar las funciones `exchanges`, `technosphere` o `biosphere`, segun lo que se desee observar.

# %%
# `exchanges` retorna un objeto the brightway que no es nativo de python
type(seleccionado.exchanges())

# %%
# Si deseamos leerlo al estilo de una lista, hay que convertirlo en una lista.
for exchange in seleccionado.exchanges():
    print(exchange)
# print(list(seleccionado.exchanges()))

# %%
# Si deseamos solo la tecnosfera, usamos la funcion correspondiente
for exchange in seleccionado.technosphere():
    print(exchange)

# %% [markdown]
# La impresion realizada en la celda de arriba nos muestra la informacion necesaria para poder construir las matrices. Sin embargo, brightway nos permite manipular el `exchange` y acceder a su metadata.

# %%
# Seleccionamos el segundo `exchange`de la list
# a
exchange = list(seleccionado.technosphere())[1]
print(exchange.as_dict())

# %% [markdown]
# ## Opciones de busqueda
# Como podran imaginar, manipular una base de datos con tantas actividades (~11k) es bastante complicado. Podemos utilizar funciones nativas de python para realizar una busqueda.

# %%
for x in bafu_db:
  if 'Bicycle' in x['name']:
    print(x)

# %%
# Para quienes esten comodos con python, pueden utilizar list-comprehension, and select the
bicycle = [x for x in bafu_db if 'Bicycle' in x['name']]
print(bicycle)
# truck

# %% [markdown]
# Esta manera de buscar es mas 'pythonic'. Sin embargo, tambien puedes usar el buscador de brightway a traves de la funcion `search`.

# %%
bafu_db.search('Bicycle')

# %%
bafu_db.search?? # La funcion search prioriza algunos campos para hacer el filtro.

# %% [markdown]
# # Introduccion a brightway - Under the hood
#
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion:
#
# https://docs.brightway.dev/en/latest/index.html

# %% [markdown]
# ## Explorando las matrices
# Ahora que sabemos como crear un actividad y metodos desde cero. Podemos concentrarnos en manipular las actividades que estan presentes en BAFU.
# Para esta parte usaremos un proyecto que hemos preparado para ustedes que contiene una biosfera y tecnosfera compatible con BAFU v2

# %%
# Re-import for this section if running independently
import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print

# %% [markdown]
# Tenemos dos bases de datos

# %%
bd.databases

# %%
# seleccionamos la base de datos bafu y una actividad que tomaremos de ejemplo
bicycle = bafu_db.search("Bicycle, conventional, urban, 2020")[-1]
bicycle

# %%
# Elegimos un metodo que ya esta instalado y hace un LCA pero nos detenemos en la etapa de LCI
method=('IPCC 2021', 'climate change', 'global warming potential (GWP100)')
lca = bc.LCA({bicycle:1},method=method) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida

# %% [markdown]
# La base de datos BAFU contiene actividades de la base de datos suiza
# Entonces que dimensiones deberia tener la matriz de la tecnosfera?

# %%
lca.technosphere_matrix.toarray().shape

# %% [markdown]
# Que dimensiones deberia tener el vector s?

# %%
lca.supply_array

# %% [markdown]
# Si quisiera saber cuanto de otra actividad específica
# se requiere en TOTAL para producir la unidad funcional...

# %%
# Ejemplo: buscar una actividad relacionada en la base de datos
otra_act = bafu_db.search('steel')[0]
otra_act

# %%
# el lca.activity_dict me permite ubicar una actividad en la matriz.
lca.supply_array[lca.activity_dict[otra_act.id]]

# %% [markdown]
# Ahora continuamos con el LCIA

# %%
lca.lcia() # Calcula los impactos
print("El impacto es: ", lca.score)

# %% [markdown]
# ## Analisis de contribuciones
# Para entender las distintas contribuciones, tenemos que seguir utilizando el objeto LCA.
# Este objeto mantiene los resultados del ACV en memoria

# %% [markdown]
# ### Procesos mas importantes
# Para listar los procesos que generan mas impactos utilizaremos el paquete `bw2analyzer` y `pandas`.

# %%
ba.ContributionAnalysis().annotated_top_processes(lca=lca) # dificil de visulizar
ba.ContributionAnalysis.annotated_top_processes??

# %%
pd.DataFrame(
    [(x, y, z["name"]) for x, y, z in ba.ContributionAnalysis().annotated_top_processes(lca=lca)],
    columns=["score", "quantity", "name"]
)

# %% [markdown]
# ### Emisiones mas importantes
# De manera similar, podemos obtener el ranking de flujos ambiental que generan mayores impactos

# %%
import pandas as pd
import bw2analyzer as ba
pd.DataFrame(
    [(x, y, z["name"]) for x, y, z in ba.ContributionAnalysis().annotated_top_emissions(lca=lca)],
    columns=["score", "quantity", "name"]
)

# %% [markdown]
# La importancia de las emisiones en el impacto tiene que ver con la cantidad y con los factores de caracterizacion.
# Podemos listar estos factores para revisarlos

# %%
for key, cf in bd.Method(method).load()[0:20]:
    # print(key, cf)
    print(bd.Database('biosphere3').get(key[1]), cf)



# %% [markdown]
# Pueden revisar
# La importancia de las emisiones en el impacto tiene que ver con la cantidad y con los factores de caracterizacion.
# Podemos listar estos factores para revisarlos

# %%
ba.print_recursive_calculation(bicycle,lcia_method=method)
