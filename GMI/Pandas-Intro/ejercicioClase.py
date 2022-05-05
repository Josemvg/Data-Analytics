import pandas as pd

# Ejercicio 1 - carga de datos
df = pd.read_csv("datasets/casos_diagnostico_ccaa.csv")

# Ejercicio 2 - 5 primeras filas
print("5 primeras filas")
print(df.head(5))
print("")

# Ejercicio 3 - 5 primeras columnas
print("5 primeras columnas")
print(df.iloc[:,:5])
print("")

# Ejercicio 4 - tuplas dataframe
print("Dataframe como lista de tuplas")
print(df.to_records(index=False))
print("")

# Ejercicio 5 - tablas con fecha "2021-01-25"
print("Tablas con fecha 2021-01-25")
print(df[df.fecha == "2021-01-25"])
print("")

# Ejercicio 6 - numero de casos con fecha "2021-01-25"
print("Numero de casos con fecha 2021-01-25")
print(df[df.fecha == "2021-01-25"].num_casos.sum())
print("")

# Ejercicio 7 - numero de casos por CCAA
print("Numero de casos por CCAA")
print(df.groupby("ccaa_iso").num_casos.sum())
print("")

# Ejercicio 8 - CCAA con mayor numero de casos
print("Comunidad con mayor numero de casos")
print(df.groupby("ccaa_iso").num_casos.sum().idxmax())
print("")

# Ejercicio 9 - CCAA con menor numero de casos
print("Comunidad con menor numero de casos")
print(df.groupby("ccaa_iso").num_casos.sum().idxmin())
print("")