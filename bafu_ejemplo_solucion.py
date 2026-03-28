# %% [markdown]
#
# Ejemplo: Producción de Zanahorias en Suiza (Convencional vs. Orgánica)

# Este ejemplo es didáctico y muestra cómo se construye un Inventario de Ciclo de Vida (LCI) utilizando la base de datos BAFU (basada en ecoinvent).
# En este ejemplo simplificado, calcularemos el impacto ambiental de 1 kg de Zanahorias producidas en Suiza (CH) bajo dos esquemas agronómicos distintos.
#
# Debes calcular el Impact de cambio climatico y comparar ambas opciones.
#
# ## SISTEMA 1: PRODUCCIÓN CONVENCIONAL DE ZANAHORIA (SUIZA)
# El rendimiento promedio estimado es de 50 t (50,000 kg) de zanahorias por hectárea.
# Esta información agronómica fue recolectada (por hectárea):
#  - Consumo de fertilizantes sintéticos: 100 kg N/ha, 50 kg P2O5/ha, 150 kg K2O/ha
#  - Consumo de diésel para maquinaria (siembra, labranza, cosecha): 300 L/ha (aprox. 10,800 MJ/ha)
#  - Aplicación de pesticidas sintéticos: 2 kg/ha
#
# ## SISTEMA 2: PRODUCCIÓN ORGÁNICA DE ZANAHORIA (SUIZA)
#
#  El rendimiento suele ser menor en sistemas orgánicos, estimado en 20 t (20,000 kg) de zanahorias por hectárea.
#  Esta información agronómica fue recolectada (por hectárea):
#  - Se aplican 25 t/ha de estiércol o compost orgánico.
#  - Consumo de diésel para maquinaria: 350 L/ha (aprox. 12,600 MJ/ha). El consumo es ligeramente mayor debido al uso intensivo de maquinaria para el control mecánico de malezas (deshierbe mecánico) ante la ausencia de herbicidas.
#
# %% [markdown]
#
# ## Pistas ;)
# Considera buscar estos terminos:
# - Para el combustible: Diesel, burned in agricultural machine
# - Para fertilizantes: Average mineral fertiliser
# - Para pesticidas: Pesticide unspecified
# - Para fertilizante organico: Green manure organic, until January (cuidado con las unidades)


# %%
# Instalamos las dependencias necesarias
# %%
# !pip install bw2calc -q # Paquete de brightway
# !pip install bw2data -q # Paquete de brightway
# !pip install bw2io -q # Paquete de brightway
# !pip install bw2analyzer # Paquete de brightway
# !pip install pandas -q
# !pip install pypardiso -q
# !pip install mermaid-py -q # Este paquete permite construir diagramas. Lo usaré para el reporte.
# !pip install seaborn -q


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
bio = bd.Database("biosphere3")

# %%
diesel = bafu_db.search("Diesel, burned in agricultural machine")[0]
n_fertiliser = bafu_db.search("Average mineral fertiliser, as N")[0]
p_fertiliser = bafu_db.search("Average mineral fertiliser, as P2O5")[0]
k_fertiliser = bafu_db.search("Average mineral fertiliser, as K2O")[0]
pesticide = bafu_db.search("Pesticide unspecified")[0]
manure = bafu_db.search("Green manure organic, until January")[
    0
]  # O estiércol equivalente

print([diesel, n_fertiliser, p_fertiliser, k_fertiliser, pesticide, manure])
# %%

# Elimina los datasets para tener un inicio limpio
try:
    _ = bafu_db.get("carrot_conv_ch")
    _.delete()
except:
    pass

try:
    _ = bafu_db.get("carrot_org_ch")
    _.delete()
except:
    pass


# SISTEMA 1: Zanahoria Convencional (Suiza)
# Rendimiento: 50,000 kg/haa

yield_conv = 50000.0

carrot_conv = bafu_db.new_activity(
    code="carrot_conv_ch",
    name="Carrots conventional, at farm",
    location="CH",
    unit="kilogram",
    type="processwithreferenceproduct",
)
carrot_conv.save()

# Añadiendo inputs desde la tecnosfera (divididos por el rendimiento para reflejar 1 kg)
carrot_conv.new_exchange(
    input=n_fertiliser, amount=(100.0 / yield_conv), type="technosphere"
).save()
carrot_conv.new_exchange(
    input=p_fertiliser, amount=(50.0 / yield_conv), type="technosphere"
).save()
carrot_conv.new_exchange(
    input=k_fertiliser, amount=(150.0 / yield_conv), type="technosphere"
).save()
carrot_conv.new_exchange(
    input=pesticide, amount=(2.0 / yield_conv), type="technosphere"
).save()
# 300 Litros de diésel equivalen a ~10800 Megajoules (tomando factor 36 MJ/L)
carrot_conv.new_exchange(
    input=diesel, amount=(10800.0 / yield_conv), type="technosphere"
).save()


# SISTEMA 2: Zanahoria Orgánica (Suiza)
# Rendimiento: 20,000 kg/ha

yield_org = 20000.0

carrot_org = bafu_db.new_activity(
    code="carrot_org_ch",
    name="Carrots organic, at farm",
    location="CH",
    unit="kilogram",
    type="processwithreferenceproduct",
)
carrot_org.save()

# 25,000 kg de abono orgánico/compost
carrot_org.new_exchange(
    input=manure, amount=(1 / yield_org), type="technosphere"
).save()
# 350 Litros de diésel equivalen a ~12600 Megajoules (mayor uso por deshierbe mecánico)
carrot_org.new_exchange(
    input=diesel, amount=(12600.0 / yield_org), type="technosphere"
).save()

print("--------Convencional-----------")
for exc in carrot_conv.technosphere():
    print(exc)

print("--------Organico-----------")
for exc in carrot_org.technosphere():
    print(exc)
# %%
method = ("IPCC 2021", "climate change", "global warming potential (GWP100)")
lca = bc.LCA({carrot_conv: 1}, method=method)  # Instancia la clase
lca.lci()  # calcula el inventario de ciclo de vida
lca.lcia()
print(f"Impacto CC concenvional: {lca.score}")
# %%
method = ("IPCC 2021", "climate change", "global warming potential (GWP100)")
lca = bc.LCA({carrot_org: 1}, method=method)  # Instancia la clase
lca.lci()  # calcula el inventario de ciclo de vida
lca.lcia()
print(f"Impacto CC organic: {lca.score}")
