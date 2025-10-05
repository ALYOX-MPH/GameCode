#fuciones 
from grafic_fun.industry_evolution import create_industry_evolution
from grafic_fun.genre_analysis import create_genre_analysis

def create_visualizations(df, option, parent):
    """Dirige a la visualización correspondiente"""
    if option == "Evolución de la Industria":
        return create_industry_evolution(df, parent)
    elif option == "Análisis por Género":  
        return create_genre_analysis(df, parent)
   # elif option == "Analisis por Sector":
       # return create_sector_analysis(df, parent)
    #elif option == "Distribucion Ingresos":
      #  return create_income_distribution(df, parent)
    #elif option == "Analisis Geografico":
        return create_geo_analysis(df, parent)
    else:
        # Mensaje de error si la opción no existe
        import tkinter as tk
        tk.Label(parent, text=f"Opción no reconocida: {option}", fg="red", bg="#1a1a2e").pack()
        return False
