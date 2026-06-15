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
# %% [markdown]
# # Descripción del problema: Producción de Manzanas en Alemania
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
# He utilizado un lenguaje para generar diagramas llamado mermaid:
# https://mermaid.live/edit#pako:eNpVkcFygjAQhl8ls2e0IUBQpuOMFb1pe-ipwCElK2aExAlh2ur4VH2EvliROm3NKbvffv8e9gSlkQgJkG1t3sqdsI48p7kmlzfPVmidqtVRaIf3r_ZutlHOCmeIRDJvjFamIKPRjKTZkzWyK0v19al7OMz6ZF-RtdC9LdrimvmQPWHrVKmkuKpXsMhShS3Wt910qJbZslGtMhpbsnhkxQ1c_YMbImrSdlibAjyorJKQbEXdogcN2kZcajhd9BzcDhvMIem_Uth9Drk-99JB6BdjGkic7XrNmq7a_YZ0BykcpkpUVvyNoJZoF6bTDhI_mAwZkJzgHRIWTscBD-PYD-iU8igOPPjo2z4dRyH3I8YZDUM64WcPjsPaHkwnMWURj33GOWXMA5TKGbv-udRwsPM3zCWGMA
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
# %%
# Instalamos las dependencias necesarias
# %%
!pip install bw2calc -q # Paquete de brightway
!pip install bw2data -q # Paquete de brightway
!pip install bw2io -q # Paquete de brightway
!pip install polars -q
!pip install pypardiso -q
!pip install seaborn -q

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
drive.CreateFile({"id": "1271F7TWk4DNGgg7XfsH0iyZVoOJ-PHJe"}).GetContentFile(
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
ei = bd.Database("ecoinvent-3.11-cutoff")
# Set the current project
bio = bd.Database("ecoinvent-3.11-biosphere")

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
fertilizer = ei.get("053ace20581bb34ddb30e49b357171e7")
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
pesticide = ei.get("73459e045fb27f5732eb10a8a79d57de")
print(pesticide.as_dict())

# %%
manzana_alemania.new_exchange(
    amount=0.000084,  # 3.36 kg/ha con 40 t/ha de rendimiento
    type="technosphere",
    input=pesticide,
).save()

# %%
# Me tomé la libertad de elegir una actividad que genera 1kg de diesel.
diesel = ei.get("7c1cbc3b02edae82503191858228ba5f")

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
        "EF v3.1" in method[1]
    ):  # Queremos identificar todos los métodos del Environmental Footprint Methodology.
        print(method)


# %%
metodo_1 = (
    "ecoinvent-3.11",
    "EF v3.1",
    "climate change",
    "global warming potential (GWP100)",
)
# Calculamos el impacto
lca_cc = bc.LCA({manzana_alemania: 1}, method=metodo_1)  # Instancia la clase
lca_cc.lci()  # calcula el inventario de ciclo de vida
lca_cc.lcia()  # Calcula los impactos
print("El impacto de Cambio Climático (kg CO2eq) es:")
print(lca_cc.score)
# %%
# Ahora para la acidificación
metodo_2 = (
    "ecoinvent-3.11",
    "EF v3.1",
    "eutrophication: freshwater",
    "fraction of nutrients reaching freshwater end compartment (P)",
)
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

# Tambien podemos convertir en analisis de contribuciones en un dataframe

print(
    pd.DataFrame(
        [
            (x, y, z["name"])
            for x, y, z in ba.ContributionAnalysis().annotated_top_emissions(lca=lca_cc)
        ],
        columns=["score", "quantity", "name"],
    )
)

# %%
calculations = ba.utils.recursive_calculation_to_object(
    manzana_alemania, lcia_method=metodo_1
)
# %%
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.sankey import Sankey


