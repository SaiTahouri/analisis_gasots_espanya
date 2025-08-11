import pandas as pd

# Cargar los datos ya limpios
df = pd.read_csv("./data/gastos_limpios.csv")


print(df.dtypes)
# Vista general del dataframe
print("Dimensiones del dataset:", df.shape)
print("Columnas:", df.columns.tolist())

print(".....................")
# Descripción estadística del total
#print("Estadísticas generales de la columna 'Total' ")
# print(df["Total"].describe())

print(".....................")
# Gastos totales por comunidad autónoma
print(" Gastos totales por comunidad ")
print(df.groupby("Comunidad autónoma de residencia")["Total"].sum().sort_values(ascending=False))

print(".....................")
# Gastos por grupo de gasto
print("Gastos por grupo de gasto ---")
print(df.groupby("Grupos de gasto (2 dígitos)")["Total"].sum().sort_values(ascending=False))
