import importlib
import re
import tkinter as tk
from tkinter import messagebox, ttk

from mysql.connector import Error

from conexion1 import eliminar_donante, guardar_donante, listar_donantes

DEPARTAMENTOS = (
    "Beni", "Chuquisaca", "Cochabamba", "La Paz", "Oruro",
    "Pando", "Potosi", "Santa Cruz", "Tarija",
)

root = tk.Tk()
root.title("Gestión de Donantes")
root.geometry("820x590")
root.configure(bg="#f4f6f9")
root.resizable(False, False)

donante_seleccionado = None  # None = registrando uno nuevo
donante_activo_id = None     # ID del donante recién guardado o seleccionado en la tabla

# ---------- Estilos ----------
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
style.configure("Header.TLabel", background="#f4f6f9", font=("Segoe UI", 14, "bold"))
style.configure("Section.TLabel", background="#ffffff", font=("Segoe UI", 11, "bold"))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

# ---------- Encabezado ----------
header = tk.Frame(root, bg="#f4f6f9")
header.pack(fill="x", padx=20, pady=(15, 6))
ttk.Label(header, text="GESTIÓN DE DONANTES", style="Header.TLabel").pack(side="left")
tk.Button(
    header, text="+ Nuevo Donante", bg="#007bff", fg="white",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5,
    command=lambda: limpiar_formulario(),
).pack(side="right")


def ir_a_aldeas():
    if donante_activo_id is None:
        messagebox.showwarning(
            "Selecciona un donante",
            "Primero registra un donante nuevo o selecciona uno de la tabla.",
            parent=root,
        )
        return
    try:
        modulo = importlib.import_module("programa")
    except ModuleNotFoundError as error:
        if error.name != "programa":
            raise
        messagebox.showinfo("En construcción",
                            "La pantalla de Aldeas todavía no está lista.", parent=root)
        return
    modulo.abrir(root, id_donante=donante_activo_id)


# ---------- Barra de navegación ----------
nav = tk.Frame(root, bg="#f4f6f9")
nav.pack(fill="x", padx=20, pady=(0, 8))
tk.Label(nav, text="Donantes", bg="#0084B4", fg="white",
         font=("Segoe UI", 9, "bold"), padx=12, pady=4).pack(side="left")

btn_ir_aldeas = tk.Button(
    nav, text="Ir a Aldeas ➔", bg="#28a745", fg="white",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=4,
    command=ir_a_aldeas,
)
btn_ir_aldeas.pack(side="right")


def actualizar_boton_aldeas(id_donante):
    global donante_activo_id
    donante_activo_id = id_donante
    if donante_activo_id is not None:
        btn_ir_aldeas.config(text=f"Ir a Aldeas (ID #{donante_activo_id}) ➔")
    else:
        btn_ir_aldeas.config(text="Ir a Aldeas ➔")


# ---------- Formulario ----------
form = tk.Frame(root, bg="#ffffff", highlightbackground="#dcdcdc", highlightthickness=1)
form.pack(fill="x", padx=20, pady=5)

titulo_formulario = ttk.Label(form, text="REGISTRAR DONANTE", style="Section.TLabel")
titulo_formulario.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 10))

ttk.Label(form, text="Nombre completo *").grid(row=1, column=0, sticky="w", padx=15)
ttk.Label(form, text="Correo electrónico *").grid(row=1, column=1, sticky="w", padx=15)
entry_nombre = ttk.Entry(form, width=42)
entry_nombre.grid(row=2, column=0, sticky="w", padx=15, pady=(2, 10))
entry_email = ttk.Entry(form, width=42)
entry_email.grid(row=2, column=1, sticky="w", padx=15, pady=(2, 10))

ttk.Label(form, text="Departamento *").grid(row=3, column=0, sticky="w", padx=15)
label_contrasena = ttk.Label(form, text="Contraseña del donante *")
label_contrasena.grid(row=3, column=1, sticky="w", padx=15)
combo_departamento = ttk.Combobox(form, width=39, state="readonly", values=DEPARTAMENTOS)
combo_departamento.grid(row=4, column=0, sticky="w", padx=15, pady=(2, 10))
entry_contrasena = ttk.Entry(form, width=42, show="*")
entry_contrasena.grid(row=4, column=1, sticky="w", padx=15, pady=(2, 10))

botones = tk.Frame(form, bg="#ffffff")
botones.grid(row=5, column=1, sticky="e", padx=15, pady=(2, 15))
tk.Button(
    botones, text="Cancelar", bg="#e2e6ea", relief="flat", padx=12, pady=4,
    command=lambda: limpiar_formulario(),
).pack(side="left", padx=5)
btn_guardar = tk.Button(
    botones, text="Guardar Datos", bg="#28a745", fg="white",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=4,
    command=lambda: guardar_desde_formulario(),
)
btn_guardar.pack(side="left")

# ---------- Tabla ----------
tabla_frame = tk.Frame(root, bg="#ffffff", highlightbackground="#dcdcdc", highlightthickness=1)
tabla_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
ttk.Label(tabla_frame, text="DIRECTORIO DE DONANTES", style="Section.TLabel").pack(
    anchor="w", padx=15, pady=(12, 8)
)

filtros = tk.Frame(tabla_frame, bg="#ffffff")
filtros.pack(fill="x", padx=15, pady=(0, 10))
ttk.Label(filtros, text="Buscar (ID, Nombre, Email, Departamento):").pack(side="left")
entrada_busqueda = ttk.Entry(filtros, width=25)
entrada_busqueda.pack(side="left", padx=(5, 10))