def plot_sankey_tree(
    data: List[Dict[str, Any]],
    title: str = "LCA Contribution Tree",
    value_field: str = "fraction",
    height: int = 800,
    width: int = 1200,
    use_plotly: bool = True,
    max_label_length: int = 50,
    min_fraction: float = 0.0,
    show_values: bool = True,
) -> None:
    """
    Plot a Sankey diagram showing the hierarchical tree structure of LCA contributions.

    The thickness of arrows represents the contribution (fraction) of each node to its parent.

    Parameters
    ----------
    data : List[Dict[str, Any]]
        List of dictionaries, each representing a node in the tree with keys:
        - 'label': unique identifier for the node
        - 'parent': label of parent node (None for root)
        - 'score': impact score
        - 'fraction': contribution to total impact (used for arrow thickness)
        - 'name': descriptive name of the activity
        - 'amount': amount value
        - 'key': unique key tuple
    title : str, optional
        Title of the diagram (default: "LCA Contribution Tree")
    value_field : str, optional
        Field to use for link values ('fraction' or 'score') (default: "fraction")
    height : int, optional
        Height of the figure in pixels (default: 800)
    width : int, optional
        Width of the figure in pixels (default: 1200)
    use_plotly : bool, optional
        If True, use Plotly; if False, use matplotlib (default: True)
    max_label_length : int, optional
        Maximum length for node labels (default: 50)
    min_fraction : float, optional
        Minimum fraction to display (filter small contributions) (default: 0.0)
    show_values : bool, optional
        Whether to show values in labels (default: True)

    Returns
    -------
    None
        Displays the Sankey diagram

    Examples
    --------
    >>> data = [
    ...     {'label': 'root', 'parent': None, 'score': 62.29, 'fraction': 1.0,
    ...      'amount': 1.0, 'name': 'Bicycle, conventional, urban, 2020',
    ...      'key': ('bafu', '522701.0')},
    ...     {'label': 'root_a', 'parent': 'root', 'score': 56.58, 'fraction': 0.908,
    ...      'amount': 0.706, 'name': 'Bicycle, at regional storage',
    ...      'key': ('bafu', '291950.0')},
    ... ]
    >>> plot_sankey_tree(data)
    """

    if use_plotly:
        _plot_sankey_plotly(
            data,
            title,
            value_field,
            height,
            width,
            max_label_length,
            min_fraction,
            show_values,
        )
    else:
        _plot_sankey_matplotlib(
            data,
            title,
            value_field,
            height,
            width,
            max_label_length,
            min_fraction,
            show_values,
        )


def _plot_sankey_plotly(
    data: List[Dict[str, Any]],
    title: str,
    value_field: str,
    height: int,
    width: int,
    max_label_length: int,
    min_fraction: float,
    show_values: bool,
) -> None:
    """Internal function to plot Sankey diagram using Plotly."""

    # Filter data by minimum fraction
    filtered_data = [node for node in data if node.get("fraction", 0) >= min_fraction]

    if not filtered_data:
        print("No data to display after filtering.")
        return

    # Create a mapping from label to index
    label_to_idx = {node["label"]: idx for idx, node in enumerate(filtered_data)}

    # Prepare node labels
    node_labels = []
    for node in filtered_data:
        name = node["name"]
        if len(name) > max_label_length:
            name = name[: max_label_length - 3] + "..."

        if show_values:
            label = f"{name}<br>({node['fraction'] * 100:.1f}%)"
        else:
            label = name

        node_labels.append(label)

    # Prepare links (edges from parent to child)
    sources = []
    targets = []
    values = []
    link_labels = []

    for node in filtered_data:
        if node["parent"] is not None:
            # Check if parent exists in filtered data
            if node["parent"] in label_to_idx:
                parent_idx = label_to_idx[node["parent"]]
                child_idx = label_to_idx[node["label"]]

                sources.append(parent_idx)
                targets.append(child_idx)

                # Use specified field for link value
                value = node.get(value_field, node.get("fraction", 0))
                values.append(value)

                # Create hover text for link
                link_label = f"{node['name'][:30]}<br>Fraction: {node['fraction'] * 100:.2f}%<br>Score: {node['score']:.2f}"
                link_labels.append(link_label)

    # Create color scale based on fraction
    node_colors = []
    for node in filtered_data:
        fraction = node["fraction"]
        # Color gradient from light blue (low) to dark red (high)
        if fraction > 0.5:
            color = f"rgba(220, 20, 60, {0.3 + fraction * 0.7})"  # Crimson
        elif fraction > 0.1:
            color = f"rgba(255, 140, 0, {0.3 + fraction * 0.7})"  # Dark orange
        else:
            color = f"rgba(70, 130, 180, {0.3 + fraction * 0.7})"  # Steel blue
        node_colors.append(color)

    # Create link colors (lighter versions, with transparency)
    link_colors = []
    for target_idx in targets:
        node = filtered_data[target_idx]
        fraction = node["fraction"]
        if fraction > 0.5:
            color = "rgba(220, 20, 60, 0.2)"  # Light crimson
        elif fraction > 0.1:
            color = "rgba(255, 140, 0, 0.2)"  # Light orange
        else:
            color = "rgba(70, 130, 180, 0.2)"  # Light steel blue
        link_colors.append(color)

    # Create the Sankey diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=node_labels,
                    color=node_colors,
                    hovertemplate="%{label}<br>Score: %{value:.2f}<extra></extra>",
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                    hovertemplate="%{label}<extra></extra>",
                    customdata=link_labels,
                ),
                orientation="h",
                arrangement="snap",
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family="Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        font=dict(size=12),
        height=height,
        width=width,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig.show()


