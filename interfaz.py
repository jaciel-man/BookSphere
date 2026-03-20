import tkinter as tk
from tkinter import ttk, messagebox

class Autenticador:
    def __init__(self):
        self.usuarios = {}

    def registrar(self, nombre, correo, telefono, usuario, password):
        if usuario in self.usuarios:
            return False
        self.usuarios[usuario] = {
            "nombre": nombre,
            "correo": correo,
            "telefono": telefono,
            "password": password
        }
        return True

    def iniciar_sesion(self, usuario, password):
        return usuario in self.usuarios and self.usuarios[usuario]["password"] == password

class VentanaLogin(tk.Toplevel):
    def __init__(self, padre, autenticador, callback_exito):
        super().__init__(padre)
        self.autenticador = autenticador
        self.callback_exito = callback_exito
        self.title("Iniciar sesión / Registro")
        self.geometry("450x500")
        self.resizable(False, False)
        self.configure(bg="#F2D492")
        self.transient(padre)
        self.grab_set()
        self.modo = "login"
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Biblioteca Digital", font=("Segoe UI", 16, "bold"),
                 bg="#F2D492", fg="#202C39").pack(pady=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=20, fill="both", expand=True)

        self.frame_login = tk.Frame(self.notebook, bg="#F2D492")
        self.frame_registro = tk.Frame(self.notebook, bg="#F2D492")
        self.notebook.add(self.frame_login, text="Iniciar sesión")
        self.notebook.add(self.frame_registro, text="Registrarse")

        self.crear_login()
        self.crear_registro()

    def crear_login(self):
        campos = [("Usuario:", 0), ("Contraseña:", 1)]
        self.login_entries = {}
        for texto, fila in campos:
            lbl = tk.Label(self.frame_login, text=texto, bg="#F2D492", fg="#202C39")
            lbl.grid(row=fila, column=0, padx=10, pady=8, sticky="e")
            entry = tk.Entry(self.frame_login, show="*" if "Contraseña" in texto else "")
            entry.grid(row=fila, column=1, padx=10, pady=8)
            self.login_entries[texto] = entry

        btn = tk.Button(self.frame_login, text="Entrar", bg="#F29559", fg="#202C39",
                        command=self.procesar_login)
        btn.grid(row=2, columnspan=2, pady=15)

        self.lbl_mensaje_login = tk.Label(self.frame_login, text="", bg="#F2D492", fg="#F29559")
        self.lbl_mensaje_login.grid(row=3, columnspan=2)

    def crear_registro(self):
        campos = [
            ("Nombre completo:", 0), ("Correo electrónico:", 1),
            ("Teléfono:", 2), ("Usuario:", 3),
            ("Contraseña:", 4), ("Confirmar contraseña:", 5)
        ]
        self.reg_entries = {}
        for texto, fila in campos:
            lbl = tk.Label(self.frame_registro, text=texto, bg="#F2D492", fg="#202C39")
            lbl.grid(row=fila, column=0, padx=10, pady=5, sticky="e")
            show = "*" if "Contraseña" in texto else ""
            entry = tk.Entry(self.frame_registro, show=show)
            entry.grid(row=fila, column=1, padx=10, pady=5)
            self.reg_entries[texto] = entry

        tk.Label(self.frame_registro, text="Fecha de nacimiento:", bg="#F2D492", fg="#202C39"
                ).grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.fecha_entry = tk.Entry(self.frame_registro)
        self.fecha_entry.grid(row=6, column=1, padx=10, pady=5)

        btn = tk.Button(self.frame_registro, text="Registrarse", bg="#F29559", fg="#202C39",
                        command=self.procesar_registro)
        btn.grid(row=7, columnspan=2, pady=15)

        self.lbl_mensaje_reg = tk.Label(self.frame_registro, text="", bg="#F2D492", fg="#F29559")
        self.lbl_mensaje_reg.grid(row=8, columnspan=2)

    def procesar_login(self):
        usuario = self.login_entries["Usuario:"].get()
        password = self.login_entries["Contraseña:"].get()
        if self.autenticador.iniciar_sesion(usuario, password):
            self.callback_exito(usuario)
            self.destroy()
        else:
            self.lbl_mensaje_login.config(text="Usuario o contraseña incorrectos")

    def procesar_registro(self):
        datos = {k: v.get() for k, v in self.reg_entries.items()}
        fecha = self.fecha_entry.get()
        if any(not v for v in datos.values()) or not fecha:
            self.lbl_mensaje_reg.config(text="Todos los campos son obligatorios")
            return
        if datos["Contraseña:"] != datos["Confirmar contraseña:"]:
            self.lbl_mensaje_reg.config(text="Las contraseñas no coinciden")
            return
        exito = self.autenticador.registrar(
            datos["Nombre completo:"],
            datos["Correo electrónico:"],
            datos["Teléfono:"],
            datos["Usuario:"],
            datos["Contraseña:"]
        )
        if exito:
            messagebox.showinfo("Registro", "Usuario registrado con éxito. Ya puede iniciar sesión.")
            self.notebook.select(0)
            self.limpiar_registro()
        else:
            self.lbl_mensaje_reg.config(text="El nombre de usuario ya existe")

    def limpiar_registro(self):
        for entry in self.reg_entries.values():
            entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.lbl_mensaje_reg.config(text="")

