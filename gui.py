# gui.py
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from constants import COLORES, LOGO_PATH
from models.usuario import UsuarioRepository
from models.libro import LibroRepository, CategoriaRepository
from models.compra import CompraRepository
from datetime import datetime

# ------------------------------------------------------------
# Ventana de historial
# ------------------------------------------------------------
class HistorialView(ctk.CTkToplevel):
    def __init__(self, padre, compra_repo, usuario):
        super().__init__(padre)
        self.title("Historial de préstamos")
        self.geometry("500x400")
        self.transient(padre)
        self.grab_set()

        self.compra_repo = compra_repo
        self.usuario = usuario

        frame = ctk.CTkFrame(self, fg_color=COLORES["soft_peach"])
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text=f"Historial de {usuario.nombre}", font=("Segoe UI", 14, "bold"),
                     text_color=COLORES["jet_black"]).pack(pady=5)

        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        prestamos = self.compra_repo.obtener_historial(usuario.id)
        if not prestamos:
            ctk.CTkLabel(scroll, text="No hay préstamos registrados",
                         text_color=COLORES["jet_black"]).pack(pady=10)
        else:
            for libro, fecha in prestamos:
                lbl = ctk.CTkLabel(scroll, text=f"{libro} - {fecha}",
                                   text_color=COLORES["jet_black"])
                lbl.pack(anchor="w", padx=5, pady=2)

        ctk.CTkButton(frame, text="Cerrar", command=self.destroy,
                      fg_color=COLORES["tangerine"],
                      text_color=COLORES["jet_black"]).pack(pady=10)


