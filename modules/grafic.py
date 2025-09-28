import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(df):
    # Gráfico de géneros
    plt.figure(figsize=(8,5))
    df['Genre'].value_counts().head(5).plot(kind='bar', color="skyblue")
    plt.title("Top 5 Géneros Más Populares")
    plt.ylabel("Número de Juegos")
    plt.show()

    # Evolución por año
    plt.figure(figsize=(8,5))
    df['Year'].value_counts().sort_index().plot(kind='line', marker='o')
    plt.title("Evolución de Lanzamientos por Año")
    plt.xlabel("Año")
    plt.ylabel("Número de Juegos")
    plt.show()


# estas grficas son de prueba solo prueba no le ponga la manooo