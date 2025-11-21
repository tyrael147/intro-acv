# %% [markdown]
#
# # Ejemplo: Producción de Manzanas en Alemania
# Este ejemplo es didáctico y muestra cómo se construye un Inventario de Ciclo de Vida utilizando la base de datos Ecoinvent.
# En este ejemplo trivial, buscamos calcular el impacto ambiental de 1 kg de Manzanas producidas en Alemania.
# El rendimiento es de 40 t de manzanas por hectárea.
# Esta información fue recolectada:
# Consumo de fertilizantes: 80 kg N/ha
# Consumo de diesel para la maquinaria: 435 L/ha
# Aplicación de pesticidas 3.36 kg/ha
#
# %%
# Instalamos las dependencias necesarias
# %%
# !pip install bw2calc>=2.1 -q # Paquete de brightway
# !pip install bw2data>=4.5 -q # Paquete de brightway
# !pip install bw2io>=0.9.11 -q # Paquete de brightway
# !pip install bw2analyzer # Paquete de brightway
# !pip install pandas -q
# !pip install pypardiso -q
# !pip install mermaid-py -q # Este paquete permite construir diagramas. Lo usaré para el reporte.
# !pip install seaborn>=0.13.2 -q

# %% [markdown]
# <div class="alert alert-block alert-warning">
# ⚠️ Debes restaurar la sesión!
# </div>

# %% [markdown]
# Debemos descargar un archivo de respaldo que contiene ecoinvent. Para ello tenemos que autenticar nuestro usuario de **gmail** que fue creado anteriormente.

# %%
from google.colab import auth
from oauth2client.client import GoogleCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
drive.CreateFile({"id": "1E3wPUOuRp13ucuNmq3557EuT3mszlmHB"}).GetContentFile(
    "backup.tar.gz"
)

# %% [markdown]
# Verificamos

# %%
# !du -hs backup.tar.gz

# %%
from dotenv import load_dotenv

load_dotenv()
import bw2calc as bc
import bw2data as bd
from rich import print

# %% [markdown]
# ### Importar el backup del proyecto
# Esta modalidad no requiere mucha explicación: El proyecto se carga nuevamente.

# %%
bi.restore_project_directory(
    "backup.tar.gz",  # nombre del archivo, creado celdas arriba
    project_name="proyecto_ei",  # Se puede elegir un nombre nuevo para el proyecto
    overwrite_existing=True,
)
# %%
# Seleccionamos el proyecto correspondiente y asignamos las bases de datos a cada variable
bd.projects.set_current("proyecto_ei")
ei = bd.Database("ecoinvent-3.9.1-cutoff")
# Set the current project
bio = bd.Database("biosphere3")

# %%
# Creamos una base de datos nueva para nuestro ejemplo
if "manzana_db" in bd.databases:
    del bd.databases["manzana_db"]
manzana_db = bd.Database("manzana_db")
manzana_db.register()
# %%
list(manzana_db)
# %%
# Creamos una actividad llamada manzana_alemania
# Paso 2: Crear la actividad principal de producción de manzanas
manzana_alemania = manzana_db.new_activity(
    code="manzana_alemania",
    name="Producción de manzanas, frescas, en Alemania",
    location="DE",
    unit="kilogram",
    type="processwithreferenceproduct",
)
# Guardar la actividad principal
manzana_alemania.save()

# %%
# %% [markdown]
# ### Buscamos las actividades que deseemos conectar
# %%
# En este caso, deseo buscar una actividad que represente el consumo de nitrato de amonio como fertilizante
print(
    "------Actividad------, -------Producto de referencia ------------,-----CÓDIGO--------"
)
for found in ei.search("ammonium nitrate"):
    print(f"{found} , {found['reference product']}, {found['code']}")

# %%
# Ahora elegimos el segundo elemento de la lista (index 1) ya que hace referencia a ReR (Rest of Europe).
# Elegimos Rest of Europe ya que es la mejor aproximación a `Alemania`.
# Podemos ver el contenido para verificar que es la actividad que queremos incluir como entrada.
fertilizer = ei.get("78a08d1a028eef23c65c9475010c14bd")
# Como verán, 1kg de esta urea contiene alrededor de 0.301 kg de Nitrógeno N
# Tomado de los comentarios...
# " ... If 1 kg of this 'urea ammonium nitrate mix' is used as fertiliser, it is equivalent to circa 0.301 kg of Nitrogen as N ..."
print(fertilizer.as_dict())
# %%
manzana_alemania.new_exchange(
    amount=0.002,  # 80 kg N/ha con rendimiento de 40 t/ha de manzanas.
    type="technosphere",
    input=fertilizer,
).save()