tk.Button(
    filtros, text="Recargar Lista", bg="#e2e6ea", relief="flat", padx=10,
    command=lambda: refrescar_tabla(),
).pack(side="right", padx=(5, 0))
tk.Button(
    filtros, text="Eliminar", bg="#dc3545", fg="white",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=10,
    command=lambda: eliminar_desde_tabla(),
).pack(side="right", padx=(5, 0))
tk.Button(
    filtros, text="Editar Seleccionado", bg="#ffc107", fg="#212529",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=10,
    command=lambda: cargar_seleccion_en_formulario(),
).pack(side="right")

columnas = ("id_donante", "nombre", "email", "departamento")
tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=6)
for columna, titulo, ancho, ancla in (
    ("id_donante", "ID", 70, "center"),
    ("nombre", "Nombre", 230, "w"),
    ("email", "Email", 250, "w"),
    ("departamento", "Departamento", 180, "w"),
):
    tabla.heading(columna, text=titulo)
    tabla.column(columna, width=ancho, anchor=ancla)
tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))


# ---------- Funciones ----------
def mostrar_error(error):
    messagebox.showerror("Error de base de datos", str(error), parent=root)


def cargar_donantes(*_):
    try:
        donantes = listar_donantes(entrada_busqueda.get().strip())
    except Error as error:
        mostrar_error(error)
        return
    tabla.delete(*tabla.get_children())
    for id_donante, nombre, email, departamento in donantes:
        tabla.insert("", "end", values=(id_donante, nombre, email, departamento or ""))


def refrescar_tabla():
    entrada_busqueda.delete(0, tk.END)
    limpiar_formulario(limpiar_activo=True)
    cargar_donantes()
    messagebox.showinfo("Lista actualizada", "El directorio de donantes se ha recargado.", parent=root)


def cargar_seleccion_en_formulario():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning(
            "Sin selección",
            "Haz clic sobre un donante en la tabla primero para editarlo.",
            parent=root,
        )
        return
    seleccionar_donante()
    entry_nombre.focus()


def seleccionar_donante(_event=None):
    global donante_seleccionado
    seleccion = tabla.selection()
    if not seleccion:
        return
    valores = tabla.item(seleccion[0], "values")
    if not valores:
        return
    id_donante, nombre, email, departamento = valores
    donante_seleccionado = int(id_donante)
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, nombre)
    entry_email.delete(0, tk.END)
    entry_email.insert(0, email)
    combo_departamento.set(departamento)
    entry_contrasena.delete(0, tk.END)
    titulo_formulario.config(text=f"EDITAR DONANTE (ID #{donante_seleccionado})")
    label_contrasena.config(text="Nueva contraseña (opcional)")
    btn_guardar.config(text="Guardar Cambios")
    actualizar_boton_aldeas(donante_seleccionado)


def limpiar_formulario(limpiar_activo=True):
    global donante_seleccionado
    donante_seleccionado = None
    entry_nombre.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)
    combo_departamento.set("")
    if tabla.selection():
        tabla.selection_remove(*tabla.selection())
    titulo_formulario.config(text="REGISTRAR DONANTE")
    label_contrasena.config(text="Contraseña del donante *")
    btn_guardar.config(text="Guardar Datos")
    if limpiar_activo:
        actualizar_boton_aldeas(None)


def guardar_desde_formulario():
    nombre = entry_nombre.get().strip()
    email = entry_email.get().strip()
    departamento = combo_departamento.get().strip()
    contrasena = entry_contrasena.get().strip()
    id_editando = donante_seleccionado
    es_nuevo = id_editando is None

    if not nombre or not email or not departamento:
        messagebox.showwarning(
            "Datos incompletos",
            "Completa el nombre, el correo y selecciona un departamento.",
            parent=root,
        )
        return
    if es_nuevo and not contrasena:
        messagebox.showwarning(
            "Datos incompletos", "Ingresa una contraseña para el nuevo donante.", parent=root
        )
        return
    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
        messagebox.showerror(
            "Error de registro", "El nombre no puede contener números ni símbolos.", parent=root
        )
        return
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        messagebox.showwarning(
            "Correo inválido", "Ingresa un correo electrónico válido.", parent=root
        )
        return

    try:
        resultado = guardar_donante(nombre, email, departamento, contrasena, id_editando)
    except Error as error:
        mostrar_error(error)
        return

    cargar_donantes()

    if not es_nuevo:
        id_actual = id_editando
    elif isinstance(resultado, int):
        id_actual = resultado
    else:
        todos = listar_donantes("")
        id_actual = max((d[0] for d in todos), default=None)

    limpiar_formulario(limpiar_activo=False)
    actualizar_boton_aldeas(id_actual)

    accion = "registraron" if es_nuevo else "actualizaron"
    messagebox.showinfo(
        "Guardado",
        f"Los datos del donante (ID #{id_actual}) se {accion} correctamente.\nHaz clic en 'Ir a Aldeas' para continuar.",
        parent=root,
    )


def eliminar_desde_tabla():
    if donante_seleccionado is None:
        messagebox.showwarning(
            "Sin selección", "Selecciona un donante de la tabla para eliminarlo.", parent=root
        )
        return
    if not messagebox.askyesno(
        "Confirmar eliminación", "¿Estás seguro de que deseas eliminar este donante?", parent=root
    ):
        return
    try:
        eliminar_donante(donante_seleccionado)
    except Error as error:
        mostrar_error(error)
        return
    limpiar_formulario(limpiar_activo=True)
    cargar_donantes()
    messagebox.showinfo("Eliminado", "El donante fue eliminado correctamente.", parent=root)


entrada_busqueda.bind("<KeyRelease>", cargar_donantes)
tabla.bind("<<TreeviewSelect>>", seleccionar_donante)
tabla.bind("<ButtonRelease-1>", seleccionar_donante)

cargar_donantes()
root.mainloop()
