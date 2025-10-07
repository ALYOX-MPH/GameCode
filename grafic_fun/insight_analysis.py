import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pandas as pd

def create_insight_analysis(df, parent):
    """Crea un panel completo de análisis de géneros con scroll"""
    main_frame, scrollable_frame, canvas = _crear_frame_scrolleable(parent)
    create_insight_grid_visualizations(df, scrollable_frame)
    return main_frame

def _crear_frame_scrolleable(parent):
    """Crea un frame principal con capacidad de scroll"""
    main_frame = tk.Frame(parent, bg="#0f0f23")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_frame, bg="#0f0f23", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = tk.Frame(canvas, bg="#0f0f23")
    canvas_frame = canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", configure_scrollregion)

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_frame, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    return main_frame, scrollable_frame, canvas

def _crear_frame_grafica(parent, titulo="", color_titulo="#00e5ff"):
    """Crea un frame contenedor para una gráfica con título"""
    frame = tk.Frame(parent, bg="#1a1a2e", relief="raised", bd=1)
    frame.pack(fill="x", padx=10, pady=10)
    
    if titulo:
        tk.Label(frame, text=titulo, font=("Arial",14,"bold"), 
                fg=color_titulo, bg="#1a1a2e").pack(pady=10)
    
    return frame

def _preparar_datos_analisis(df):
    """Prepara los datos para el análisis de insights"""
    juegos_promedio = (
        df.groupby('title')
        .agg({
            'critic_score': 'mean',
            'total_sales': 'mean',
            'genre': 'first',
            'console': lambda x: list(x.unique())
        })
        .round(2)
        .reset_index()
    )

    if juegos_promedio['critic_score'].max() > 10:
        juegos_promedio['critic_score'] = juegos_promedio['critic_score'] / 10

    conteo_generos = juegos_promedio.groupby("genre").size().reset_index(name='count')
    generos_filtrados = conteo_generos[conteo_generos['count'] > 10]['genre']
    df_filtrado = juegos_promedio[juegos_promedio['genre'].isin(generos_filtrados)]

    return df_filtrado

