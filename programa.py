import tkinter as tk
from tkinter import messagebox, ttk

from mysql.connector import Error

import compromiso
from conexion1 import asegurar_programas, guardar_programa, listar_programas

AZUL = "#00A0D6"
AZUL_OSCURO = "#0084B4"
ROSADO = "#F8C8DC"
ROSADO_SUAVE = "#FDECF2"
BLANCO = "white"
GRIS_TEXTO = "#333333"

ALDEAS = (
    "Beni", "Chuquisaca", "Cochabamba", "La Paz", "Oruro",
    "Pando", "Potosi", "Santa Cruz", "Tarija",
)


def abrir(padre, id_donante=None):
    try:
        asegurar_programas()
        programas = listar_programas()
    except Error as error:
        messagebox.showerror("Error de base de datos", str(error), parent=padre)
        return

    ventana = tk.Toplevel(padre)
    ventana.title("Programas - Aldeas Infantiles SOS")
    ventana.geometry("950x600")
    ventana.configure(bg=BLANCO)

    # ===== LADO IZQUIERDO - ROSADO =====
    izq = tk.Frame(ventana, bg=ROSADO, width=430)
    izq.pack(side="left", fill="both")

    tk.Label(izq, text="ALDEAS INFANTILES SOS", bg=AZUL, fg=BLANCO,
             font=("Arial", 11, "bold"), padx=12, pady=8).pack(anchor="w", padx=20, pady=(20, 0))
    tk.Label(izq, text="Cada programa abre\nuna nueva oportunidad",
             bg=ROSADO, fg="#2B2B2B", font=("Arial", 20, "bold"),
             justify="left", wraplength=380).pack(anchor="w", padx=20, pady=(25, 10))
    tk.Label(izq, text="Estos son los programas que los donantes pueden apoyar con su compromiso, y la aldea donde se desarrollan.",
             bg=ROSADO, fg=GRIS_TEXTO, font=("Arial", 11),
             justify="left", wraplength=380).pack(anchor="w", padx=20)

    tk.Label(izq, text="¿QUÉ PROGRAMAS QUIERES AYUDAR CON TU COMPROMISO?", bg=ROSADO,
             font=("Arial", 10, "bold"), fg=AZUL_OSCURO).pack(anchor="w", padx=20, pady=(25, 5))

    lista_frame = tk.Frame(izq, bg=ROSADO)
    lista_frame.pack(fill="x")

    iconos = ("🏠", "📚", "❤️", "👩‍👧")

    def dibujar_lista():
        for widget in lista_frame.winfo_children():
            widget.destroy()
        for i, (_id, nombre, aldea) in enumerate(programas[:6]):
            tk.Label(lista_frame,
                     text=f"{iconos[i % 4]}  {nombre} - Aldea {aldea or 'sin aldea'}",
                     bg=ROSADO_SUAVE, fg=GRIS_TEXTO, font=("Arial", 10),
                     anchor="w", padx=10, pady=6).pack(fill="x", padx=20, pady=2)

    dibujar_lista()

    # ===== LADO DERECHO =====
    der = tk.Frame(ventana, bg=BLANCO)
    der.pack(side="right", fill="both", expand=True, padx=25, pady=20)

    tk.Label(der, text="Programas de las aldeas", bg=BLANCO,
             font=("Arial", 16, "bold")).pack(anchor="w")
    tk.Label(der, text="Elige un programa de la lista y la aldea donde se realiza. No se puede escribir, solo seleccionar.",
             bg=BLANCO, fg="#666666", font=("Arial", 10), wraplength=450,
             justify="left").pack(anchor="w", pady=(2, 10))

    # Mostrar ID Donante activo (solo lectura)
    if id_donante is not None:
        tk.Label(der, text=f"Donante activo: ID # {id_donante}", bg="#F0F8FF", fg=AZUL_OSCURO,
                 font=("Arial", 10, "bold"), padx=10, pady=5).pack(anchor="w", pady=(0, 10))

    def textos_programas():
        return [f"{i} - {n} - {a or 'sin aldea'}" for i, n, a in programas]

    tk.Label(der, text="1. Programa:", bg=BLANCO,
             font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
    combo_programa = ttk.Combobox(der, values=textos_programas(), state="readonly", width=45)
    combo_programa.pack(fill="x")

    tk.Label(der, text="2. Aldea donde se realiza:", bg=BLANCO,
             font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 2))
    combo_aldea = ttk.Combobox(der, values=ALDEAS, state="readonly", width=45)
    combo_aldea.pack(fill="x")

    def al_elegir_programa(_event=None):
        id_elegido = int(combo_programa.get().split(" - ")[0])
        for id_programa, _nombre, aldea in programas:
            if id_programa == id_elegido:
                combo_aldea.set(aldea or "")
                return

    combo_programa.bind("<<ComboboxSelected>>", al_elegir_programa)

    def guardar():
        nonlocal programas
        if not combo_programa.get() or not combo_aldea.get():
            messagebox.showwarning("Falta dato", "Elige un programa y una aldea.",
                                   parent=ventana)
            return
        id_elegido = int(combo_programa.get().split(" - ")[0])
        nombre = next(n for i, n, _a in programas if i == id_elegido)
        aldea_elegida = combo_aldea.get()
        try:
            guardar_programa(nombre, aldea_elegida, id_elegido)
            programas = listar_programas()
        except Error as error:
            messagebox.showerror("Error de base de datos", str(error), parent=ventana)
            return

        dibujar_lista()
        combo_programa.config(values=textos_programas())
        for texto in textos_programas():
            if texto.startswith(f"{id_elegido} - "):
                combo_programa.set(texto)

        messagebox.showinfo("Guardado", "Programa y aldea seleccionados. Continuando a Compromiso...",
                            parent=ventana)
        ventana.destroy()
        compromiso.abrir(padre, id_donante=id_donante, id_programa=id_elegido)

    tk.Button(der, text="GUARDAR Y CONTINUAR A COMPROMISO", bg=AZUL, fg=BLANCO,
              font=("Arial", 12, "bold"), pady=10,
              command=guardar).pack(fill="x", pady=25)