# %%
# Repetimos el mismo ejercicio de búsqueda para el caso del pesticida.
print(
    "------Actividad------, -------Producto de referencia ------------,-----CÓDIGO--------"
)
for found in ei.search("pesticide"):
    print(f"{found} , {found['reference product']}, {found['code']}")
# %%
# Elegimos el pesticida producido en RER.
pesticide = ei.get("1c5c182327d3b34ec6a3db5024e60d1a")
print(pesticide.as_dict())

# %%
manzana_alemania.new_exchange(
    amount=0.000084,  # 3.36 kg/ha con 40 t/ha de rendimiento
    type="technosphere",
    input=pesticide,
).save()

# %%
# Me tomé la libertad de elegir una actividad que genera 1kg de diesel.
diesel = ei.get("dd036517891922c427be648943a735a3")

# Diesel
manzana_alemania.new_exchange(
    amount=0.0090806,  # 435 L/ha con 40 t/ha rendimiento, densidad del diesel 0.835 kg/L
    type="technosphere",
    input=diesel,
).save()

# %%
# De igual forma, sabemos que la combustión de diesel genera emisiones de CO2
# En este caso hacemos la búsqueda en la biosfera.
print("------Actividad------, -----CÓDIGO--------")
for found in bio.search("carbon dioxide"):
    print(f"{found} , {found['code']}")
# %%
# Elegimos el primer elemento de la lista ya que las emisiones de CO2 son de origen fósil.
co2 = bio.get("349b29d1-3e58-4c66-98b9-9d1a076efd2e")
print(co2.as_dict())

# Emisiones de CO2 fósil
manzana_alemania.new_exchange(
    amount=0.024,  # Asumimos que todo el diesel se convierte en CO2, por estequiometría 1 kg de diesel se convierte en 2.68 kg de CO2
    type="biosphere",
    input=co2,
).save()


# %%
# Repetimos este ejercicio y consideramos las emisiones de nitrógeno al suelo producto de la aplicación de fertilizantes

n_soil = bio.get("b748f6f1-7061-4243-89c7-3f2d01dcec07")
manzana_alemania.new_exchange(
    amount=0.0004214,  # Asumimos de manera simplificada que el 70% del nitrógeno se pierde y termina en el suelo.
    # (0.002 * 0.301 * 0.7) -> cantidad de fertilizante * contenido de nitrógeno por kg * porcentaje de pérdida.
    type="biosphere",
    input=n_soil,
).save()

# %%
# Ahora vemos los flujos de nuestra actividad
print(list(list(manzana_db)[0].exchanges()))

# %% [markdown]
# # Métodos de Impacto
# Deseo analizar dos métodos de impacto: Cambio Climático y Acidificación, pero antes debemos saber el nombre exacto del método
# %%
# Un método es una tupla con la siguiente estructura: (<método>, <categoría de impacto>, <indicador>)
# Podemos explorar en la lista de métodos disponibles de esta manera:
for method in bd.methods:
    if (
        "EF v3.1" in method[0]
    ):  # Queremos identificar todos los métodos del Environmental Footprint Methodology.
        print(method)


# %%
metodo_1 = ("IPCC 2021", "climate change", "global warming potential (GWP100)")
# Calculamos el impacto
lca_cc = bc.LCA({manzana_alemania: 1}, method=metodo_1)  # Instancia la clase
lca_cc.lci()  # calcula el inventario de ciclo de vida
lca_cc.lcia()  # Calcula los impactos
print("El impacto de Cambio Climático (kg CO2eq) es:")
print(lca_cc.score)
# %%
# Ahora para la acidificación
metodo_2 = ("EF v3.1", "acidification", "accumulated exceedance (AE)")
lca_acid = bc.LCA({manzana_alemania: 1}, method=metodo_2)  # Instancia la clase
lca_acid.lci()  # calcula el inventario de ciclo de vida
lca_acid.lcia()  # Calcula los impactos
print("El impacto de Acidificación (mol H+ eq) es:")
print(lca_acid.score)
# %%
# Realizamos un análisis de contribuciones solo para el primer método como demostración.
import bw2analyzer as ba
import pandas as pd

