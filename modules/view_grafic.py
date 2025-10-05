import tkinter as tk
from PIL import Image, ImageTk
from modules.grafic import create_visualizations

def open_graph_view(root, df):
    win = tk.Toplevel(root)
    win.title("Visualizaciones")
    win.geometry("600x400")
    win.config(bg="#1e1e2f")

    tk.Label(win, text="Visualizaciones Disponibles",
             font=("Arial Black", 18), fg="#00d4ff", bg="#1e1e2f").pack(pady=10)

    frame = tk.Frame(win, bg="#1e1e2f")
    frame.pack(pady=20)

    graphs = [
        ("Evolucion de la Industria", "assets/logo.png", lambda: create_visualizations(df, "Evolucion de la Industria")),
        ("Analisis por Genero", "assets/logo.png", lambda: create_visualizations(df, "Analisis por Genero")),  # CORREGIDO
    
    ]

    for i, (title, img_file, callback) in enumerate(graphs):
        try:
            img = Image.open(img_file).resize((120, 80))
            photo = ImageTk.PhotoImage(img)

            btn = tk.Button(frame, image=photo, command=callback, bg="#1e1e2f")
            btn.image = photo  
            btn.grid(row=0, column=i, padx=10)

            tk.Label(frame, text=title, fg="white", bg="#1e1e2f", font=("Arial", 10)).grid(row=1, column=i)
        except:
            tk.Label(frame, text=f"[{title}]", fg="white", bg="#1e1e2f").grid(row=0, column=i, padx=10)
