import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from constants import COLORES
from auth import Autenticador

class VentanaLogin(ctk.CTkToplevel):
    def __init__(self, padre, autenticador, callback_exito):
        super().__init__(padre)
        self.autenticador = autenticador
        self.callback_exito = callback_exito
        self.title("Iniciar sesión / Registro")
        self.geometry("450x500")
        self.resizable(False, False)
        self.transient(padre)
        self.grab_set()
        self.modo = "login"

        
        self.colores = COLORES

        self.crear_widgets()

    def crear_widgets(self):
        # Título
        ctk.CTkLabel(
            self, text="Biblioteca Digital",
            font=("Segoe UI", 16, "bold"),
            text_color=self.colores["jet_black"]
        ).pack(pady=10)

       
        self.tabview = ctk.CTkTabview(self, fg_color=self.colores["soft_peach"])
        self.tabview.pack(pady=10, padx=20, fill="both", expand=True)

        self.tab_login = self.tabview.add("Iniciar sesión")
        self.tab_registro = self.tabview.add("Registrarse")

        self.crear_login()
        self.crear_registro()

    def crear_login(self):
        frame = self.tab_login
        self.login_entries = {}

        
        ctk.CTkLabel(frame, text="Usuario:", text_color=self.colores["jet_black"]).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        entry_usuario = ctk.CTkEntry(frame)
        entry_usuario.grid(row=0, column=1, padx=10, pady=8)
        self.login_entries["Usuario:"] = entry_usuario

        
        ctk.CTkLabel(frame, text="Contraseña:", text_color=self.colores["jet_black"]).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        entry_pass = ctk.CTkEntry(frame, show="*")
        entry_pass.grid(row=1, column=1, padx=10, pady=8)
        self.login_entries["Contraseña:"] = entry_pass

        
        btn = ctk.CTkButton(
            frame, text="Entrar",
            fg_color=self.colores["tangerine"],
            text_color=self.colores["jet_black"],
            command=self.procesar_login
        )
        btn.grid(row=2, columnspan=2, pady=15)

        
        self.lbl_mensaje_login = ctk.CTkLabel(frame, text="", text_color=self.colores["tangerine"])
        self.lbl_mensaje_login.grid(row=3, columnspan=2)

    def crear_registro(self):
        frame = self.tab_registro
        self.reg_entries = {}

        campos = [
            ("Nombre completo:", 0),
            ("Correo electrónico:", 1),
            ("Teléfono:", 2),
            ("Usuario:", 3),
            ("Contraseña:", 4),
            ("Confirmar contraseña:", 5)
        ]

        for texto, fila in campos:
            ctk.CTkLabel(frame, text=texto, text_color=self.colores["jet_black"]).grid(row=fila, column=0, padx=10, pady=5, sticky="e")
            show = "*" if "Contraseña" in texto else ""
            entry = ctk.CTkEntry(frame, show=show)
            entry.grid(row=fila, column=1, padx=10, pady=5)
            self.reg_entries[texto] = entry

        
        ctk.CTkLabel(frame, text="Fecha de nacimiento:", text_color=self.colores["jet_black"]).grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.fecha_entry = ctk.CTkEntry(frame)
        self.fecha_entry.grid(row=6, column=1, padx=10, pady=5)

    
        btn = ctk.CTkButton(
            frame, text="Registrarse",
            fg_color=self.colores["tangerine"],
            text_color=self.colores["jet_black"],
            command=self.procesar_registro
        )
        btn.grid(row=7, columnspan=2, pady=15)

        
        self.lbl_mensaje_reg = ctk.CTkLabel(frame, text="", text_color=self.colores["tangerine"])
        self.lbl_mensaje_reg.grid(row=8, columnspan=2)

    def procesar_login(self):
        usuario = self.login_entries["Usuario:"].get()
        password = self.login_entries["Contraseña:"].get()
        if self.autenticador.iniciar_sesion(usuario, password):
            self.callback_exito(usuario)
            self.destroy()
        else:
            self.lbl_mensaje_login.configure(text="Usuario o contraseña incorrectos")

    def procesar_registro(self):
        datos = {k: v.get() for k, v in self.reg_entries.items()}
        fecha = self.fecha_entry.get()
        if any(not v for v in datos.values()) or not fecha:
            self.lbl_mensaje_reg.configure(text="Todos los campos son obligatorios")
            return
        if datos["Contraseña:"] != datos["Confirmar contraseña:"]:
            self.lbl_mensaje_reg.configure(text="Las contraseñas no coinciden")
            return
        exito = self.autenticador.registrar(
            datos["Nombre completo:"],
            datos["Correo electrónico:"],
            datos["Teléfono:"],
            datos["Usuario:"],
            datos["Contraseña:"]
        )
        if exito:
            CTkMessagebox(self, title="Registro", message="Usuario registrado con éxito. Ya puede iniciar sesión.", icon="info")
            self.tabview.set("Iniciar sesión")
            self.limpiar_registro()
        else:
            self.lbl_mensaje_reg.configure(text="El nombre de usuario ya existe")

    def limpiar_registro(self):
        for entry in self.reg_entries.values():
            entry.delete(0, "end")
        self.fecha_entry.delete(0, "end")
        self.lbl_mensaje_reg.configure(text="")

