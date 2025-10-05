import tkinter as tk
from tkinter import ttk
from modules.grafic import create_visualizations

def open_graph_view(root, df):
    win = tk.Toplevel(root)
    win.title("Visualizaciones - Dashboard Profesional")
    win.geometry("1200x800")
    win.config(bg="#0f0f23")
    win.minsize(1000, 700)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.TFrame", background="#0f0f23")
    style.configure("Card.TFrame", background="#1a1a2e", relief="flat", borderwidth=1)

    main_container = tk.Frame(win, bg="#0f0f23")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    content_container = tk.Frame(main_container, bg="#0f0f23")
    content_container.pack(fill="both", expand=True)

    nav_frame = ttk.Frame(content_container, style="Card.TFrame", width=280)
    nav_frame.pack(side="left", fill="y", padx=(0, 20))
    nav_frame.pack_propagate(False)

    tk.Label(nav_frame, text="CATEGORÍAS", font=("Segoe UI", 12, "bold"),
             fg="#00e5ff", bg="#1a1a2e").pack(pady=(20, 15))

    graph_container = ttk.Frame(content_container, style="Custom.TFrame")
    graph_container.pack(side="right", fill="both", expand=True)

    canvas = tk.Canvas(graph_container, bg="#0f0f23", highlightthickness=0, width=500)
    scrollbar = ttk.Scrollbar(graph_container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")

    canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind("<MouseWheel>", _on_mousewheel)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    graph_frames = {}

    graphs = [
        {"title": "📈 Evolución de la Industria", "key": "industry"},
        {"title": "👥 Análisis por Género", "key": "genre"},
    ]

    for g in graphs:
        frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        frame.pack_forget()  # Oculto al inicio

        tk.Label(frame, text=g["title"], font=("Segoe UI", 20, "bold"),
                 fg="#00e5ff", bg="#1a1a2e").pack(pady=(20,10))

        try:
            create_visualizations(df, g["title"].replace("📈 ","").replace("👥 ",""), frame)
        except Exception as e:
            tk.Label(frame, text=f"Error: {str(e)}", fg="red", bg="#1a1a2e").pack(pady=50)

        graph_frames[g["key"]] = frame

    def mostrar_grafica(key):
        for f in graph_frames.values():
            f.pack_forget()
        graph_frames[key].pack(fill="both", expand=True, padx=10, pady=10)

    def create_nav_button(parent, graph):
        btn = tk.Button(
            parent,
            text=graph["title"],
            bg="#252540",
            fg="#00e5ff",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            command=lambda k=graph["key"]: mostrar_grafica(k)
        )
        btn.pack(fill="x", padx=15, pady=8)

    for g in graphs:
        create_nav_button(nav_frame, g)

    # --- Footer ---
    footer_frame = tk.Frame(main_container, bg="#0f0f23")
    footer_frame.pack(fill="x", pady=(20, 0))
    tk.Label(
        footer_frame,
        text="Dashboard",
        font=("Segoe UI", 10), fg="#8a8aa3", bg="#0f0f23"
    ).pack()

    # --- Centrar ventana ---
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (win.winfo_width() // 2)
    y = (win.winfo_screenheight() // 2) - (win.winfo_height() // 2)
    win.geometry(f"+{x}+{y}")

    if graphs:
        mostrar_grafica(graphs[0]["key"])
