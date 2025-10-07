import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pandas as pd

def crear_frame_scrolleable(parent):
    """Crea un frame principal con capacidad de scroll"""
    main_frame = tk.Frame(parent, bg="#0f0f23")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_frame, bg="#0f0f23", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Frame interno dentro del canvas
    scrollable_frame = tk.Frame(canvas, bg="#0f0f23")
    canvas_frame = canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

    # Configurar scroll automático
    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", configure_scrollregion)

    # Ajustar ancho del frame interno al tamaño del canvas
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_frame, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    # Scroll con la rueda del mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    return main_frame, scrollable_frame, canvas

def crear_frame_grafica(parent, titulo="", color_titulo="#00e5ff"):
    """Crea un frame contenedor para una gráfica con título"""
    frame = tk.Frame(parent, bg="#1a1a2e", relief="raised", bd=1)
    frame.pack(fill="x", padx=10, pady=10)
    
    if titulo:
        tk.Label(frame, text=titulo, font=("Arial",14,"bold"), 
                fg=color_titulo, bg="#1a1a2e").pack(pady=10)
    
    return frame

def crear_grafico_top_consolas_juegos(ax, df, colors):
    """Crea gráfico de top consolas con más juegos"""
    if "console" in df.columns and "title" in df.columns:
        # Calcular consolas con más juegos
        consolas_mas_juegos = (
            df.groupby("console")["title"]
            .count()
            .reset_index()
            .rename(columns={"title": "num_juegos"})
            .sort_values(by="num_juegos", ascending=False)
        )
        
        top_consolas_juegos = consolas_mas_juegos.head(10)
        
        bars = ax.bar(range(len(top_consolas_juegos)), 
                     top_consolas_juegos["num_juegos"], 
                     color=colors[:len(top_consolas_juegos)],
                     alpha=0.8)
        
        ax.set_xticks(range(len(top_consolas_juegos)))
        ax.set_xticklabels(top_consolas_juegos["console"], 
                          color='white', fontsize=8, rotation=45, ha='right')
        ax.set_title("📊 Top 10 Consolas con Más Juegos", color='white', fontsize=12, fontweight='bold')
        ax.set_ylabel("Número de Juegos", color='white', fontsize=10)
        ax.set_xlabel("Consola", color='white', fontsize=10)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f"{int(height):,}", ha='center', va='bottom',
                   color='white', fontweight='bold', fontsize=9)

def crear_grafico_ventas_totales(ax, df, colors):
    """Crea gráfico de ventas totales por consola"""
    if "console" in df.columns and "total_sales" in df.columns:
        total_sales_by_console = df.groupby('console')['total_sales'].sum().sort_values(ascending=False).head(10)
        total_sales_by_console.head(8).plot(kind='bar', ax=ax, color=colors, alpha=0.8)
        ax.set_title('＄ Ventas Totales', color='white', fontsize=11, fontweight='bold')
        ax.set_ylabel('Ventas (Millones)', color='white', fontsize=9)
        ax.tick_params(axis='x', rotation=45, colors='white', labelsize=8)
        ax.tick_params(axis='y', colors='white', labelsize=8)

def crear_grafico_puntuacion_promedio(ax, df, colors):
    """Crea gráfico de puntuación promedio por consola"""
    if "console" in df.columns and "critic_score" in df.columns:
        avg_score_by_console = df.groupby('console')['critic_score'].mean().sort_values(ascending=False).head(10)
        avg_score_by_console.head(8).plot(kind='barh', ax=ax, color=colors, alpha=0.8)
        ax.set_title('℗ Puntuación Promedio', color='white', fontsize=11, fontweight='bold')
        ax.set_xlabel('Puntuación', color='white', fontsize=9)  
        ax.set_ylabel('Consola', color='white', fontsize=9)     
        ax.tick_params(axis='x', colors='white', labelsize=8)  
        ax.tick_params(axis='y', colors='white', labelsize=8)

def crear_grafico_diversidad_generos(ax, df, colors):
    """Crea gráfico de donut de diversidad de géneros por plataforma"""
    if "console" in df.columns and "genre" in df.columns:
        genres_per_console = df.groupby('console')['genre'].nunique()
        top_consoles = genres_per_console.nlargest(8)

        wedges, texts, autotexts = ax.pie(
            top_consoles.values, 
            labels=top_consoles.index, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            wedgeprops=dict(width=0.4, edgecolor='white'),
            textprops={'color': 'white', 'fontsize': 8}
        )

        # Mejorar etiquetas
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        ax.set_title('◎ Diversidad de géneros por plataforma', color='white', fontsize=11, fontweight='bold', pad=20)

def aplicar_estilo_graficos(axes):
    """Aplica estilo consistente a todos los gráficos"""
    for ax in axes:
        ax.set_facecolor('#0a0a1a')
        for spine in ax.spines.values():
            spine.set_color('#00e5ff')
            spine.set_linewidth(1)
        ax.tick_params(colors='white', labelsize=8)

def crear_primera_grafica_consolas(parent, df, available_width):
    """Crea la primera figura con análisis de consolas"""
    frame1 = crear_frame_grafica(parent, "", "#00e5ff")
    
    fig1_width, fig1_height = min(available_width, 1400), min(available_width, 1400)*0.7
    colors = ["#0d7a86", "#550663", "#0d9e5b", "#7c3f10", "#ad9e11"]
    
    fig1 = plt.figure(figsize=(fig1_width/100, fig1_height/100), facecolor='#0f0f23', dpi=100)
    gs1 = fig1.add_gridspec(2, 2)
    
    # Crear subgráficos
    ax1 = fig1.add_subplot(gs1[0, 0])  # Top consolas por juegos
    ax2 = fig1.add_subplot(gs1[0, 1])  # Ventas totales
    ax3 = fig1.add_subplot(gs1[1, 0])  # Puntuación promedio
    ax4 = fig1.add_subplot(gs1[1, 1])  # Diversidad de géneros
    
    crear_grafico_top_consolas_juegos(ax1, df, colors)
    crear_grafico_ventas_totales(ax2, df, colors)
    crear_grafico_puntuacion_promedio(ax3, df, colors)
    crear_grafico_diversidad_generos(ax4, df, colors)
    
    aplicar_estilo_graficos([ax1, ax2, ax3, ax4])
    fig1.tight_layout(pad=3.0)
    
    # Integrar en Tkinter
    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    return frame1

def create_console_analysis(df, parent):
    """Función principal que crea el panel completo de análisis de consolas"""
    # Configurar estilo de matplotlib
    plt.style.use('dark_background')
    
    # Crear frame scrolleable
    main_frame, scrollable_frame, canvas = crear_frame_scrolleable(parent)
    
    # Calcular ancho disponible
    scrollable_frame.update_idletasks()
    available_width = max(scrollable_frame.winfo_width() - 40, 1200)
    
    # Crear gráficas
    crear_primera_grafica_consolas(scrollable_frame, df, available_width)
    
    return main_frame

# Función mantenida por compatibilidad (puede eliminarse eventualmente)
def create_console_grid_visualizations(df, parent):
    """Función legacy - usar create_console_analysis en su lugar"""
    return create_console_analysis(df, parent)