import tkinter as tk
from tkinter import messagebox, ttk

from mysql.connector import Error

from conexion import guardar_donante, listar_donantes

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Donantes - Mockup")
root.geometry("820x540")
root.configure(bg="#f4f6f9")
root.resizable(False, False)

donantes = []
donante_seleccionado = None

# Estilos generales
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
style.configure("Header.TLabel", background="#f4f6f9", font=("Segoe UI", 14, "bold"))
style.configure("Section.TLabel", background="#ffffff", font=("Segoe UI", 11, "bold"), foreground="#333333")
style.configure("TRadiobutton", background="#ffffff", font=("Segoe UI", 10))
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
entry_nombre.grid(row=2, column=0, sticky="w", padx=15, pady=(2, 12))

entry_email = ttk.Entry(form_frame, width=42)
entry_email.grid(row=2, column=1, sticky="w", padx=15, pady=(2, 12))

# Fila 2: Tipo (ENUM) y País (NULL)
ttk.Label(form_frame, text="Tipo de donante *").grid(row=3, column=0, sticky="w", padx=15)
ttk.Label(form_frame, text="País (Opcional)").grid(row=3, column=1, sticky="w", padx=15)

radio_frame = tk.Frame(form_frame, bg="#ffffff")
radio_frame.grid(row=4, column=0, sticky="w", padx=15, pady=(2, 15))

tipo_var = tk.StringVar(value="")  # Sin selección inicial
ttk.Radiobutton(radio_frame, text="Local", variable=tipo_var, value="local").pack(side="left", padx=(0, 15))
ttk.Radiobutton(radio_frame, text="Internacional", variable=tipo_var, value="internacional").pack(side="left")

# Ahora permite escribir directamente
combo_pais = ttk.Combobox(form_frame, width=39)
combo_pais.grid(row=4, column=1, sticky="w", padx=15, pady=(2, 15))

# Botones de acción del formulario
btn_frame = tk.Frame(form_frame, bg="#ffffff")
btn_frame.grid(row=5, column=0, columnspan=2, sticky="e", padx=15, pady=(0, 15))

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

# Barra de búsqueda y filtro (vacíos)
filter_frame = tk.Frame(table_frame, bg="#ffffff")
filter_frame.pack(fill="x", padx=15, pady=(0, 10))

ttk.Label(filter_frame, text="Buscar:").pack(side="left")
entrada_busqueda = ttk.Entry(filter_frame, width=30)
entrada_busqueda.pack(side="left", padx=(5, 20))

ttk.Label(filter_frame, text="Filtrar por tipo:").pack(side="left")
filtro_tipo = ttk.Combobox(
    filter_frame, width=18, state="readonly",
    values=("Todos", "Local", "Internacional")
)
filtro_tipo.set("Todos")
filtro_tipo.pack(side="left", padx=5)
tk.Button(
    filter_frame, text="Actualizar", command=lambda: cargar_donantes()
).pack(side="right")

# Tabla vacía con las 5 columnas exactas de la base de datos
columnas = ("id_donante", "nombre", "email", "pais", "tipo")
tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", height=6)

tabla.heading("id_donante", text="ID")
tabla.heading("nombre", text="Nombre")
tabla.heading("email", text="Email")
tabla.heading("pais", text="País")
tabla.heading("tipo", text="Tipo")

tabla.column("id_donante", width=60, anchor="center")
tabla.column("nombre", width=200)
tabla.column("email", width=220)
tabla.column("pais", width=130)
tabla.column("tipo", width=130, anchor="center")

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
    tipo = filtro_tipo.get()
    tipo_filtro = tipo.casefold() if tipo != "Todos" else ""

    for item in tabla.get_children():
        tabla.delete(item)

    for donante in donantes:
        id_donante, nombre, email, pais, tipo_donante = donante
        valores_busqueda = (nombre, email, pais or "", tipo_donante)
        if busqueda and not any(busqueda in str(valor).casefold() for valor in valores_busqueda):
            continue
        if tipo_filtro and str(tipo_donante).casefold() != tipo_filtro:
            continue
        tabla.insert(
            "", "end",
            values=(id_donante, nombre, email, pais or "", tipo_donante),
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
    combo_pais.set(valores[3])
    tipo_var.set(valores[4])
    titulo_formulario.config(text="EDITAR DONANTE")
    btn_guardar.config(text="Guardar Cambios")


def cambiar_filtros(event):
    if event.widget in (entrada_busqueda, filtro_tipo):
        mostrar_donantes()


def cambiar_seleccion(event):
    if event.widget is tabla:
        seleccionar_donante()


entrada_busqueda.bind("<KeyRelease>", cambiar_filtros)
filtro_tipo.bind("<<ComboboxSelected>>", cambiar_filtros)
tabla.bind("<<TreeviewSelect>>", cambiar_seleccion)


def limpiar_formulario():
    global donante_seleccionado
    donante_seleccionado = None
    entry_nombre.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    combo_pais.set("")
    tipo_var.set("")
    tabla.selection_remove(*tabla.selection())
    titulo_formulario.config(text="REGISTRAR DONANTE")
    btn_guardar.config(text="Guardar Datos")


def guardar_desde_formulario():
    nombre = entry_nombre.get().strip()
    email = entry_email.get().strip()
    pais = combo_pais.get().strip() or None
    tipo = tipo_var.get()

    if not nombre or not email or not tipo:
        messagebox.showwarning(
            "Datos incompletos",
            "Completa el nombre, el correo y el tipo de donante.",
            parent=root,
        )
        return
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        messagebox.showwarning(
            "Correo inválido", "Ingresa un correo electrónico válido.", parent=root
        )
        return

    try:
        guardar_donante(nombre, email, pais, tipo, donante_seleccionado)
    except (ConnectionError, Error, ValueError) as error:
        mostrar_error(error)
        return

    limpiar_formulario()
    cargar_donantes()
    messagebox.showinfo("Guardado", "Los datos del donante se guardaron.", parent=root)

cargar_donantes()
root.mainloop()
