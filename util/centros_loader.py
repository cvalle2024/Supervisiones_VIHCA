
import pandas as pd

def cargar_centros():
    df = pd.read_csv("data/centros_salud.csv", encoding="latin1")
    return df
