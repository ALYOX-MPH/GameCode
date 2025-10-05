#fuciones 
from grafic_fun.industry_evolution import create_industry_evolution
from grafic_fun.genre_analysis import create_genre_analysis

def create_visualizations(df, option):
    if option == "Evolucion de la Industria":
        create_industry_evolution(df)
        
    elif option == "Analisis por Genero":  
        create_genre_analysis(df)



