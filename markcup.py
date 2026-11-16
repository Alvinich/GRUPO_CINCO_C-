import tkinter as tk
from tkinter import ttk

# Configuración de la ventana principal
root = tk.Tk()
root.title("Mockup - Gestión de Programas")
root.geometry("980x540")
root.configure(bg="#f4f6f9")

# Estilos generales
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", foreground="#333333", rowheight=32, fieldbackground="white", font=("Segoe UI", 10))
style.configure("Treeview.Heading", background="#f8fafc", foreground="#475569", font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[("selected", "#e0f2fe")], foreground=[("selected", "#0369a1")])

# Contenedor principal
container = tk.Frame(root, bg="#f4f6f9")
container.pack(fill="both", expand=True, padx=30, pady=25)

# --- ENCABEZADO ---
header = tk.Frame(container, bg="#f4f6f9")
header.pack(fill="x", pady=(0, 20))

lbl_titulo = tk.Label(header, text="Administración de Programas", font=("Segoe UI", 18, "bold"), bg="#f4f6f9", fg="#1e293b")
lbl_titulo.pack(side="left")

btn_nuevo = tk.Button(header, text="+ Nuevo Programa", bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=14, pady=8, cursor="hand2")
btn_nuevo.pack(side="right")

# --- GRID PRINCIPAL (2 COLUMNAS) ---
grid_frame = tk.Frame(container, bg="#f4f6f9")
grid_frame.pack(fill="both", expand=True)
grid_frame.columnconfigure(0, weight=1)
grid_frame.columnconfigure(1, weight=2)

# ================= COLUMNA 1: FORMULARIO =================
card_form = tk.Frame(grid_frame, bg="white", padx=20, pady=20, highlightbackground="#e2e8f0", highlightthickness=1)
card_form.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

tk.Label(card_form, text="Datos del Programa", font=("Segoe UI", 13, "bold"), bg="white", fg="#333333").pack(anchor="w")
ttk.Separator(card_form, orient="horizontal").pack(fill="x", pady=(8, 15))

# Campo: ID Programa
tk.Label(card_form, text="ID Programa", font=("Segoe UI", 10, "bold"), bg="white", fg="#333333").pack(anchor="w")
entry_id = tk.Entry(card_form, font=("Segoe UI", 10), bg="#f1f5f9", fg="#64748b", relief="solid", bd=1, state="disabled")
entry_id.pack(fill="x", ipady=5, pady=(4, 14))

# Campo: Nombre del Programa *
lbl_nombre_frame = tk.Frame(card_form, bg="white")
lbl_nombre_frame.pack(anchor="w")
tk.Label(lbl_nombre_frame, text="Nombre del Programa ", font=("Segoe UI", 10, "bold"), bg="white", fg="#333333").pack(side="left")
tk.Label(lbl_nombre_frame, text="*", font=("Segoe UI", 10, "bold"), bg="white", fg="#dc2626").pack(side="left")

entry_nombre = tk.Entry(card_form, font=("Segoe UI", 10), relief="solid", bd=1)
entry_nombre.pack(fill="x", ipady=5, pady=(4, 2))
tk.Label(card_form, text="Máximo 100 caracteres (Obligatorio).", font=("Segoe UI", 8), bg="white", fg="#64748b").pack(anchor="w", pady=(0, 14))

# Campo: Aldea
tk.Label(card_form, text="Aldea", font=("Segoe UI", 10, "bold"), bg="white", fg="#333333").pack(anchor="w")
entry_aldea = tk.Entry(card_form, font=("Segoe UI", 10), relief="solid", bd=1)
entry_aldea.pack(fill="x", ipady=5, pady=(4, 2))
tk.Label(card_form, text="Máximo 100 caracteres (Opcional).", font=("Segoe UI", 8), bg="white", fg="#64748b").pack(anchor="w", pady=(0, 20))

# Botones del Formulario
btn_frame = tk.Frame(card_form, bg="white")
btn_frame.pack(fill="x", pady=(5, 0))

btn_guardar = tk.Button(btn_frame, text="Guardar", bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"), bd=0, pady=8, cursor="hand2")
btn_guardar.pack(side="left", fill="x", expand=True, padx=(0, 8))

btn_limpiar = tk.Button(btn_frame, text="Limpiar", bg="#e2e8f0", fg="#475569", font=("Segoe UI", 10, "bold"), bd=0, padx=16, pady=8, cursor="hand2")
btn_limpiar.pack(side="right")

# ================= COLUMNA 2: LISTADO =================
card_list = tk.Frame(grid_frame, bg="white", padx=20, pady=20, highlightbackground="#e2e8f0", highlightthickness=1)
card_list.grid(row=0, column=1, sticky="nsew")

tk.Label(card_list, text="Programas Registrados", font=("Segoe UI", 13, "bold"), bg="white", fg="#333333").pack(anchor="w")
ttk.Separator(card_list, orient="horizontal").pack(fill="x", pady=(8, 15))

# Barra de búsqueda vacía
search_entry = tk.Entry(card_list, font=("Segoe UI", 10), fg="#333333", relief="solid", bd=1)
search_entry.pack(fill="x", ipady=5, pady=(0, 15))

# Tabla de registros vacía
columns = ("id", "nombre", "aldea", "acciones")
tree = ttk.Treeview(card_list, columns=columns, show="headings", height=8)

tree.heading("id", text="ID", anchor="w")
tree.heading("nombre", text="Nombre", anchor="w")
tree.heading("aldea", text="Aldea", anchor="w")
tree.heading("acciones", text="Acciones", anchor="center")

tree.column("id", width=55, anchor="w")
tree.column("nombre", width=200, anchor="w")
tree.column("aldea", width=165, anchor="w")
tree.column("acciones", width=85, anchor="center")

tree.pack(fill="both", expand=True)

root.mainloop()
