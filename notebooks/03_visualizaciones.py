# 1. Imports
import pandas as pd #para leer y trabajar con los datos
import matplotlib.pyplot as plt # para crear gráficos personalizados
import seaborn as sns #para hacer gráficos chachi ;)
import os  # para manejo de carpetas y archivos y guardar graficos
from matplotlib.ticker import FuncFormatter # para dar formato personalizado a las etiquetas de los ejes en un gráfico de Matplotlib

# from IPython.display import Image, display
#_________________________________________


# 2. Funciones (cargar datos, gráficos)

# 2.1 Función para cargar datos  cargar_datos argumento: ruta_archivo
def cargar_datos(ruta_archivo):
  df = pd.read_csv(ruta_archivo)
  return df
# df = cargar_datos("./data/gastos_limpio.csv")

#__________________________________
# 2.2 guardar graficos
def guardar_grafico(figura, nombre_archivo):
  if not os.path.exists("output"):
      os.makedirs("output")
  ruta = os.path.join("output", nombre_archivo)
  figura.savefig(ruta, bbox_inches="tight")  # Guardar bien 
  plt.close(figura)  # Cerrar la figura bien


# 2.3 Función para visualizar el gasto total por comunidad

#______________________________________________________

def gasto_por_comunidad(df):
  # Excluir "Total Nacional" para centrarse solo en comunidades individuales
  df = df[
      (df["Tipo de dato"] == "Dato base") &
      (df["Grupos de gasto (2 dígitos)"] != "Índice general") &
      (df["Periodo"] == 2023) &
      (df["Comunidad autónoma de residencia"] != "Total Nacional") &
      (df["Gastos totales"] == "Gasto medio por persona")
  ]


 #  Agrupo el DataFrame por comunidad autónoma, sumo los valores en la columna "Total" para cada comunidad, y ordeno de mayor a menor.
  resumen = df.groupby("Comunidad autónoma de residencia")["Total"].sum().sort_values(ascending=False)
    
  # Eliminar los 3 primeros caracteres del nombre (código + espacio) para dejarlo limpio y bonito
  resumen.index = resumen.index.str[3:]

  fig, ax = plt.subplots(figsize=(12, 6))  # cambio aquí para usar figura explícita y eje
  sns.barplot(x=resumen.values, y=resumen.index, palette="viridis", ax=ax)

  ax.set_title("Gasto total por Comunidad Autónoma por Persona en el año 2023")
  ax.set_xlabel("Gasto por Euros")
  ax.set_ylabel("Comunidad Autónoma")
  plt.tight_layout()

  guardar_grafico(fig, "gasto_por_comunidad.png")  # <-- paso figura, no plt


# 2.4 funcion para visuañlizar tipos de gasto
#____________________________________________________

