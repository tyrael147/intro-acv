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
