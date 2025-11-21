# %% [markdown]

# 🚧 Ejercicios de Inventarios de Ciclo de Vida
#
# A continuación encontrarás 6 ejercicios para practicar la construcción de inventarios de ACV.
# Cada caso presenta un producto diferente con datos realistas pero aproximados para el análisis.

# %% [markdown]

# ## Ejercicio 1: Producción de Bicicletas
#
#     El negocio de las bicicletas sigue en aumento y es momento que consideres aumentar la producción. Eres consciente que si deseas llegar a más mercados, deberás proporcionar más información a los mayoristas, sobretodo en el aspecto ambiental
#     Los ingenieros han sugerido considerar la importación de aluminio chino e incluso llevar las plantas de producción a china.
#     Tu trabajo es construir dos modelos y explorar las posibles diferencias entre producir bicicletas en Perú y producirlas en China.
#     Debes considerar lo siguiente:
#
#     Los consumos estimados por bicicleta son:
#
#         345 kwh de energía
#         5 kg de acero
#         25 kg de aluminio
#         El producto final pesa 24kgs
#         Se consumen alrededor de 15 litros diesel

# %% [markdown]

# ## Ejercicio 2: Fabricación de Laptops
#
#     Una empresa tecnológica está evaluando la huella ambiental de sus laptops para cumplir con regulaciones europeas.
#     Necesitas comparar la producción en dos ubicaciones: una fábrica en Malasia y otra en México.
#     La empresa busca certificación ambiental y requiere un análisis detallado del inventario de materiales.
#
#     Los consumos estimados por laptop son:
#
#         180 kwh de energía eléctrica
#         2.5 kg de plásticos diversos (ABS, PC)
#         0.8 kg de aluminio para carcasa
#         0.15 kg de cobre para circuitos
#         0.05 kg de oro y metales preciosos
#         El producto final pesa 1.8 kg
#         Se consumen 8 litros de agua en procesos de enfriamiento

# %% [markdown]

# ## Ejercicio 3: Producción de Paneles Solares
#
#     Una startup de energía renovable quiere expandirse a mercados latinoamericanos y necesita evaluar
#     el impacto ambiental de sus paneles solares fotovoltaicos.
#     Están considerando establecer producción local en Colombia versus importar desde Alemania.
#     El análisis debe incluir tanto la fabricación como el transporte hasta el usuario final.
#
#     Los consumos estimados por panel solar (300W) son:
#
#         520 kwh de energía durante fabricación
#         12 kg de silicio purificado
#         15 kg de vidrio templado
#         8 kg de aluminio para marco
#         2 kg de polímeros (EVA, backsheet)
#         El producto final pesa 22 kg
#         Se consumen 25 litros de químicos de limpieza

# %% [markdown]

# ## Ejercicio 4: Fabricación de Botellas de Vidrio
#
#     Una empresa de bebidas artesanales busca reducir su impacto ambiental y está evaluando
#     cambiar de botellas plásticas a botellas de vidrio reutilizables.
#     Necesitan comparar la producción de botellas de vidrio reciclado versus vidrio virgen,
#     considerando que las botellas tendrán un ciclo de vida de 15 reutilizaciones promedio.
#
#     Los consumos estimados por botella de vidrio (500ml) son:
#
#         0.8 kwh de energía para fusión
#         0.45 kg de arena sílica (o vidrio reciclado equivalente)
#         0.05 kg de carbonato de sodio
#         0.02 kg de caliza
#         El producto final pesa 0.35 kg
#         Se consumen 2 litros de agua para enfriamiento

# %% [markdown]

# ## Ejercicio 5: Producción de Camisetas de Algodón
#
#     Una marca de ropa sostenible quiere cuantificar el impacto de sus camisetas básicas.
#     Están evaluando tres opciones: algodón convencional de India, algodón orgánico de Perú,
#     y una mezcla de algodón reciclado producido en Turquía.
#     El análisis debe incluir el cultivo/reciclaje, hilado, tejido, teñido y confección.
#
#     Los consumos estimados por camiseta son:
#
#         12 kwh de energía total del proceso
#         0.25 kg de fibra de algodón
#         0.03 kg de tintes y químicos
#         0.01 kg de hilos auxiliares
#         El producto final pesa 0.18 kg
#         Se consumen 150 litros de agua en procesos húmedos

# %% [markdown]

# ## Ejercicio 6: Fabricación de Ladrillos Cerámicos
#
#     Una constructora está implementando criterios de construcción sostenible y necesita evaluar
#     diferentes tipos de ladrillos para sus proyectos habitacionales.
#     Quieren comparar ladrillos tradicionales de arcilla versus ladrillos con contenido reciclado,
#     ambos producidos en hornos con diferentes combustibles (gas natural vs. biomasa).
#
#     Los consumos estimados por ladrillo estándar son:
#
#         1.2 kwh de energía térmica para cocción
#         2.8 kg de arcilla y agregados
#         0.2 kg de combustible (gas natural o biomasa)
#         El producto final pesa 2.5 kg
#         Se consumen 0.8 litros de agua para moldeo
#         Genera aproximadamente 1.1 kg de CO₂ por combustión

# %% [markdown]

# Para cada ejercicio, debes:
# 1. Definir claramente la unidad funcional
# 2. Establecer los límites del sistema
# 3. Crear el inventario de entradas y salidas utilizando Brightway
# 4. Considerar los procesos de transporte cuando sean relevantes. Se pueden utilizar distancias aproximadas en barco, avion o transporte terrestre.
# 5. Realizar el analisis para 2 de las categorias del metodo EF v3.1
# 6. Analizar los resultados y proponer alternativas de mejora basadas en los resultados
