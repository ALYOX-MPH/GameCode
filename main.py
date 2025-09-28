import tkinter as tk
from modules.visula_tkinter import App

def main():
    root = tk.Tk()
    root.title("Videojuegos Trends Analyzer")
    root.geometry("600x400")
    root.config(bg="#1e1e2f") 
    
    app = App(root)  #eto es la interfas esta lista y se carga con los modulos
    
    root.mainloop()

if __name__ == "__main__":
    main()
