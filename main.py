import re
import tkinter as tk
from tkinter import messagebox, ttk

from mysql.connector import Error

from conexion import eliminar_donante, guardar_donante, listar_donantes

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Donantes")
root.geometry("820x550")
root.configure(bg="#f4f6f9")
root.resizable(False, False)

donantes = []
donante_seleccionado = None

DEPARTAMENTOS = (
    "Beni", "Chuquisaca", "Cochabamba", "La Paz", "Oruro",
    "Pando", "Potosi", "Santa Cruz", "Tarija"
)

# Estilos generales
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
style.configure("Header.TLabel", background="#f4f6f9", font=("Segoe UI", 14, "bold"))
style.configure("Section.TLabel", background="#ffffff", font=("Segoe UI", 11, "bold"), foreground="#333333")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

# ==========================================
# ENCABEZADO SUPERIOR
# ==========================================
header_frame = tk.Frame(root, bg="#f4f6f9")
header_frame.pack(fill="x", padx=20, pady=(15, 10))

ttk.Label(header_frame, text="GESTIÓN DE DONANTES", style="Header.TLabel").pack(side="left")
btn_nuevo = tk.Button(
    header_frame, text="+ Nuevo Donante", bg="#007bff", fg="white",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5,
    command=lambda: limpiar_formulario()
)
btn_nuevo.pack(side="right")

# ==========================================
# SECCIÓN 1: FORMULARIO (REGISTRAR / EDITAR)
# ==========================================
form_frame = tk.Frame(root, bg="#ffffff", highlightbackground="#dcdcdc", highlightthickness=1)
form_frame.pack(fill="x", padx=20, pady=5)

titulo_formulario = ttk.Label(form_frame, text="REGISTRAR DONANTE", style="Section.TLabel")
titulo_formulario.grid(
    row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 10)
)

# Fila 1: Nombre y Email
ttk.Label(form_frame, text="Nombre completo *").grid(row=1, column=0, sticky="w", padx=15)
ttk.Label(form_frame, text="Correo electrónico *").grid(row=1, column=1, sticky="w", padx=15)

entry_nombre = ttk.Entry(form_frame, width=42)
entry_nombre.grid(row=2, column=0, sticky="w", padx=15, pady=(2, 10))

entry_email = ttk.Entry(form_frame, width=42)
entry_email.grid(row=2, column=1, sticky="w", padx=15, pady=(2, 10))

# Fila 2: Departamento y Contraseña del donante
ttk.Label(form_frame, text="Departamento *").grid(row=3, column=0, sticky="w", padx=15)
label_contrasena = ttk.Label(form_frame, text="Contraseña del donante *")
label_contrasena.grid(row=3, column=1, sticky="w", padx=15)

combo_departamento = ttk.Combobox(form_frame, width=39, state="readonly", values=DEPARTAMENTOS)
combo_departamento.grid(row=4, column=0, sticky="w", padx=15, pady=(2, 10))

entry_contrasena = ttk.Entry(form_frame, width=42, show="*")
entry_contrasena.grid(row=4, column=1, sticky="w", padx=15, pady=(2, 10))

# Fila 3: Botones
btn_frame = tk.Frame(form_frame, bg="#ffffff")
btn_frame.grid(row=5, column=1, sticky="e", padx=15, pady=(5, 15))

btn_cancelar = tk.Button(
    btn_frame, text="Cancelar", bg="#e2e6ea", fg="#333333",
    relief="flat", padx=12, pady=4, command=lambda: limpiar_formulario()
)
btn_cancelar.pack(side="left", padx=5)
btn_guardar = tk.Button(
    btn_frame, text="Guardar Datos", bg="#28a745", fg="white",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=4,
    command=lambda: guardar_desde_formulario()
)
btn_guardar.pack(side="left")

# ==========================================
# SECCIÓN 2: DIRECTORIO DE DONANTES (TABLA)
# ==========================================
table_frame = tk.Frame(root, bg="#ffffff", highlightbackground="#dcdcdc", highlightthickness=1)
table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

ttk.Label(table_frame, text="DIRECTORIO DE DONANTES", style="Section.TLabel").pack(anchor="w", padx=15, pady=(12, 8))

filter_frame = tk.Frame(table_frame, bg="#ffffff")
filter_frame.pack(fill="x", padx=15, pady=(0, 10))

ttk.Label(filter_frame, text="Buscar (ID, Nombre, Email, Departamento):").pack(side="left")
entrada_busqueda = ttk.Entry(filter_frame, width=28)
entrada_busqueda.pack(side="left", padx=(5, 12))

tk.Button(
    filter_frame, text="Actualizar", bg="#e2e6ea", relief="flat", padx=10,
    command=lambda: cargar_donantes()
).pack(side="right", padx=(5, 0))

