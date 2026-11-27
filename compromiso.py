import tkinter as tk
from datetime import date, timedelta
from tkinter import messagebox, ttk

from mysql.connector import Error
from tkcalendar import DateEntry

from conexion1 import guardar_compromiso, listar_programas

AZUL = "#00A0D6"
AZUL_OSCURO = "#0084B4"
ROSADO = "#F8C8DC"
ROSADO_SUAVE = "#FDECF2"
BLANCO = "white"
GRIS_TEXTO = "#333333"
FONDO_TARJETA = "#F0F8FF"


def abrir(padre, id_donante=None, id_programa=None):
    ventana = tk.Toplevel(padre)
    ventana.title("Crea tu Compromiso - Aldeas Infantiles SOS")
    ventana.geometry("950x610")
    ventana.configure(bg=BLANCO)

    try:
        prog_id = int(id_programa) if id_programa is not None else 1
    except ValueError:
        prog_id = 1

    # Obtener desde la base de datos el nombre y aldea actualizados del programa elegido
    nombre_programa = f"Programa #{prog_id}"
    try:
        for pid, nom, ald in listar_programas():
            if pid == prog_id:
                nombre_programa = f"{nom} - Aldea {ald or 'sin aldea'}"
                break
    except Error:
        pass

    texto_donante = str(id_donante) if id_donante is not None else "No asignado"

    # ===== LADO IZQUIERDO - ROSADO =====
    izq = tk.Frame(ventana, bg=ROSADO, width=410)
    izq.pack(side="left", fill="both")
    izq.pack_propagate(False)

    tk.Label(izq, text="ALDEAS INFANTILES SOS", bg=AZUL, fg=BLANCO,
             font=("Arial", 11, "bold"), padx=12, pady=8).pack(anchor="w", padx=20, pady=(20, 0))
    tk.Label(izq, text="Tu compromiso cambia\nuna vida para siempre",
             bg=ROSADO, fg="#2B2B2B", font=("Arial", 19, "bold"),
             justify="left", wraplength=370).pack(anchor="w", padx=20, pady=(20, 10))
    tk.Label(izq, text="Con un compromiso mensual ayudas a que niñas y niños de Aldeas Infantiles SOS crezcan en una familia amorosa, con educación, salud y alimentación.",
             bg=ROSADO, fg=GRIS_TEXTO, font=("Arial", 10),
             justify="left", wraplength=370).pack(anchor="w", padx=20)

    tk.Label(izq, text="NUESTROS PROGRAMAS", bg=ROSADO, font=("Arial", 10, "bold"),
             fg=AZUL_OSCURO).pack(anchor="w", padx=20, pady=(20, 5))
    for p in (
        "🏠  Cuidado Alternativo - Aldea La Paz",
        "📚  Educación y Desarrollo - Aldea Cochabamba",
        "❤️  Salud y Nutrición - Aldea Santa Cruz",
        "👩‍👧  Fortalecimiento Familiar - Aldea Tarija",
    ):
        tk.Label(izq, text=p, bg=ROSADO_SUAVE, fg=GRIS_TEXTO, font=("Arial", 10),
                 anchor="w", padx=10, pady=5).pack(fill="x", padx=20, pady=2)

    tk.Label(izq, text="¿Necesitas ayuda?\nEscríbenos, te ayudamos a crear tu compromiso.",
             bg=AZUL, fg=BLANCO, font=("Arial", 10, "bold"),
             padx=15, pady=10, justify="left").pack(fill="x", padx=20, pady=20)

    # ===== LADO DERECHO - FORMULARIO =====
    der = tk.Frame(ventana, bg=BLANCO)
    der.pack(side="right", fill="both", expand=True, padx=25, pady=15)

    tk.Label(der, text="Crea tu compromiso de ayuda",
             bg=BLANCO, font=("Arial", 16, "bold")).pack(anchor="w")
    tk.Label(der, text="Revisa tu programa asignado y configura tu aporte.",
             bg=BLANCO, fg="#666666", font=("Arial", 10)).pack(anchor="w", pady=(2, 10))

    # --- TARJETA SUPERIOR FIJA (NO MODIFICABLE: PROGRAMA/ALDEA + ID DONANTE AL LADO) ---
    tarjeta_info = tk.Frame(der, bg=FONDO_TARJETA, highlightbackground=AZUL, highlightthickness=1)
    tarjeta_info.pack(fill="x", pady=(0, 12), ipady=6, ipadx=10)

    col_prog = tk.Frame(tarjeta_info, bg=FONDO_TARJETA)
    col_prog.pack(side="left", fill="x", expand=True, padx=10)
    tk.Label(col_prog, text="PROGRAMA Y ALDEA ELEGIDA:", bg=FONDO_TARJETA,
             fg=AZUL_OSCURO, font=("Arial", 8, "bold")).pack(anchor="w")
    tk.Label(col_prog, text=nombre_programa, bg=FONDO_TARJETA,
             fg=GRIS_TEXTO, font=("Arial", 11, "bold")).pack(anchor="w")

    col_id = tk.Frame(tarjeta_info, bg=FONDO_TARJETA)
    col_id.pack(side="right", padx=12)
    tk.Label(col_id, text="ID DONANTE:", bg=FONDO_TARJETA,
             fg=AZUL_OSCURO, font=("Arial", 8, "bold")).pack(anchor="e")
    tk.Label(col_id, text=f"# {texto_donante}", bg=FONDO_TARJETA,
             fg=GRIS_TEXTO, font=("Arial", 12, "bold")).pack(anchor="e")

    # 1. Montos con sintaxis (Bs. 100, etc.)
    monto_var = tk.StringVar(value="100")

    tk.Label(der, text="1. Elige tu monto:", bg=BLANCO,
             font=("Arial", 10, "bold")).pack(anchor="w")
    frame_montos = tk.Frame(der, bg=BLANCO)
    frame_montos.pack(fill="x", pady=4)

    def actualizar_otro():
        if monto_var.get() == "Otro":
            entry_otro.config(state="normal")
            entry_otro.focus()
        else:
            entry_otro.delete(0, tk.END)
            entry_otro.config(state="disabled")

    for monto, texto in (("100", "Bs. 100"), ("50", "Bs. 50"), ("30", "Bs. 30"), ("Otro", "Otro")):
        tk.Radiobutton(frame_montos, text=texto, variable=monto_var, value=monto,
                       bg=BLANCO, font=("Arial", 10, "bold"),
                       command=actualizar_otro).pack(side="left", padx=8)

    tk.Label(der, text="Otro monto en Bs. (si elegiste Otro):", bg=BLANCO,
             font=("Arial", 10)).pack(anchor="w", pady=(6, 2))
    entry_otro = tk.Entry(der, width=48, font=("Arial", 11), state="disabled")
    entry_otro.pack(fill="x", ipady=3)

    # 2. Frecuencia y 3. Estado en dos columnas
    fila_combos = tk.Frame(der, bg=BLANCO)
    fila_combos.pack(fill="x", pady=(10, 4))

    col_frec = tk.Frame(fila_combos, bg=BLANCO)
    col_frec.pack(side="left", fill="x", expand=True, padx=(0, 8))
    tk.Label(col_frec, text="2. Frecuencia:", bg=BLANCO, font=("Arial", 10, "bold")).pack(anchor="w")
    combo_frecuencia = ttk.Combobox(col_frec, values=["mensual", "unico", "anual"], state="readonly")
    combo_frecuencia.pack(fill="x", pady=(2, 0), ipady=2)
    combo_frecuencia.current(0)

    col_est = tk.Frame(fila_combos, bg=BLANCO)
    col_est.pack(side="right", fill="x", expand=True, padx=(8, 0))
    tk.Label(col_est, text="3. Estado:", bg=BLANCO, font=("Arial", 10, "bold")).pack(anchor="w")
    combo_estado = ttk.Combobox(col_est, values=["activo", "pausado", "cancelado"], state="readonly")
    combo_estado.pack(fill="x", pady=(2, 0), ipady=2)
    combo_estado.current(0)

    # 4. Calendario interactivo (solo fechas después de hoy y formato DD,MM,AAAA)
    tk.Label(der, text="4. Fecha de inicio (elije la fecha de hoy y posterior):",
             bg=BLANCO, font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 3))

    manana = date.today() + timedelta(days=1)
    cal_fecha = DateEntry(
        der,
        width=25,
        background=AZUL,
        foreground=BLANCO,
        headersbackground=AZUL_OSCURO,
        headersforeground=BLANCO,
        selectbackground=AZUL,
        borderwidth=2,
        year=manana.year,
        month=manana.month,
        day=manana.day,
        date_pattern="dd/mm/yyyy",
        font=("Arial", 11, "bold")
    )
    cal_fecha.config(mindate=manana)
    cal_fecha.set_date(manana)
    cal_fecha.bind("<Key>", lambda _event: "break")
    cal_fecha.pack(anchor="w", ipady=4)

    def crear_compromiso():
        if id_donante is None or not str(id_donante).isdigit():
            messagebox.showerror(
                "Error de sesión",
                "No se recibió un ID de donante válido desde el registro.",
                parent=ventana
            )
            return

        monto_texto = entry_otro.get().strip() if monto_var.get() == "Otro" else monto_var.get()

        if not monto_texto:
            messagebox.showwarning(
                "Falta monto",
                "Por favor ingresa un monto en Bs. para continuar.",
                parent=ventana
            )
            return

        try:
            monto = float(monto_texto)
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Monto inválido",
                "El monto debe ser un número válido mayor a Bs. 0.",
                parent=ventana
            )
            return

        fecha_seleccionada = cal_fecha.get_date()
        if fecha_seleccionada <= date.today():
            messagebox.showwarning(
                "Fecha inválida",
                "Debes seleccionar una fecha posterior a hoy.",
                parent=ventana
            )
            return

        fecha_sql = fecha_seleccionada.strftime("%Y-%m-%d")

        try:
            guardar_compromiso(
                int(id_donante),
                prog_id,
                monto,
                combo_frecuencia.get(),
                fecha_sql,
                combo_estado.get()
            )
        except Error as error:
            messagebox.showerror("Error de base de datos", str(error), parent=ventana)
            return

        messagebox.showinfo(
            "¡Compromiso creado!",
            f"Programa: {nombre_programa}\nMonto: Bs. {monto:.2f}\nFecha inicio: {cal_fecha.get()}",
            parent=ventana
        )
        ventana.destroy()

    tk.Button(der, text="¡CREAR MI COMPROMISO!", bg=AZUL, fg=BLANCO,
              font=("Arial", 12, "bold"), pady=10,
              command=crear_compromiso).pack(fill="x", pady=(18, 6))
    tk.Label(der, text="Puedes pausar o cancelar tu compromiso cuando quieras.",
             bg=BLANCO, fg="#999999", font=("Arial", 9)).pack()