def _plot_sankey_matplotlib(
    data: List[Dict[str, Any]],
    title: str,
    value_field: str,
    height: int,
    width: int,
    max_label_length: int,
    min_fraction: float,
    show_values: bool,
) -> None:
    """
    Internal function to plot Sankey diagram using Matplotlib.

    Note: Matplotlib's Sankey is more limited and works best for simpler diagrams.
    For complex hierarchical trees, consider using Plotly instead.
    """

    # Filter data by minimum fraction
    filtered_data = [node for node in data if node.get("fraction", 0) >= min_fraction]

    if not filtered_data:
        print("No data to display after filtering.")
        return

    # Note: Matplotlib's Sankey is designed for flow diagrams, not hierarchical trees
    # This is a simplified implementation
    print("Warning: Matplotlib's Sankey has limited support for hierarchical trees.")
    print("For better results, use use_plotly=True")

    fig, ax = plt.subplots(figsize=(width / 100, height / 100))

    # Build tree level by level
    root = None
    for node in filtered_data:
        if node["parent"] is None:
            root = node
            break

    if root is None:
        print("No root node found.")
        return

    # Simple visualization: just show top-level contributions
    children = [node for node in filtered_data if node["parent"] == root["label"]]

    if not children:
        print("No children found for root node.")
        return

    # Sort children by fraction (descending)
    children.sort(key=lambda x: x["fraction"], reverse=True)

    # Create a simple Sankey diagram for one level
    sankey = Sankey(ax=ax, scale=0.01, offset=0.3, head_angle=120)

    # Calculate flows
    flows = []
    labels = []
    orientations = []

    # Input flow (root)
    flows.append(1.0)
    root_name = root["name"][:max_label_length]
    if show_values:
        labels.append(f"{root_name}\n{root['fraction'] * 100:.1f}%")
    else:
        labels.append(root_name)
    orientations.append(0)

    # Output flows (children)
    for child in children[:10]:  # Limit to top 10 for readability
        flows.append(-child["fraction"])
        child_name = child["name"][:max_label_length]
        if show_values:
            labels.append(f"{child_name}\n{child['fraction'] * 100:.1f}%")
        else:
            labels.append(child_name)
        orientations.append(1)

    # Add remaining as "others" if needed
    if len(children) > 10:
        remaining = sum(c["fraction"] for c in children[10:])
        flows.append(-remaining)
        labels.append(f"Others\n{remaining * 100:.1f}%")
        orientations.append(1)

    sankey.add(
        flows=flows,
        labels=labels,
        orientations=orientations,
        pathlengths=[0.25] * len(flows),
    )

    diagrams = sankey.finish()

    plt.title(title, fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()


def print_tree_structure(
    data: List[Dict[str, Any]],
    max_depth: Optional[int] = None,
    min_fraction: float = 0.0,
) -> None:
    """
    Print the tree structure in a readable text format.

    Parameters
    ----------
    data : List[Dict[str, Any]]
        List of dictionaries representing the tree nodes
    max_depth : int, optional
        Maximum depth to display (None for all levels)
    min_fraction : float, optional
        Minimum fraction to display (default: 0.0)
    """

    # Filter by minimum fraction
    filtered_data = [node for node in data if node.get("fraction", 0) >= min_fraction]

    # Build parent-to-children mapping
    children_map = {}
    root = None

    for node in filtered_data:
        parent = node.get("parent")
        if parent is None:
            root = node
        else:
            if parent not in children_map:
                children_map[parent] = []
            children_map[parent].append(node)

    # Sort children by fraction (descending)
    for children_list in children_map.values():
        children_list.sort(key=lambda x: x["fraction"], reverse=True)

    def print_node(node, depth=0, prefix=""):
        """Recursively print node and its children."""
        if max_depth is not None and depth > max_depth:
            return

        indent = "  " * depth
        fraction_pct = node["fraction"] * 100
        score = node["score"]
        name = node["name"]

        print(f"{indent}{prefix}{name}")
        print(f"{indent}  └─ Fraction: {fraction_pct:.2f}% | Score: {score:.2f}")

        # Print children
        label = node["label"]
        if label in children_map:
            for i, child in enumerate(children_map[label]):
                is_last = i == len(children_map[label]) - 1
                child_prefix = "└─ " if is_last else "├─ "
                print_node(child, depth + 1, child_prefix)

    if root:
        print("\n" + "=" * 80)
        print("LCA CONTRIBUTION TREE")
        print("=" * 80 + "\n")
        print_node(root)
        print("\n" + "=" * 80)
    else:
        print("No root node found in data.")


# %%
plot_sankey_tree(calculations)
