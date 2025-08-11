import pandas as pd

#leer el archivo que ya se sabe que está separao por ;

df = pd.read_csv("gastos_comunidad.csv", sep=';')
 # Elimina espacios al principio/final
df.columns = df.columns.str.strip()  



# Exploracion y ver los datos para mi

print(df.dtypes) #miro tipo de datos



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


print(df["Total"].dtypes) #vamos a comprobar que se haya cambiado

print("_________________")
print(df["Total"].unique())









import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Crear carpeta de salida 
# os.makedirs("./output", exist_ok=True)

# Cargar el CSV limpio
df = pd.read_csv("./data/gastos_limpios.csv")

# Excluir "TOTAL NACIONAL"
df = df[df["Comunidad autónoma de residencia"] != "Total Nacional"]

# Estilo
sns.set(style="whitegrid")

# Agrupar y ordenar
gasto_por_comunidad = df.groupby("Comunidad autónoma de residencia")["Total"].sum().sort_values(ascending=False)

# Gráfico
plt.figure(figsize=(12, 6))
sns.barplot(x=gasto_por_comunidad.values, y=gasto_por_comunidad.index, palette="Blues_d")

plt.title("Gasto total por comunidad autónoma", fontsize=20)
plt.xlabel("Gasto total (€)")
plt.ylabel("Comunidad Autónoma")

# Guardar
plt.tight_layout()
plt.savefig("./output/gasto_por_comunidad.png")




