import customtkinter as ctk
from gui import BibliotecaGUI

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = BibliotecaGUI()
    app.mainloop()