def gasto_por_grupo(df):
  df = df[
      (df["Tipo de dato"] == "Dato base") &
      (df["Grupos de gasto (2 dígitos)"] != "Índice general") &
      (df["Comunidad autónoma de residencia"] == "Total Nacional") &
      (df["Periodo"] == 2020) &
      (df["Gastos totales"] == "Gasto medio por hogar")
  ]

  resumen = df.groupby("Grupos de gasto (2 dígitos)")["Total"].sum().sort_values(ascending=False)
  resumen.index = resumen.index.str[3:]  # Eliminar el código inicial en el nombre
  # DICCIONARIO para renombrar a nombres más cortos

  nombres_cortos = {
      "Alimentos y bebidas no alcohólicas": "Alimentos",
      "Bebidas alcohólicas y tabaco": "Alcohol y tabaco",
      "Muebles, artículos del hogar y artículos para el mantenimiento corriente del hogar": "Artículos del hogar",

      "Vestido y calzado": "Vestimenta",
      "Vivienda, agua, electricidad, gas y otros combustibles": "Vivienda y servicios",
      "Muebles, equipamiento y mantenimiento del hogar": "Hogar",
      "Salud": "Salud",
      "Transporte": "Transporte",
      "Comunicaciones": "Comunicación",
      "Ocio, espectáculos y cultura": "Ocio y cultura",
      "Educación": "Educación",
      "Restaurantes y hoteles": "Restauración y hoteles",
      "Otros bienes y servicios": "Otros bienes"
  }

   #Agrupar los grupos pequeños en "Otros"

  total = resumen.sum()
  porcentajes = resumen / total
  umbral = 0.03 # Umbral mínimo para mostrar individualmente ajustar el porcentaje para que sea suficientemente pequeño 

  grupos_principales = resumen[porcentajes >= umbral]
  otros = resumen[porcentajes < umbral].sum()
  if otros > 0:
     grupos_principales["Otros"] = otros

  # Mover "Otros" al final siempre ya que la cantidad total de otros es un poquito mas grande que el valor de comunicacion y queda antes y se ve raro
  otros_valor = None
  if "Otros" in grupos_principales.index:
      otros_valor = grupos_principales["Otros"]
      grupos_principales = grupos_principales.drop("Otros")

  resumen = grupos_principales.sort_values(ascending=False)

  if otros_valor is not None:
      resumen["Otros"] = otros_valor

  # Renombrar con nombres más cortos
  resumen.index = [nombres_cortos.get(nombre, nombre) for nombre in resumen.index]


  # Crear gráfico tipo tarta 

  fig, ax = plt.subplots(figsize=(12, 12))
  result = ax.pie(
      resumen.values,
      labels=resumen.index,
      autopct="%1.1f%%",
      startangle=90,
      counterclock=False,
      textprops={'fontsize': 12},
      pctdistance=0.75,
      labeldistance=1.05,
      colors= colores_pastel
  )

  if len(result) == 3:
      wedges, texts, autotexts = result
  else:
      wedges, texts = result

  # Mostrar en consola los valores en € y %
  total_final = resumen.sum()
  porcentajes_final = (resumen / total_final) * 100

  print("\n--- Resumen de gastos por grupo (€ y %) ---")

  for nombre, valor in resumen.items():
    print(f"{nombre}: {valor:,.2f} €  ({porcentajes_final[nombre]:.2f}%)")

  ax.set_title("Distribución del gasto medio por hogar en 2020 en España", 
               fontsize=18, # aumenta el tamaño de letra
               y=1.02) # ajusta la distancia vertical más bajo 

  ax.axis("equal")
  plt.tight_layout()
  guardar_grafico(fig, "gasto_por_grupo.png")



# Paleta vibrante y colorida (más llamativa) :D
colores_chachi = [
    "#FF5733", "#33FF57", "#3357FF", "#F333FF", "#33FFF2",
    "#FF33A1", "#FF8C33", "#8C33FF", "#33FFA1", "#33FFF6",
    "#FF6F33", "#C70039"
]


#Paleta pastel suave (agradable y moderna) :  
colores_pastel = [
    "#FFD1DC", "#FFB347", "#77DD77", "#AEC6CF", "#FF6961",
    "#FDFD96", "#CBAACB", "#FFB6C1", "#CB99C9", "#B0E0E6",
    "#FFA07A", "#E6E6FA"
]


#2.5 def evolucion_gasto_periodo todos los años de mi dataset, hasta 2023 esta disponible
#____________________________________



def evolucion_gasto_periodo(df):
    resumen = df.groupby("Periodo")["Total"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))  # fig es lo que se guarda
    sns.lineplot(x=resumen.index, y=resumen.values, marker="o", ax=ax, color="#4C72B0", linewidth=2)

    ax.set_title("Evolución del gasto total por periodo", fontsize=16, weight="bold")
    ax.set_xlabel("Año", fontsize=14)
    ax.set_ylabel("Euros", fontsize=14)

    ax.set_xticks(resumen.index)
    ax.set_xticklabels(resumen.index.astype(int), rotation=45)

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))

    ax.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    guardar_grafico(fig, "evolucion_gasto_periodo.png")  # guarda

  #display(Image("output/evolucion_gasto_periodo.png"))  # para en notebook 


#2.6 4ª funcion vivienda en canarias (Beautiful y sencilla -Ich liebe sie!) ^^

#_________________________

