#fuciones 
from grafic_fun.industry_evolution import create_industry_evolution
from grafic_fun.genre_analysis import create_genre_analysis
from grafic_fun.platform_trend_analysis import create_platform_quality_sales_trend
from grafic_fun.critic_sales_correlation import create_critic_sales_correlation

def create_visualizations(df, option):
    if option == "Evolucion de la Industria":
        create_industry_evolution(df)
        
    elif option == "Analisis por Genero":  
        create_genre_analysis(df)
    
    elif option == "Tendencia por Plataforma":
        create_platform_quality_sales_trend(df)
        
    elif option == "Correlacion Critica-Ventas":
        create_critic_sales_correlation(df)


