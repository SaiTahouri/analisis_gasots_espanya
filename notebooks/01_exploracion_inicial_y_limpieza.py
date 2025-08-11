# 01_exploracion_inicial.py
# Limpieza inicial del dataset de gastos por comunidad autónoma
# Proyecto: Análisis de gastos realizado por Sai


import pandas as pd
from datetime import datetime #para guardar el archivo con fecha

#leer el archivo que ya se sabe que está separao por ;

df = pd.read_csv("./data/gastos_comunidad.csv", sep=';')
 # Elimina espacios al principio/final
df.columns = df.columns.str.strip()  


# Exploracion y ver los datos pour moi

print(df.dtypes) #miro tipo de datos


#echarle un ojo a los valores unicos dentro de df
print("_________________")

print(df["Comunidad autónoma de residencia"].unique())

print("_________________")

print(df["Tipo de dato"].unique())
print("_________________")


print(df["Gastos totales"].unique())

print("_________________")

print(df["Grupos de gasto (2 dígitos)"].unique())
print("_________________")

print(df["Periodo"].unique())

print("_________________")
print(df["Total"].unique())


print("_________________")

#necesito convertir la colummna Total en numerico 

df["Total"] = df["Total"].str.replace(".", "", regex=False)
df["Total"] = df["Total"].str.replace(",", ".", regex=False)
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")


print(df["Total"].dtypes) #para comprobar que se haya cambiado

print("_________________")
print(df["Total"].unique())

print("_________________")
#valores null - hay muchos valores nulos 
#print(df.isnull().sum())

df.to_csv("data/gastos_limpios.csv", index=False)


# from datetime import datetime

fecha = datetime.today().strftime('%Y%m%d')
df.to_csv(f"data/gastos_limpios_{fecha}.csv", index=False)


#print(df["Total"].unique().tolist())