def evolucion_gasto_vivienda_canarias(df):
    # Filtrar los datos para Canarias y el grupo de gasto "Vivienda"
    df_canarias_vivienda = df[
        (df['Comunidad autónoma de residencia'] == '05 Canarias') &
        (df['Grupos de gasto (2 dígitos)'] == '04 Vivienda, agua, electricidad, gas y otros combustibles') &
    (df['Periodo'] >= 2013 ) &
    (df["Gastos totales"] == "Gasto medio por hogar")
    ]

    # Agrupar por periodo (año) y sumar el gasto total
    resumen = df_canarias_vivienda.groupby('Periodo')['Total'].sum()

    # Crear gráfico de línea
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=resumen.index, y=resumen.values, marker='o', ax=ax, color='tab:blue', linewidth=2)

    # Personalizar el gráfico
    ax.set_title('Evolución del Gasto en Vivienda en Canarias (2013-2023)', fontsize=16, pad=30)
    ax.set_xlabel('Año', fontsize=14)
    ax.set_ylabel('Gasto Total Anual (€)', fontsize=14)
    ax.set_xticks(resumen.index)
    ax.set_xticklabels(resumen.index.astype(int), rotation=45)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
    ax.grid(True, linestyle='--', alpha=0.6)



    # Cambiar tamaño de puntos y línea un poco más gruesa
    ax.lines[0].set_linewidth(3)
    ax.lines[0].set_markersize(10)
    ax.lines[0].set_color('#1f77b4')  # Azul vibrante :D

    # Añadir etiquetas de valor encima de cada punto por mi curiosidad :D
    for x, y in zip(resumen.index, resumen.values):
        ax.text(x, y * 1.02, f'{y:,.0f} €', ha='center', fontsize=10, weight='bold', color='#1f77b4')

    # Suavizar la grilla ^^
    ax.grid(True, linestyle='--', alpha=0.4)

    # Quitar bordes superior y derecho para un estilo algo más limpio
    sns.despine(ax=ax)

    # Ajustar el diseño y guardar el gráfico
    plt.tight_layout()
    guardar_grafico(fig, 'evolucion_gasto_vivienda_canarias.png')

# .2.7 .5ª funcion del script ... de momento ;)
    
# funcion que va a demostrar gastos de alcohol y tabaco por la comunidad autonoma
#________________________________
def gasto_alcohol_tabaco_por_comunidad(df):
    # Filtrar datos para alcohol y tabaco, dato base, periodo 2023, excluyendo total nacional
    df_filtrado = df[
        (df["Tipo de dato"] == "Dato base") &
        (df["Grupos de gasto (2 dígitos)"] == "02 Bebidas alcohólicas y tabaco") &
        (df["Periodo"] == 2023) &
        (df["Comunidad autónoma de residencia"] != "Total Nacional") &
        (df["Gastos totales"] == "Gasto medio por persona")
    ]

    # Agrupar por comunidad autónoma y sumar el total
    resumen = df_filtrado.groupby("Comunidad autónoma de residencia")["Total"].sum().sort_values(ascending=False)

    # Limpiar nombres eliminando código que viene delante de cada nombre
    resumen.index = resumen.index.str[3:]

    # Crear gráfico vertical
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=resumen.index, y=resumen.values, palette="magma", ax=ax, order=resumen.index)

    ax.set_title("Gasto en Alcohol y Tabaco por Comunidad Autónoma en 2023", fontsize=16, pad=20)
    ax.set_ylabel("Gasto (€)", fontsize=14)
    ax.set_xlabel("Comunidad Autónoma", fontsize=14)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.')))
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Mejorar visibilidad etiquetas eje x 
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    # Guardar gráfico
    guardar_grafico(fig, "gasto_alcohol_tabaco_por_comunidad.png")




#_____________________________________________________
# 3. Configuraciones generales

sns.set(style="whitegrid")  # estilo uniforme para los gráficos
plt.style.use("seaborn-v0_8-darkgrid")  # estilo visual
sns.set_context("talk")  # tamaño de letras un poco más grande


#___________________________________________________
# 4. Carga del dataset

ruta = "./data/gastos_limpios.csv"
df = cargar_datos(ruta)



#________________________________
# 5. Llamadas a funciones para visualizar

gasto_por_comunidad(df)
gasto_por_grupo(df)
evolucion_gasto_periodo(df)
evolucion_gasto_vivienda_canarias(df)
gasto_alcohol_tabaco_por_comunidad(df)