print(
    pd.DataFrame(
        [
            (x, y, z["name"])
            for x, y, z in ba.ContributionAnalysis().annotated_top_processes(lca=lca_cc)
        ],
        columns=["score", "quantity", "name"],
    )
)


# %%
import bw2analyzer as ba
import pandas as pd

# Create the dataframe with emissions data
df = pd.DataFrame(
    [
        (x, y, z["name"])
        for x, y, z in ba.ContributionAnalysis().annotated_top_emissions(lca=lca_cc)
    ],
    columns=["score", "quantity", "name"],
)


# %% [markdown]
# Aquí pueden ver un ejemplo de cómo pueden reportar su código:
#
#
# # Reporte de Análisis de Ciclo de Vida: Producción de Manzanas en Alemania
#
# ## 1. Introducción
#
# ### 1.1 Unidad funcional
# Este inventario representa la producción de 1 kg de manzanas frescas producidas en Alemania.
# El rendimiento asumido es de 40 toneladas por hectárea.
#
# ### 1.2 Límites del sistema
# En este ejemplo simplificado, se han considerado únicamente los siguientes procesos:
# - Consumo de fertilizantes (nitrato de amonio): 80 kg N/ha
# - Consumo de diesel para maquinaria: 435 L/ha
# - Aplicación de pesticidas: 3.36 kg/ha
# - Emisiones directas de CO2 por combustión de diesel
# - Emisiones de nitrógeno al suelo por pérdidas de fertilizante
# %%
# Si desean, pueden importar una imagen en vez de diagramar directamente en el notebook.
import mermaid as md

render = md.Mermaid("""
    flowchart TD
         A[Fertilizante<br/>Nitrato de Amonio] --> D[Produccion de<br/>1 kg Manzanas]
         B[Pesticida] --> D
         C[Diesel] --> D
         D --> E[Emisiones CO2]
         D --> F[Emisiones N al suelo]

         classDef green fill:#90EE90
         class E,F green
""")
render

# %% [markdown]
#
# Los siguientes procesos fueron excluidos del sistema: infraestructura agrícola, transporte, procesamiento, empaque, irrigación, mano de obra, entre otros.
#
# ## 2. Inventario de Ciclo de Vida
#
# ### 2.1 Tecnosfera
# **Fertilizantes**: Se utilizó el proceso de producción de nitrato de amonio de la región RER (Rest of Europe). El consumo se calculó considerando que 1 kg de mezcla de nitrato de amonio equivale a 0.301 kg de nitrógeno.
#
# **Pesticidas**: Se utilizó el proceso genérico de producción de pesticidas de la región RER. El consumo se aproximó dividiendo la aplicación por hectárea entre el rendimiento.
#
# **Diesel**: Se seleccionó el proceso de producción de diesel considerando una densidad de 0.835 kg/L para la conversión de litros a kilogramos.
#
# ### 2.2 Biosfera
# **Dióxido de Carbono**: Este flujo se calculó usando estequiometría asumiendo que todo el diesel se convierte en CO2 (factor de 2.68 kg CO2/kg diesel).
#
# **Nitrógeno al suelo**: Se estimó que el 70% del nitrógeno aplicado como fertilizante se pierde y termina en el suelo.
#
# ## 3. Análisis de Impactos
#
# ### 3.1 Métodos seleccionados
# **Cambio climático**: Se eligió el método IPCC 2021 de cambio climático con potencial de calentamiento global a 100 años (GWP100). Este método considera los factores de caracterización más actualizados para gases de efecto invernadero.
#
# **Acidificación**: Se utilizó el método EF v3.1 (Environmental Footprint) para acidificación con el indicador de exceso acumulado (AE).
#
# ## 4. Resultados
#
# Para cambio climático, el impacto total es de aproximadamente 0.035 kg CO2eq por kg de manzana. El análisis de contribuciones indica que el proceso que más impacto directo genera es la producción de las manzanas misma, seguido por las emisiones asociadas al gas natural y la producción de diesel.
#
# La sustancia que más se emite es el dióxido de carbono fósil (2.64e-02 kg CO2eq), seguido por el metano fósil (3.47e-03 kg CO2eq).
#
# Los procesos con mayor contribución son:
# 1. Producción de manzanas (impacto total): 0.024 kg CO2eq
# 2. Venteo de gas natural: 0.003315 kg CO2eq
# 3. Producción de diesel: 0.001774 kg CO2eq
#
