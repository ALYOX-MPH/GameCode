import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Para usar el logo esta libreria es para las imagenessss
from modules.data_loader import load_data
from modules.analysis import run_eda
from modules.grafic import create_visualizations

class App:
    def __init__(self, root):
        self.root = root

        # --- LOGO ---
        try:
            logo_img = Image.open("logo.png")
            logo_img = logo_img.resize((120, 120))  
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(root, image=self.logo, bg="#1e1e2f").pack(pady=10)
        except:
            tk.Label(root, text="[LOGO]", fg="white", bg="#1e1e2f", font=("Arial", 16)).pack(pady=10)

        # --- TÍTULO ---
        tk.Label(root, text="GameSoft", 
                 font=("Arial Black", 24), 
                 fg="#00d4ff", bg="#1e1e2f").pack(pady=10)

        # --- BOTONES PRINCIPALES ---
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=6)

        self.btn_load = ttk.Button(root, text="Cargar Datos", command=self.load_data)
        self.btn_load.pack(pady=10)

        self.btn_eda = ttk.Button(root, text="Análisis Exploratorio", command=self.run_eda)
        self.btn_eda.pack(pady=10)

        self.btn_visuals = ttk.Button(root, text="Ver Gráficas", command=self.create_visuals)
        self.btn_visuals.pack(pady=10)

        # --- BOTÓN DE CRÉDITOS ---
        self.btn_credits = ttk.Button(root, text="Créditos", command=self.show_credits)
        self.btn_credits.pack(pady=30)

    def load_data(self):
        try:
            self.df = load_data()
            messagebox.showinfo("Éxito", "Datos cargados correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
#no entiendo porque no queria cargar los datos de repente 
    def run_eda(self):
        if hasattr(self, 'df'):
            run_eda(self.df)
        else:
            messagebox.showwarning("Aviso", "Primero carga los datos")

    def create_visuals(self):
        if hasattr(self, 'df'):
            create_visualizations(self.df)
        else:
            messagebox.showwarning("Aviso", "Primero carga los datos")

    def show_credits(self):
        credits = (
            "Proyecto: GameSoft\n"
            "Grupo: CIncobite\n"
            "Integrantes:\n"
            "- Álvaro Pérez\n"
            "- Poner su nombre pliisss\n"
            "- Poner su nombre pliisss\n"
            "- Poner su nombre pliisss\n"
            "- "
        )
        messagebox.showinfo("Créditos", credits)
#esta parte funciona de por dios 