# ------------------------------------------------------------
# Ventana de lista de usuarios (admin)
# ------------------------------------------------------------
class AdminUsersView(ctk.CTkToplevel):
    def __init__(self, padre, usuario_repo):
        super().__init__(padre)
        self.title("Usuarios Registrados")
        self.geometry("600x400")
        self.transient(padre)
        self.grab_set()

        self.usuario_repo = usuario_repo

        frame = ctk.CTkFrame(self, fg_color=COLORES["soft_peach"])
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Lista de Usuarios", font=("Segoe UI", 14, "bold"),
                     text_color=COLORES["jet_black"]).pack(pady=5)

        # Contador total
        count = self.usuario_repo.obtener_cantidad_usuarios()
        ctk.CTkLabel(frame, text=f"Total: {count} usuarios", text_color=COLORES["jet_black"]).pack(pady=5)

        # Tabla scrollable
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, pady=5)

        headers = ["ID", "Nombre", "Email", "Teléfono", "Rol"]
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(scroll, text=text, font=("Segoe UI", 12, "bold"),
                               text_color=COLORES["jet_black"])
            lbl.grid(row=0, column=col, padx=5, pady=5, sticky="w")

        users = self.usuario_repo.obtener_todos_usuarios()
        for row_idx, user in enumerate(users):
            for col_idx, value in enumerate(user):
                lbl = ctk.CTkLabel(scroll, text=str(value), text_color=COLORES["jet_black"])
                lbl.grid(row=row_idx+1, column=col_idx, padx=5, pady=2, sticky="w")

        ctk.CTkButton(frame, text="Cerrar", command=self.destroy,
                      fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"]).pack(pady=10)


# ------------------------------------------------------------
# Panel de administración (libros, categorías, usuarios)
# ------------------------------------------------------------
class AdminPanel(ctk.CTkToplevel):
    def __init__(self, padre, libro_repo, categoria_repo, usuario_repo, callback_actualizar):
        super().__init__(padre)
        self.title("Panel de administración")
        self.geometry("800x600")
        self.transient(padre)
        self.grab_set()

        self.libro_repo = libro_repo
        self.categoria_repo = categoria_repo
        self.usuario_repo = usuario_repo
        self.callback_actualizar = callback_actualizar

        self.tabview = ctk.CTkTabview(self, fg_color=COLORES["soft_peach"])
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_libros = self.tabview.add("Libros")
        self.tab_categorias = self.tabview.add("Categorías")
        self.tab_usuarios = self.tabview.add("Usuarios")

        self.crear_tab_libros()
        self.crear_tab_categorias()
        self.crear_tab_usuarios()

    def crear_tab_libros(self):
        # Formulario para agregar/editar libro
        frame_form = ctk.CTkFrame(self.tab_libros, fg_color=COLORES["dry_sage"])
        frame_form.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(frame_form, text="Título:", text_color=COLORES["jet_black"]).grid(row=0, column=0, padx=5, pady=5)
        self.entry_titulo = ctk.CTkEntry(frame_form)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_form, text="Autor:", text_color=COLORES["jet_black"]).grid(row=1, column=0, padx=5, pady=5)
        self.entry_autor = ctk.CTkEntry(frame_form)
        self.entry_autor.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_form, text="Año:", text_color=COLORES["jet_black"]).grid(row=2, column=0, padx=5, pady=5)
        self.entry_anio = ctk.CTkEntry(frame_form)
        self.entry_anio.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_form, text="Precio:", text_color=COLORES["jet_black"]).grid(row=3, column=0, padx=5, pady=5)
        self.entry_precio = ctk.CTkEntry(frame_form)
        self.entry_precio.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_form, text="Stock:", text_color=COLORES["jet_black"]).grid(row=4, column=0, padx=5, pady=5)
        self.entry_stock = ctk.CTkEntry(frame_form)
        self.entry_stock.grid(row=4, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_form, text="Categoría:", text_color=COLORES["jet_black"]).grid(row=5, column=0, padx=5, pady=5)
        self.combo_categoria = ctk.CTkComboBox(frame_form, values=self.categoria_repo.obtener_nombres())
        self.combo_categoria.grid(row=5, column=1, padx=5, pady=5)

        # Botones
        btn_agregar = ctk.CTkButton(frame_form, text="Agregar libro",
                                    fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"],
                                    command=self.agregar_libro)
        btn_agregar.grid(row=6, column=0, pady=10)

        btn_editar = ctk.CTkButton(frame_form, text="Editar seleccionado",
                                   fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"],
                                   command=self.editar_libro)
        btn_editar.grid(row=6, column=1, pady=10)

        btn_eliminar = ctk.CTkButton(frame_form, text="Eliminar seleccionado",
                                     fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"],
                                     command=self.eliminar_libro)
        btn_eliminar.grid(row=7, column=0, columnspan=2, pady=5)

        # Lista de libros
        scroll = ctk.CTkScrollableFrame(self.tab_libros, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.lista_libros = ctk.CTkTextbox(scroll, height=300, fg_color=COLORES["soft_peach"],
                                           text_color=COLORES["jet_black"])
        self.lista_libros.pack(fill="both", expand=True)
        self.actualizar_lista_libros()

    def actualizar_lista_libros(self):
        self.lista_libros.delete("0.0", "end")
        libros = self.libro_repo.get_all()
        for i, libro in enumerate(libros):
            self.lista_libros.insert("end", f"{i+1}. {libro.titulo} - {libro.autor} ({libro.year}) [Stock: {libro.stock}] - {libro.category}\n")

    def agregar_libro(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        anio = self.entry_anio.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        categoria = self.combo_categoria.get()

        if not all([titulo, autor, anio, precio, stock, categoria]):
            CTkMessagebox(self, title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return
        try:
            anio = int(anio)
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            CTkMessagebox(self, title="Error", message="Año, precio y stock deben ser números válidos", icon="cancel")
            return

        from models.libro import Libro
        nuevo_libro = Libro(None, titulo, autor, precio, stock, anio, categoria)
        self.libro_repo.agregar(nuevo_libro)
        self.actualizar_lista_libros()
        self.callback_actualizar()
        self.limpiar_formulario_libro()

    def editar_libro(self):
        try:
            linea = self.lista_libros.index("sel.first")
        except:
            CTkMessagebox(self, title="Error", message="Seleccione un libro de la lista", icon="cancel")
            return
        indice = int(linea.split(".")[0]) - 1
        libros = self.libro_repo.get_all()
        if indice < 0 or indice >= len(libros):
            return
        libro = libros[indice]

        # Llenar formulario con datos actuales
        self.entry_titulo.delete(0, "end")
        self.entry_titulo.insert(0, libro.titulo)
        self.entry_autor.delete(0, "end")
        self.entry_autor.insert(0, libro.autor)
        self.entry_anio.delete(0, "end")
        self.entry_anio.insert(0, str(libro.year))
        self.entry_precio.delete(0, "end")
        self.entry_precio.insert(0, str(libro.precio))
        self.entry_stock.delete(0, "end")
        self.entry_stock.insert(0, str(libro.stock))
        self.combo_categoria.set(libro.category)

        # Botón de guardar cambios (reemplazar temporalmente)
        self.btn_guardar = ctk.CTkButton(self.tab_libros, text="Guardar cambios",
                                         fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"],
                                         command=lambda: self.guardar_edicion(indice))
        self.btn_guardar.pack(pady=5)

    def guardar_edicion(self, indice):
        libro = self.libro_repo.get_all()[indice]
        libro.titulo = self.entry_titulo.get()
        libro.autor = self.entry_autor.get()
        try:
            libro.year = int(self.entry_anio.get())
            libro.precio = float(self.entry_precio.get())
            libro.stock = int(self.entry_stock.get())
        except ValueError:
            CTkMessagebox(self, title="Error", message="Datos inválidos", icon="cancel")
            return
        libro.category = self.combo_categoria.get()
        self.libro_repo.actualizar(libro)
        self.actualizar_lista_libros()
        self.callback_actualizar()
        self.limpiar_formulario_libro()
        if hasattr(self, 'btn_guardar'):
            self.btn_guardar.destroy()

    def eliminar_libro(self):
        try:
            linea = self.lista_libros.index("sel.first")
        except:
            CTkMessagebox(self, title="Error", message="Seleccione un libro de la lista", icon="cancel")
            return
        indice = int(linea.split(".")[0]) - 1
        libros = self.libro_repo.get_all()
        if indice < 0 or indice >= len(libros):
            return
        libro = libros[indice]
        if CTkMessagebox(self, title="Confirmar", message=f"¿Eliminar '{libro.titulo}'?", icon="question", option_1="Sí", option_2="No").get() == "Sí":
            self.libro_repo.eliminar(libro.id)
            self.actualizar_lista_libros()
            self.callback_actualizar()

    def limpiar_formulario_libro(self):
        self.entry_titulo.delete(0, "end")
        self.entry_autor.delete(0, "end")
        self.entry_anio.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_stock.delete(0, "end")
        categorias = self.categoria_repo.obtener_nombres()
        self.combo_categoria.set(categorias[0] if categorias else "")

    def crear_tab_categorias(self):
        scroll = ctk.CTkScrollableFrame(self.tab_categorias, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.lista_categorias = ctk.CTkTextbox(scroll, height=300, fg_color=COLORES["soft_peach"],
                                               text_color=COLORES["jet_black"])
        self.lista_categorias.pack(fill="both", expand=True)
        self.actualizar_lista_categorias()

        frame_form = ctk.CTkFrame(self.tab_categorias, fg_color=COLORES["dry_sage"])
        frame_form.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(frame_form, text="Nueva categoría:", text_color=COLORES["jet_black"]).pack(side="left", padx=5)
        self.entry_categoria = ctk.CTkEntry(frame_form)
        self.entry_categoria.pack(side="left", padx=5, expand=True, fill="x")

        btn_agregar = ctk.CTkButton(frame_form, text="Agregar",
                                    fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"],
                                    command=self.agregar_categoria)
        btn_agregar.pack(side="left", padx=5)

        btn_eliminar = ctk.CTkButton(frame_form, text="Eliminar seleccionada",
                                     fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"],
                                     command=self.eliminar_categoria)
        btn_eliminar.pack(side="left", padx=5)

    def actualizar_lista_categorias(self):
        self.lista_categorias.delete("0.0", "end")
        categorias = self.categoria_repo.obtener_nombres()
        for i, cat in enumerate(categorias):
            self.lista_categorias.insert("end", f"{i+1}. {cat}\n")

    def agregar_categoria(self):
        nueva = self.entry_categoria.get().strip()
        if not nueva:
            return
        if nueva in self.categoria_repo.obtener_nombres():
            CTkMessagebox(self, title="Error", message="La categoría ya existe", icon="cancel")
            return
        self.categoria_repo.agregar(nueva)
        self.actualizar_lista_categorias()
        self.combo_categoria.configure(values=self.categoria_repo.obtener_nombres())
        self.callback_actualizar()

    def eliminar_categoria(self):
        try:
            linea = self.lista_categorias.index("sel.first")
        except:
            CTkMessagebox(self, title="Error", message="Seleccione una categoría", icon="cancel")
            return
        indice = int(linea.split(".")[0]) - 1
        categorias = self.categoria_repo.obtener_nombres()
        if indice < 0 or indice >= len(categorias):
            return
        cat = categorias[indice]
        if cat in ["Todos", "Ficción", "No ficción", "Infantil", "Revistas", "Tesis"]:
            CTkMessagebox(self, title="Error", message="No se puede eliminar una categoría predeterminada", icon="cancel")
            return
        self.categoria_repo.eliminar(cat)
        self.actualizar_lista_categorias()
        self.combo_categoria.configure(values=self.categoria_repo.obtener_nombres())
        self.callback_actualizar()

    def crear_tab_usuarios(self):
        frame = self.tab_usuarios
        ctk.CTkLabel(frame, text="Gestión de Usuarios", font=("Segoe UI", 14, "bold"),
                     text_color=COLORES["jet_black"]).pack(pady=10)

        btn_ver = ctk.CTkButton(frame, text="Ver todos los usuarios",
                                fg_color=COLORES["tangerine"], text_color=COLORES["jet_black"],
                                command=self.ver_usuarios)
        btn_ver.pack(pady=10)

    def ver_usuarios(self):
        AdminUsersView(self, self.usuario_repo)


# ------------------------------------------------------------
# Ventana de login/registro
# ------------------------------------------------------------
class VentanaLogin(ctk.CTkToplevel):
    def __init__(self, padre, usuario_repo, callback_exito):
        super().__init__(padre)
        self.usuario_repo = usuario_repo
        self.callback_exito = callback_exito
        self.title("Iniciar sesión / Registro")
        self.geometry("450x550")
        self.resizable(False, False)
        self.transient(padre)
        self.grab_set()

        self.colores = COLORES
        self.crear_widgets()

    def crear_widgets(self):
        ctk.CTkLabel(self, text="Biblioteca Digital", font=("Segoe UI", 16, "bold"),
                     text_color=self.colores["jet_black"]).pack(pady=10)

        self.tabview = ctk.CTkTabview(self, fg_color=self.colores["soft_peach"])
        self.tabview.pack(pady=10, padx=20, fill="both", expand=True)

        self.tab_login = self.tabview.add("Iniciar sesión")
        self.tab_registro = self.tabview.add("Registrarse")

        self.crear_login()
        self.crear_registro()

    def crear_login(self):
        frame = self.tab_login
        self.login_entries = {}

        ctk.CTkLabel(frame, text="Email:", text_color=self.colores["jet_black"]).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        entry_email = ctk.CTkEntry(frame)
        entry_email.grid(row=0, column=1, padx=10, pady=8)
        self.login_entries["Email:"] = entry_email

        ctk.CTkLabel(frame, text="Contraseña:", text_color=self.colores["jet_black"]).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        entry_pass = ctk.CTkEntry(frame, show="*")
        entry_pass.grid(row=1, column=1, padx=10, pady=8)
        self.login_entries["Contraseña:"] = entry_pass

        btn = ctk.CTkButton(frame, text="Entrar", fg_color=self.colores["tangerine"],
                            text_color=self.colores["jet_black"], command=self.procesar_login)
        btn.grid(row=2, columnspan=2, pady=15)

        self.lbl_mensaje_login = ctk.CTkLabel(frame, text="", text_color=self.colores["tangerine"])
        self.lbl_mensaje_login.grid(row=3, columnspan=2)

    def crear_registro(self):
        frame = self.tab_registro
        self.reg_entries = {}

        campos = [
            ("Nombre completo:", 0),
            ("Email:", 1),
            ("Teléfono:", 2),
            ("Fecha nacimiento (YYYYMMDD):", 3),
            ("Contraseña:", 4),
            ("Confirmar contraseña:", 5)
        ]

        for texto, fila in campos:
            ctk.CTkLabel(frame, text=texto, text_color=self.colores["jet_black"]).grid(row=fila, column=0, padx=10, pady=5, sticky="e")
            show = "*" if "Contraseña" in texto else ""
            entry = ctk.CTkEntry(frame, show=show)
            entry.grid(row=fila, column=1, padx=10, pady=5)
            self.reg_entries[texto] = entry

        # Checkbox para administrador
        self.is_admin = ctk.BooleanVar()
        cb_admin = ctk.CTkCheckBox(frame, text="Registrar como administrador", variable=self.is_admin,
                                   text_color=self.colores["jet_black"])
        cb_admin.grid(row=6, columnspan=2, pady=5)

        btn = ctk.CTkButton(frame, text="Registrarse", fg_color=self.colores["tangerine"],
                            text_color=self.colores["jet_black"], command=self.procesar_registro)
        btn.grid(row=7, columnspan=2, pady=15)

        self.lbl_mensaje_reg = ctk.CTkLabel(frame, text="", text_color=self.colores["tangerine"])
        self.lbl_mensaje_reg.grid(row=8, columnspan=2)

    def procesar_login(self):
        email = self.login_entries["Email:"].get()
        password = self.login_entries["Contraseña:"].get()
        usuario = self.usuario_repo.iniciar_sesion(email, password)
        if usuario:
            self.callback_exito(usuario)
            self.destroy()
        else:
            self.lbl_mensaje_login.configure(text="Email o contraseña incorrectos")

    def procesar_registro(self):
        datos = {k: v.get() for k, v in self.reg_entries.items()}
        if any(not v for v in datos.values()):
            self.lbl_mensaje_reg.configure(text="Todos los campos son obligatorios")
            return
        if datos["Contraseña:"] != datos["Confirmar contraseña:"]:
            self.lbl_mensaje_reg.configure(text="Las contraseñas no coinciden")
            return
        rol = "admin" if self.is_admin.get() else "usuario"
        exito = self.usuario_repo.registrar(
            datos["Nombre completo:"],
            datos["Email:"],
            datos["Teléfono:"],
            datos["Fecha nacimiento (YYYYMMDD):"],
            datos["Contraseña:"],
            rol
        )
        if exito:
            CTkMessagebox(self, title="Registro", message="Usuario registrado con éxito. Ya puede iniciar sesión.", icon="info")
            # Enviar correo de bienvenida en un hilo separado
            from utils.email_sender import send_welcome_email
            send_welcome_email(datos["Email:"], datos["Nombre completo:"])
            self.tabview.set("Iniciar sesión")
            self.limpiar_registro()
        else:
            self.lbl_mensaje_reg.configure(text="El email ya está registrado")

    def limpiar_registro(self):
        for entry in self.reg_entries.values():
            entry.delete(0, "end")
        self.lbl_mensaje_reg.configure(text="")
        self.is_admin.set(False)


# ------------------------------------------------------------
# Panel de categorías
# ------------------------------------------------------------
class PanelCategorias(ctk.CTkFrame):
    def __init__(self, padre, colores, callback_categoria, categorias):
        super().__init__(padre, fg_color=colores["dry_sage"], corner_radius=0)
        self.colores = colores
        self.callback = callback_categoria
        self.categorias = categorias
        self.botones = []
        self.categoria_actual = "Todos"
        self.crear_botones()

    def crear_botones(self):
        for btn in self.botones:
            btn.destroy()
        self.botones.clear()

        ctk.CTkLabel(self, text="Categorías", font=("Segoe UI", 12, "bold"),
                     text_color=self.colores["jet_black"]).pack(pady=10)

        for cat in self.categorias:
            btn = ctk.CTkButton(self, text=cat, fg_color=self.colores["soft_peach"],
                                text_color=self.colores["jet_black"],
                                hover_color=self.colores["tangerine"],
                                command=lambda c=cat: self.seleccionar(c))
            btn.pack(fill="x", padx=10, pady=3)
            self.botones.append(btn)

    def seleccionar(self, categoria):
        for btn in self.botones:
            if btn.cget("text") == categoria:
                btn.configure(fg_color=self.colores["tangerine"])
            else:
                btn.configure(fg_color=self.colores["soft_peach"])
        self.categoria_actual = categoria
        self.callback(categoria)

    def actualizar_categorias(self, nuevas_categorias):
        self.categorias = nuevas_categorias
        self.crear_botones()


# ------------------------------------------------------------
# Panel de libros
# ------------------------------------------------------------
class PanelLibros(ctk.CTkFrame):
    def __init__(self, padre, colores, libro_repo, compra_repo, usuario_actual_callback):
        super().__init__(padre, fg_color=colores["soft_peach"], corner_radius=0)
        self.colores = colores
        self.libro_repo = libro_repo
        self.compra_repo = compra_repo
        self.usuario_actual_callback = usuario_actual_callback
        self.todos_libros = self.libro_repo.get_all()
        self.libros_filtrados = self.todos_libros[:]
        self.crear_widgets()

    def crear_widgets(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.encabezados = ["Título", "Autor", "Año", "Estado", "Acción"]
        for i, texto in enumerate(self.encabezados):
            lbl = ctk.CTkLabel(self.scroll_frame, text=texto, font=("Segoe UI", 12, "bold"),
                               text_color=self.colores["jet_black"])
            lbl.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            self.scroll_frame.grid_columnconfigure(i, weight=1 if i < 2 else 0)

        separator = ctk.CTkFrame(self.scroll_frame, height=2, fg_color=self.colores["jet_black"])
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", pady=5)

        self.filas = []
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for fila in self.filas:
            for widget in fila:
                widget.destroy()
        self.filas.clear()

        for idx, libro in enumerate(self.libros_filtrados):
            fila_widgets = []
            valores = [libro.titulo, libro.autor, libro.year, libro.status]
            for col, valor in enumerate(valores):
                lbl = ctk.CTkLabel(self.scroll_frame, text=str(valor),
                                   text_color=self.colores["jet_black"])
                lbl.grid(row=idx+2, column=col, padx=5, pady=2, sticky="w")
                fila_widgets.append(lbl)

            btn_prestar = ctk.CTkButton(self.scroll_frame, text="Prestar",
                                        fg_color=self.colores["tangerine"],
                                        text_color=self.colores["jet_black"],
                                        width=80,
                                        command=lambda l=libro: self.prestar_libro(l))
            btn_prestar.grid(row=idx+2, column=4, padx=5, pady=2)
            fila_widgets.append(btn_prestar)

            self.filas.append(fila_widgets)

    def prestar_libro(self, libro):
        usuario = self.usuario_actual_callback()
        if not usuario:
            CTkMessagebox(self, title="Error", message="Debe iniciar sesión para prestar libros", icon="cancel")
            return
        if libro.stock <= 0:
            CTkMessagebox(self, title="Error", message="El libro no está disponible", icon="cancel")
            return
        exito = self.compra_repo.registrar_prestamo(usuario.id, libro.id)
        if exito:
            libro.stock -= 1
            libro.status = "Disponible" if libro.stock > 0 else "Prestado"
            self.actualizar_tabla()
            CTkMessagebox(self, title="Préstamo", message=f"Has tomado prestado '{libro.titulo}'.", icon="info")
        else:
            CTkMessagebox(self, title="Error", message="No se pudo realizar el préstamo", icon="cancel")

    def filtrar(self, texto, categoria):
        self.libros_filtrados = self.libro_repo.filter(texto, categoria)
        self.actualizar_tabla()


# ------------------------------------------------------------
# Ventana principal
# ------------------------------------------------------------
class BibliotecaGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca Digital")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.colores = COLORES

        # Repositorios
        self.usuario_repo = UsuarioRepository()
        self.libro_repo = LibroRepository()
        self.categoria_repo = CategoriaRepository()
        self.compra_repo = CompraRepository()

        self.usuario_actual = None
        self.crear_widgets()

        # Cargar logo si existe
        self.cargar_logo()

    def cargar_logo(self):
        try:
            from PIL import Image
            logo_img = ctk.CTkImage(Image.open(LOGO_PATH), size=(40, 40))
            self.label_logo = ctk.CTkLabel(self.top_frame, image=logo_img, text="")
            self.label_logo.pack(side="left", padx=5)
        except:
            pass

    def crear_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color=self.colores["soft_peach"])
        main_frame.pack(fill="both", expand=True)

        # Barra superior
        self.top_frame = ctk.CTkFrame(main_frame, fg_color=self.colores["jet_black"], height=50)
        self.top_frame.pack(fill="x")
        self.top_frame.pack_propagate(False)

        ctk.CTkLabel(self.top_frame, text="Biblioteca", font=("Segoe UI", 14, "bold"),
                     text_color=self.colores["soft_peach"]).pack(side="left", padx=10)

        self.busqueda_var = ctk.StringVar()
        self.busqueda_var.trace("w", self.filtrar_libros)
        entrada_busqueda = ctk.CTkEntry(self.top_frame, textvariable=self.busqueda_var,
                                        placeholder_text="Buscar por título o autor...")
        entrada_busqueda.pack(side="left", fill="x", expand=True, padx=10)

        self.boton_usuario = ctk.CTkButton(self.top_frame, text="Iniciar sesión",
                                           fg_color=self.colores["tangerine"],
                                           text_color=self.colores["jet_black"],
                                           command=self.abrir_login)
        self.boton_usuario.pack(side="right", padx=5, pady=10)

        self.boton_ajustes = ctk.CTkButton(self.top_frame, text="⚙ Ajustes",
                                           fg_color=self.colores["tangerine"],
                                           text_color=self.colores["jet_black"],
                                           command=self.abrir_ajustes)
        self.boton_ajustes.pack(side="right", padx=5)

        # Contenido principal
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.colores["soft_peach"])
        content_frame.pack(fill="both", expand=True, pady=5)

        self.categorias = PanelCategorias(content_frame, self.colores, self.cambiar_categoria,
                                          self.categoria_repo.obtener_nombres())
        self.categorias.pack(side="left", fill="y", padx=(0,5))

        self.libros = PanelLibros(content_frame, self.colores, self.libro_repo, self.compra_repo,
                                  lambda: self.usuario_actual)
        self.libros.pack(side="right", fill="both", expand=True)

        # Barra de estado
        status_frame = ctk.CTkFrame(main_frame, fg_color=self.colores["jet_black"], height=25)
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(status_frame, text=f"{len(self.libro_repo.get_all())} libros en catálogo",
                                         text_color=self.colores["soft_peach"])
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
            self.cerrar_sesion()
            return
        VentanaLogin(self, self.usuario_repo, self.login_exitoso)

    def login_exitoso(self, usuario):
        self.usuario_actual = usuario
        self.boton_usuario.configure(text=f"{usuario.nombre} (cerrar)")

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.boton_usuario.configure(text="Iniciar sesión")

    def abrir_ajustes(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Ajustes")
        ventana.geometry("300x250")
        ventana.transient(self)
        ventana.grab_set()

        frame = ctk.CTkFrame(ventana, fg_color=self.colores["soft_peach"])
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        if self.usuario_actual:
            btn_cerrar = ctk.CTkButton(frame, text="Cerrar sesión",
                                       fg_color=self.colores["tangerine"],
                                       text_color=self.colores["jet_black"],
                                       command=lambda: [self.cerrar_sesion(), ventana.destroy()])
            btn_cerrar.pack(pady=5, fill="x")

            btn_historial = ctk.CTkButton(frame, text="Ver historial",
                                          fg_color=self.colores["tangerine"],
                                          text_color=self.colores["jet_black"],
                                          command=lambda: HistorialView(ventana, self.compra_repo, self.usuario_actual))
            btn_historial.pack(pady=5, fill="x")

            if self.usuario_actual.rol == "admin":
                btn_admin = ctk.CTkButton(frame, text="Administrar",
                                          fg_color=self.colores["tangerine"],
                                          text_color=self.colores["jet_black"],
                                          command=lambda: AdminPanel(ventana, self.libro_repo, self.categoria_repo, self.usuario_repo, self.actualizar_despues_admin))
                btn_admin.pack(pady=5, fill="x")
        else:
            ctk.CTkLabel(frame, text="No has iniciado sesión", text_color=self.colores["jet_black"]).pack(pady=10)

        ctk.CTkButton(frame, text="Cerrar", command=ventana.destroy,
                      fg_color=self.colores["tangerine"], text_color=self.colores["jet_black"]).pack(pady=10)

    def actualizar_despues_admin(self):
        self.categorias.actualizar_categorias(self.categoria_repo.obtener_nombres())
        self.libros.todos_libros = self.libro_repo.get_all()
        self.libros.filtrar(self.busqueda_var.get(), self.categorias.categoria_actual)
        self.status_label.configure(text=f"{len(self.libro_repo.get_all())} libros en catálogo")