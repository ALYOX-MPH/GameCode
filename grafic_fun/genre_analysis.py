import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pandas as pd

def create_genre_analysis(df, parent):
    df_processed = df.copy()
    if 'genre' not in df_processed.columns and 'Genre' in df_processed.columns:
        df_processed['genre'] = df_processed['Genre']

    # Lista de datos para graficar
    plots = []

    if 'genre' in df_processed.columns:
        genre_sales = df_processed.groupby('genre')['total_sales'].mean().nlargest(8)
        plots.append(("Ventas Promedio por Género (Top 8)", genre_sales, 'skyblue', 'total_sales'))

    if 'genre' in df_processed.columns and 'critic_score' in df_processed.columns:
        genre_scores = df_processed.groupby('genre')['critic_score'].mean().nlargest(8)
        plots.append(("Puntuación Crítica por Género (Top 8)", genre_scores, 'lightgreen', 'critic_score'))

    if 'genre' in df_processed.columns:
        genre_counts = df_processed['genre'].value_counts().head(8)
        plots.append(("Número de Juegos por Género (Top 8)", genre_counts, 'lightcoral', None))

    if 'genre' in df_processed.columns:
        genre_total_sales = df_processed.groupby('genre')['total_sales'].sum().nlargest(8)
        plots.append(("Ventas Totales por Género (Top 8)", genre_total_sales, 'gold', 'total_sales'))

    # Crear canvas para cada gráfica y poner debajo de la anterior
    for title, data, color, col in plots:
        fig, ax = plt.subplots(figsize=(12,5))
        if col:
            data.plot(kind='bar', ax=ax, color=color)
        else:
            data.plot(kind='bar', ax=ax, color=color)
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)  # se apilan verticalmente