btn_eliminar = tk.Button(
    filter_frame, text="Eliminar Seleccionado", bg="#dc3545", fg="white",
    font=("Segoe UI", 9, "bold"), relief="flat", padx=10,
    command=lambda: eliminar_desde_tabla()
)
btn_eliminar.pack(side="right")

columnas = ("id_donante", "nombre", "email", "departamento")
tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", height=6)

tabla.heading("id_donante", text="ID")
tabla.heading("nombre", text="Nombre")
tabla.heading("email", text="Email")
tabla.heading("departamento", text="Departamento")

tabla.column("id_donante", width=70, anchor="center")
tabla.column("nombre", width=230)
tabla.column("email", width=250)
tabla.column("departamento", width=180)

tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))


def mostrar_error(error):
    messagebox.showerror("Error de base de datos", str(error), parent=root)


def cargar_donantes():
    global donantes
    try:
        donantes = listar_donantes()
    except (ConnectionError, Error, ValueError) as error:
        mostrar_error(error)
        return
    mostrar_donantes()


def mostrar_donantes():
    busqueda = entrada_busqueda.get().strip().casefold()
    for item in tabla.get_children():
        tabla.delete(item)
    for donante in donantes:
        id_donante, nombre, email, departamento = donante
        valores_busqueda = (id_donante, nombre, email, departamento or "")
        if busqueda and not any(busqueda in str(valor).casefold() for valor in valores_busqueda):
            continue
        tabla.insert(
            "", "end",
            values=(id_donante, nombre, email, departamento or ""),
        )


def seleccionar_donante():
    global donante_seleccionado
    seleccion = tabla.selection()
    if not seleccion:
        return
    valores = tabla.item(seleccion[0], "values")
    donante_seleccionado = int(valores[0])
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, valores[1])
    entry_email.delete(0, tk.END)
    entry_email.insert(0, valores[2])
    combo_departamento.set(valores[3])
    entry_contrasena.delete(0, tk.END)
    titulo_formulario.config(text="EDITAR DONANTE")
    label_contrasena.config(text="Nueva contraseña (Opcional)")
    btn_guardar.config(text="Guardar Cambios")


def cambiar_filtros(event):
    if event.widget is entrada_busqueda:
        mostrar_donantes()


def cambiar_seleccion(event):
    if event.widget is tabla:
        seleccionar_donante()


entrada_busqueda.bind("<KeyRelease>", cambiar_filtros)
tabla.bind("<<TreeviewSelect>>", cambiar_seleccion)


def limpiar_formulario():
    global donante_seleccionado
    donante_seleccionado = None
    entry_nombre.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)
    combo_departamento.set("")
    tabla.selection_remove(*tabla.selection())
    titulo_formulario.config(text="REGISTRAR DONANTE")
    label_contrasena.config(text="Contraseña del donante *")
    btn_guardar.config(text="Guardar Datos")


def guardar_desde_formulario():
    nombre = entry_nombre.get().strip()
    email = entry_email.get().strip()
    departamento = combo_departamento.get().strip()
    contrasena = entry_contrasena.get().strip()

    if not nombre or not email or not departamento:
        messagebox.showwarning(
            "Datos incompletos",
            "Completa el nombre, el correo y selecciona un departamento.",
            parent=root,
        )
        return

    if donante_seleccionado is None and not contrasena:
        messagebox.showwarning(
            "Datos incompletos",
            "Ingresa una contraseña para el nuevo donante.",
            parent=root,
        )
        return

    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
        messagebox.showerror(
            "Error de registro",
            "El nombre no puede contener números ni símbolos.",
            parent=root,
        )
        return

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        messagebox.showwarning(
            "Correo inválido",
            "Ingresa un correo electrónico válido.",
            parent=root,
        )
        return

    try:
        guardar_donante(nombre, email, departamento, contrasena, donante_seleccionado)
    except (ConnectionError, Error, ValueError) as error:
        mostrar_error(error)
        return

    limpiar_formulario()
    cargar_donantes()
    messagebox.showinfo("Guardado", "Los datos del donante se guardaron.", parent=root)


def eliminar_desde_tabla():
    if donante_seleccionado is None:
        messagebox.showwarning(
            "Sin selección",
            "Selecciona un donante de la tabla para eliminarlo.",
            parent=root,
        )
        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Estás seguro de que deseas eliminar este donante?",
        parent=root,
    )
    if not confirmar:
        return

    try:
        eliminar_donante(donante_seleccionado)
    except (ConnectionError, Error, ValueError) as error:
        mostrar_error(error)
        return

    limpiar_formulario()
    cargar_donantes()
    messagebox.showinfo("Eliminado", "El donante fue eliminado correctamente.", parent=root)

cargar_donantes()
root.mainloop()
