# main.py
import customtkinter as ctk
from gui import BibliotecaGUI
import sys

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    try:
        app = BibliotecaGUI()
        app.mainloop()
    except Exception as e:
        print("Error al iniciar la aplicación:", e)
        sys.exit(1)