class PanelCategorias(tk.Frame):
    def __init__(self, padre, colores, callback_categoria):
        super().__init__(padre, bg=colores["dry_sage"])
        self.colores = colores
        self.callback = callback_categoria
        self.botones = []
        self.categorias = ["Todos", "Ficción", "No ficción", "Infantil", "Revistas", "Tesis"]
        self.crear_botones()

    def crear_botones(self):
        tk.Label(self, text="Categorías", font=("Segoe UI", 12, "bold"),
                 bg=self.colores["dry_sage"], fg=self.colores["jet_black"]).pack(pady=10)
        for cat in self.categorias:
            btn = tk.Button(self, text=cat, bg=self.colores["soft_peach"],
                            fg=self.colores["jet_black"], relief=tk.RAISED,
                            command=lambda c=cat: self.seleccionar(c))
            btn.pack(fill=tk.X, padx=10, pady=3)
            self.botones.append(btn)

    def seleccionar(self, categoria):
        for btn in self.botones:
            if btn["text"] == categoria:
                btn.config(bg=self.colores["tangerine"])
            else:
                btn.config(bg=self.colores["soft_peach"])
        self.callback(categoria)

class PanelLibros(tk.Frame):
    def __init__(self, padre, colores):
        super().__init__(padre, bg=colores["soft_peach"])
        self.colores = colores
        self.todos_libros = [
            ("Cien años de soledad", "Gabriel García Márquez", 1967, "Disponible", "Ficción"),
            ("1984", "George Orwell", 1949, "Prestado", "Ficción"),
            ("El Quijote", "Miguel de Cervantes", 1605, "Disponible", "Ficción"),
            ("Breve historia del tiempo", "Stephen Hawking", 1988, "Disponible", "No ficción"),
            ("Cosmos", "Carl Sagan", 1980, "Disponible", "No ficción"),
            ("El principito", "Antoine de Saint-Exupéry", 1943, "Disponible", "Infantil"),
        ]
        self.libros_filtrados = self.todos_libros[:]
        self.crear_widgets()

    def crear_widgets(self):
        self.tree = ttk.Treeview(self, columns=("titulo", "autor", "año", "estado"),
                                  show="headings", height=15)
        self.tree.heading("titulo", text="Título")
        self.tree.heading("autor", text="Autor")
        self.tree.heading("año", text="Año")
        self.tree.heading("estado", text="Estado")
        self.tree.column("titulo", width=300)
        self.tree.column("autor", width=200)
        self.tree.column("año", width=80, anchor="center")
        self.tree.column("estado", width=120, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scroll.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for libro in self.libros_filtrados:
            self.tree.insert("", tk.END, values=libro[:4])

    def filtrar(self, texto, categoria):
        texto = texto.lower()
        filtrados = []
        for libro in self.todos_libros:
            if categoria != "Todos" and libro[4] != categoria:
                continue
            if texto in libro[0].lower() or texto in libro[1].lower():
                filtrados.append(libro)
        self.libros_filtrados = filtrados
        self.actualizar_tabla()

class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca Digital")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        self.colores = {
            "jet_black": "#202C39",
            "dark_gray": "#283845",
            "dry_sage": "#B8B08D",
            "soft_peach": "#F2D492",
            "tangerine": "#F29559"
        }

        self.autenticador = Autenticador()
        self.usuario_actual = None
        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground=self.colores["jet_black"],
                        fieldbackground="white", rowheight=25)
        style.map("Treeview", background=[("selected", self.colores["tangerine"])])
        style.configure("Treeview.Heading", background=self.colores["dark_gray"],
                        foreground="white", relief="flat")
        style.configure("TEntry", fieldbackground="white", foreground=self.colores["jet_black"])

    def crear_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.colores["soft_peach"])
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = tk.Frame(main_frame, bg=self.colores["jet_black"], height=50)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)

        tk.Label(top_frame, text="Biblioteca", font=("Segoe UI", 14, "bold"),
                 bg=self.colores["jet_black"], fg=self.colores["soft_peach"]).pack(side=tk.LEFT, padx=10)

        self.busqueda_var = tk.StringVar()
        self.busqueda_var.trace("w", self.filtrar_libros)
        entrada = ttk.Entry(top_frame, textvariable=self.busqueda_var, font=("Segoe UI", 10))
        entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        self.boton_usuario = tk.Button(top_frame, text="Iniciar sesión",
                                        bg=self.colores["tangerine"], fg=self.colores["jet_black"],
                                        command=self.abrir_login)
        self.boton_usuario.pack(side=tk.RIGHT, padx=5, pady=10)

        tk.Button(top_frame, text="⚙ Ajustes", bg=self.colores["tangerine"],
                  fg=self.colores["jet_black"]).pack(side=tk.RIGHT, padx=5)

        content_frame = tk.Frame(main_frame, bg=self.colores["soft_peach"])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.categorias = PanelCategorias(content_frame, self.colores, self.cambiar_categoria)
        self.categorias.pack(side=tk.LEFT, fill=tk.Y, padx=(0,5))

        self.libros = PanelLibros(content_frame, self.colores)
        self.libros.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        status_frame = tk.Frame(main_frame, bg=self.colores["jet_black"], height=25)
        status_frame.pack(fill=tk.X)
        self.status_label = tk.Label(status_frame, text="6 libros en catálogo",
                                      bg=self.colores["jet_black"], fg=self.colores["soft_peach"])
        self.status_label.pack(side=tk.LEFT, padx=5)

    def filtrar_libros(self, *args):
        texto = self.busqueda_var.get()
        categoria = self.categorias.categoria_actual if hasattr(self.categorias, 'categoria_actual') else "Todos"
        self.libros.filtrar(texto, categoria)

    def cambiar_categoria(self, categoria):
        self.categorias.categoria_actual = categoria
        self.filtrar_libros()

    def abrir_login(self):
        if self.usuario_actual:
            self.usuario_actual = None
            self.boton_usuario.config(text="Iniciar sesión")
            return
        VentanaLogin(self.root, self.autenticador, self.login_exitoso)

    def login_exitoso(self, usuario):
        self.usuario_actual = usuario
        self.boton_usuario.config(text=f"{usuario} (cerrar)")

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()