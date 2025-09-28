import pandas as pd

def load_data(path="data/data_mas_falsa_que_tu_novia.csv"):
    df = pd.read_csv(path)
    return df