class PanelCategorias(ctk.CTkFrame):
    def __init__(self, padre, colores, callback_categoria):
        super().__init__(padre, fg_color=colores["dry_sage"], corner_radius=0)
        self.colores = colores
        self.callback = callback_categoria
        self.botones = []
        self.categorias = ["Todos", "Ficción", "No ficción", "Infantil", "Revistas", "Tesis"]
        self.crear_botones()

    def crear_botones(self):
        ctk.CTkLabel(
            self, text="Categorías",
            font=("Segoe UI", 12, "bold"),
            text_color=self.colores["jet_black"]
        ).pack(pady=10)

        for cat in self.categorias:
            btn = ctk.CTkButton(
                self, text=cat,
                fg_color=self.colores["soft_peach"],
                text_color=self.colores["jet_black"],
                hover_color=self.colores["tangerine"],
                command=lambda c=cat: self.seleccionar(c)
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.botones.append(btn)

    def seleccionar(self, categoria):
        for btn in self.botones:
            if btn.cget("text") == categoria:
                btn.configure(fg_color=self.colores["tangerine"])
            else:
                btn.configure(fg_color=self.colores["soft_peach"])
        self.callback(categoria)

class PanelLibros(ctk.CTkFrame):
    def __init__(self, padre, colores):
        super().__init__(padre, fg_color=colores["soft_peach"], corner_radius=0)
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
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

    
        self.encabezados = ["Título", "Autor", "Año", "Estado"]
        for i, texto in enumerate(self.encabezados):
            lbl = ctk.CTkLabel(
                self.scroll_frame, text=texto,
                font=("Segoe UI", 12, "bold"),
                text_color=self.colores["jet_black"]
            )
            lbl.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            
            self.scroll_frame.grid_columnconfigure(i, weight=1 if i < 2 else 0)

        
        separator = ctk.CTkFrame(self.scroll_frame, height=2, fg_color=self.colores["jet_black"])
        separator.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)

        self.filas = []  
        self.actualizar_tabla()

    def actualizar_tabla(self):
       
        for fila in self.filas:
            for widget in fila:
                widget.destroy()
        self.filas.clear()

        
        for idx, libro in enumerate(self.libros_filtrados):
            fila_widgets = []
            for col, valor in enumerate(libro[:4]):
                lbl = ctk.CTkLabel(
                    self.scroll_frame, text=str(valor),
                    text_color=self.colores["jet_black"]
                )
                lbl.grid(row=idx+2, column=col, padx=5, pady=2, sticky="w")
                fila_widgets.append(lbl)
            self.filas.append(fila_widgets)

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

class BibliotecaGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca Digital")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.colores = COLORES

        self.autenticador = Autenticador()
        self.usuario_actual = None
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color=self.colores["soft_peach"])
        main_frame.pack(fill="both", expand=True)

        # Barra superior
        top_frame = ctk.CTkFrame(main_frame, fg_color=self.colores["jet_black"], height=50)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)

        ctk.CTkLabel(
            top_frame, text="Biblioteca",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colores["soft_peach"]
        ).pack(side="left", padx=10)

        self.busqueda_var = ctk.StringVar()
        self.busqueda_var.trace("w", self.filtrar_libros)
        entrada_busqueda = ctk.CTkEntry(
            top_frame, textvariable=self.busqueda_var,
            placeholder_text="Buscar por título o autor..."
        )
        entrada_busqueda.pack(side="left", fill="x", expand=True, padx=10)

        self.boton_usuario = ctk.CTkButton(
            top_frame, text="Iniciar sesión",
            fg_color=self.colores["tangerine"],
            text_color=self.colores["jet_black"],
            hover_color="#d97e44",
            command=self.abrir_login
        )
        self.boton_usuario.pack(side="right", padx=5, pady=10)

        ctk.CTkButton(
            top_frame, text="⚙ Ajustes",
            fg_color=self.colores["tangerine"],
            text_color=self.colores["jet_black"],
            hover_color="#d97e44"
        ).pack(side="right", padx=5)

        
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.colores["soft_peach"])
        content_frame.pack(fill="both", expand=True, pady=5)

        self.categorias = PanelCategorias(content_frame, self.colores, self.cambiar_categoria)
        self.categorias.pack(side="left", fill="y", padx=(0,5))

        self.libros = PanelLibros(content_frame, self.colores)
        self.libros.pack(side="right", fill="both", expand=True)

        
        status_frame = ctk.CTkFrame(main_frame, fg_color=self.colores["jet_black"], height=25)
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            status_frame, text="6 libros en catálogo",
            text_color=self.colores["soft_peach"]
        )
        self.status_label.pack(side="left", padx=5)

    def filtrar_libros(self, *args):
        texto = self.busqueda_var.get()
        categoria = getattr(self.categorias, 'categoria_actual', "Todos")
        self.libros.filtrar(texto, categoria)

    def cambiar_categoria(self, categoria):
        self.categorias.categoria_actual = categoria
        self.filtrar_libros()

    def abrir_login(self):
        if self.usuario_actual:
            
            self.usuario_actual = None
            self.boton_usuario.configure(text="Iniciar sesión")
            return
        VentanaLogin(self, self.autenticador, self.login_exitoso)

    def login_exitoso(self, usuario):
        self.usuario_actual = usuario
        self.boton_usuario.configure(text=f"{usuario} (cerrar)")