def _crear_grafico_calidad_ventas(ax, df_filtrado, colors):
    """Crea gráfico de Calidad vs Ventas"""
    if "critic_score" in df_filtrado.columns and "total_sales" in df_filtrado.columns:
        ax.scatter(
            df_filtrado['total_sales'], 
            df_filtrado['critic_score'],
            c='#00e5ff',
            alpha=0.6,
            s=50,
            edgecolors='white',
            linewidth=0.5
        )

        joyas_ocultas = df_filtrado[
            (df_filtrado['critic_score'] >= 8.0) & 
            (df_filtrado['total_sales'] < 0.5)
        ]
        blockbusters_vacios = df_filtrado[
            (df_filtrado['total_sales'] >= 2.0) & 
            (df_filtrado['critic_score'] < 6.0)
        ]

        if len(joyas_ocultas) > 0:
            ax.scatter(
                joyas_ocultas['total_sales'], 
                joyas_ocultas['critic_score'],
                c='#00ff88',
                s=80,
                edgecolors='white',
                linewidth=1.5,
                label='✦ Joyas Ocultas'
            )

  

        ax.axhline(y=8.0, color='#00ff88', linestyle='--', alpha=0.5)
        ax.axhline(y=6.0, color='#ff6d00', linestyle='--', alpha=0.5)
        ax.axvline(x=0.5, color='#00ff88', linestyle='--', alpha=0.5)
        ax.axvline(x=2.0, color='#ff6d00', linestyle='--', alpha=0.5)

        ax.set_title("＄ Calidad vs Ventas – Análisis Estratégico", color='white', fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel("Ventas Totales (Millones)", color='white', fontsize=10)
        ax.set_ylabel("Puntaje Crítico Promedio (0-10)", color='white', fontsize=10)
        ax.legend(facecolor='#1a1a2e', edgecolor='#00e5ff', labelcolor='white', fontsize=9, loc='upper right')
        ax.set_xlim(-0.1, max(df_filtrado['total_sales']) * 1.1)
        ax.set_ylim(0, 10.5)
        
        return joyas_ocultas
    return pd.DataFrame()

def _crear_grafico_top_joyas(ax, joyas_ocultas):
    """Crea gráfico de Top 5 Joyas Ocultas"""
    ax.axis('off')

    if not joyas_ocultas.empty:
        # Tomar las 5 mejores joyas por score
        top5 = joyas_ocultas.nlargest(5, 'critic_score')
        cell_height = 0.12
        start_y = 0.9

        ax.text(0.5, 0.97, "★ TOP 5 JOYAS OCULTAS", transform=ax.transAxes,
                ha='center', color='white', fontsize=12, fontweight='bold')

        for idx, (_, row) in enumerate(top5.iterrows()):
            bg_color = '#1a1a2e' if idx % 2 == 0 else '#0f0f23'
            rect = plt.Rectangle((0.02, start_y - 0.04), 0.96, cell_height,
                                transform=ax.transAxes, facecolor=bg_color, alpha=0.7)
            ax.add_patch(rect)

            ax.text(0.05, start_y, f"{idx+1}. {row['title'][:25]}", transform=ax.transAxes,
                    color='white', fontsize=9, fontweight='bold')
            ax.text(0.55, start_y, f"{row['critic_score']:.1f}/10", transform=ax.transAxes,
                    color='#00ff88', fontsize=9, fontweight='bold')
            ax.text(0.75, start_y, f"{row['total_sales']:.2f}M", transform=ax.transAxes,
                    color='#00e5ff', fontsize=8)
            
            # Mostrar máximo 2 consolas
            consolas = ", ".join(row['console'][:2])
            if len(row['console']) > 2:
                consolas += f" (+{len(row['console'])-2})"
            ax.text(0.9, start_y, consolas, transform=ax.transAxes,
                    color='#9c27b0', fontsize=8, ha='right')

            start_y -= cell_height
    else:
        ax.text(0.5, 0.5, "No se encontraron joyas ocultas en la muestra.", 
                transform=ax.transAxes, color='gray', fontsize=10, ha='center', va='center')

def _crear_grafico_analisis_publishers(ax, df):
    """Crea gráfico de análisis de publishers"""
    if all(col in df.columns for col in ['publisher', 'total_sales', 'console']):
        resumen_publishers = (
            df.groupby('publisher')
            .agg({
                'total_sales': 'sum',
                'title': 'count',
                'console': lambda x: len(set(x))
            })
            .rename(columns={'title': 'num_juegos', 'console': 'num_plataformas'})
            .reset_index()
        )

        top_publishers = resumen_publishers.sort_values('total_sales', ascending=False).head(10)

        ax.bar(top_publishers['publisher'], top_publishers['total_sales'],
                color='#00e5ff', alpha=0.7, label='Ventas Totales (M)')
        
        ax3b = ax.twinx()
        ax3b.plot(top_publishers['publisher'], top_publishers['num_plataformas'],
                color='#ff6d00', marker='o', linewidth=2, label='Nº de Plataformas')

        ax.set_title("★ Top 10 Publishers – Ventas, Presencia y Diversificación", 
                    color='white', fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel("Publisher", color='white', fontsize=9)
        ax.set_ylabel("Ventas Totales (millones)", color='#00e5ff', fontsize=9)
        ax3b.set_ylabel("Nº de Plataformas", color='#ff6d00', fontsize=9)

        ax.tick_params(colors='white', rotation=40)
        ax3b.tick_params(colors='white')

        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', facecolor='#1a1a2e', edgecolor='#00e5ff', fontsize=8)
        ax3b.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#ff6d00', fontsize=8)

        for i, val in enumerate(top_publishers['total_sales']):
            ax.text(i, val + 1, f"{val:.1f}M", color='white', fontsize=8, ha='center', fontweight='bold')
            ax.text(i, val / 2, f"{top_publishers['num_juegos'].iloc[i]} juegos", 
                    color='#9c27b0', fontsize=7, ha='center')

def _aplicar_estilo_graficos(axes):
    """Aplica estilo consistente a todos los gráficos"""
    for ax in axes:
        ax.set_facecolor('#0a0a1a')
        for spine in ax.spines.values():
            spine.set_color('#00e5ff')
            spine.set_linewidth(1)
        ax.tick_params(colors='white', labelsize=8)

def _crear_primera_grafica(parent, df, available_width, colors):
    """Crea la primera figura con análisis de insights"""
    frame1 = _crear_frame_grafica(parent)

    fig1_width, fig1_height = min(available_width, 1400), min(available_width, 1400)*0.7
    
    fig1 = plt.figure(figsize=(fig1_width/100, fig1_height/100), facecolor='#0f0f23', dpi=100)
    gs1 = fig1.add_gridspec(2, 2)

    # Preparar datos
    df_filtrado = _preparar_datos_analisis(df)

    # POSICIÓN 1: Calidad vs Ventas (superior izquierda)
    ax1 = fig1.add_subplot(gs1[0, 0])
    joyas_ocultas = _crear_grafico_calidad_ventas(ax1, df_filtrado, colors)

    # POSICIÓN 2: Top 5 Joyas Ocultas (superior derecha)
    ax2 = fig1.add_subplot(gs1[0, 1])
    _crear_grafico_top_joyas(ax2, joyas_ocultas)

    # POSICIÓN 3: Análisis Publishers (inferior completa)
    ax3 = fig1.add_subplot(gs1[1, :])
    _crear_grafico_analisis_publishers(ax3, df)

    _aplicar_estilo_graficos([ax1, ax3])
    fig1.tight_layout(pad=3.0)
    
    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    return frame1

def create_insight_grid_visualizations(df, parent):
    """Crea un grid de gráficas para el análisis de insights"""
    plt.style.use('dark_background')
    parent.update_idletasks()
    available_width = max(parent.winfo_width() - 40, 1200)
    colors = ['#00e5ff', '#9c27b0', '#00ff88', '#ff6d00', '#ffeb3b']

    _crear_primera_grafica(parent, df, available_width, colors)