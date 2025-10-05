# grafic_fun/genre_analysis.py
import matplotlib.pyplot as plt
import pandas as pd

def create_genre_analysis(df):
    # Procesar datos para análisis por género
    df_processed = df.copy()
    
    # Si no existe la columna genre, usar Genre
    if 'genre' not in df_processed.columns and 'Genre' in df_processed.columns:
        df_processed['genre'] = df_processed['Genre']
    
    # Crear figura con subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análisis de Géneros en el Mercado', fontsize=16, fontweight='bold')
    
    # 1. Ventas promedio por género (Top 8)
    if 'genre' in df_processed.columns:
        genre_sales = df_processed.groupby('genre')['total_sales'].mean().nlargest(8)
        genre_sales.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Ventas Promedio por Género (Top 8)')
        ax1.set_ylabel('Ventas Promedio (millones)')
        ax1.tick_params(axis='x', rotation=45)
    
    # 2. Puntuación crítica por género (Top 8)
    if 'genre' in df_processed.columns and 'critic_score' in df_processed.columns:
        genre_scores = df_processed.groupby('genre')['critic_score'].mean().nlargest(8)
        genre_scores.plot(kind='bar', ax=ax2, color='lightgreen')
        ax2.set_title('Puntuación Crítica por Género (Top 8)')
        ax2.set_ylabel('Puntuación Promedio')
        ax2.tick_params(axis='x', rotation=45)
    
    # 3. Número de juegos por género (Top 8)
    if 'genre' in df_processed.columns:
        genre_counts = df_processed['genre'].value_counts().head(8)
        genre_counts.plot(kind='bar', ax=ax3, color='lightcoral')
        ax3.set_title('Número de Juegos por Género (Top 8)')
        ax3.set_ylabel('Cantidad de Juegos')
        ax3.tick_params(axis='x', rotation=45)
    
    # 4. Ventas totales por género (Top 8)
    if 'genre' in df_processed.columns:
        genre_total_sales = df_processed.groupby('genre')['total_sales'].sum().nlargest(8)
        genre_total_sales.plot(kind='bar', ax=ax4, color='gold')
        ax4.set_title('Ventas Totales por Género (Top 8)')
        ax4.set_ylabel('Ventas Totales (millones)')
        ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()