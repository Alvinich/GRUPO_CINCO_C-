import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from mysql.connector import Error

from conexion1 import (
    guardar_reporte,
    listar_donantes,
    listar_donantes_por_programa,
    listar_programas,
    listar_reportes_donante,
    obtener_resumen_donante,
)

AZUL = "#00A0D6"
AZUL_OSCURO = "#0B4F6C"
VERDE = "#2E9E6B"
ROSADO = "#F8C8DC"
FONDO = "#F7F9FC"
BLANCO = "white"


def calcular_matrices(filas_donantes, pagos_donante):
    # 1. Matriz trimestral: cada fila es un donante (Mes 1, Mes 2, Mes 3)
    matriz = []
    etiquetas = []
    activos = pausados = cancelados = 0

    for did, nombre, depto, aldea, monto, freq, estado in filas_donantes:
        m = float(monto)
        etiquetas.append((did, nombre, depto, aldea, m, freq, estado))
        if estado == "activo":
            activos += 1
            fila = (m, 0.0, 0.0) if freq == "unico" else (m, m, m)
        elif estado == "pausado":
            pausados += 1
            fila = (m, 0.0, 0.0)
        else:
            cancelados += 1
            fila = (0.0, 0.0, 0.0)
        matriz.append(fila)

    tot_filas = tuple(round(sum(f), 2) for f in matriz)
    if matriz:
        m1 = round(sum(f[0] for f in matriz), 2)
        m2 = round(sum(f[1] for f in matriz), 2)
        m3 = round(sum(f[2] for f in matriz), 2)
    else:
        m1 = m2 = m3 = 0.0
    tot_trimestre = round(m1 + m2 + m3, 2)

    # 2. Distribución del gasto (50% Alimentación, 30% Educación, 20% Salud)
    gasto_alim = round(m1 * 0.50, 2)
    gasto_educ = round(m1 * 0.30, 2)
    gasto_salu = round(m1 * 0.20, 2)

    # 3. Cadena de Márkov (proyección a 1 y 6 meses)
    total_p = len(filas_donantes)
    if total_p > 0:
        v_act = round(activos * 100 / total_p, 2)
        v_pau = round(pausados * 100 / total_p, 2)
        v_can = round(cancelados * 100 / total_p, 2)
    else:
        v_act, v_pau, v_can = 0.0, 0.0, 100.0

    a, p, c = v_act, v_pau, v_can
    m1_markov = (a, p, c)
    for mes in range(1, 7):
        na = round(a * 0.85 + p * 0.30, 2)
        np = round(a * 0.10 + p * 0.50, 2)
        nc = round(a * 0.05 + p * 0.20 + c * 1.00, 2)
        a, p, c = na, np, nc
        if mes == 1:
            m1_markov = (a, p, c)
    m6_markov = (a, p, c)

    # 4. Conciliación (Comprometido mensual vs Pagos exitosos)
    pagado = round(sum(float(pm) for _, _, pm, _, est in pagos_donante if est == "exitoso"), 2)
    diferencia = round(m1 - pagado, 2)

    return {
        "etiquetas": etiquetas,
        "matriz": matriz,
        "tot_filas": tot_filas,
        "tot_meses": (m1, m2, m3),
        "tot_trimestre": tot_trimestre,
        "gastos": (gasto_alim, gasto_educ, gasto_salu),
        "conteo": (activos, pausados, cancelados),
        "v_inicial": (v_act, v_pau, v_can),
        "m1_markov": m1_markov,
        "m6_markov": m6_markov,
        "pagado": pagado,
        "diferencia": diferencia,
    }


def abrir(padre, id_donante=None):
    if id_donante is None or not str(id_donante).isdigit():
        messagebox.showwarning("Aviso", "Registra o selecciona un donante primero.", parent=padre)
        return

    id_donante = int(id_donante)

    try:
        donantes = listar_donantes("")
        programas_db = listar_programas()
        compromisos_don, pagos_don = obtener_resumen_donante(id_donante)
        historial = listar_reportes_donante(id_donante)
    except Error as err:
        messagebox.showerror("Error BD", str(err), parent=padre)
        return

    donante_actual = next(((i, n, e, d) for i, n, e, d in donantes if i == id_donante), None)
    if not donante_actual:
        messagebox.showerror("Error", "Donante no encontrado en la base de datos.", parent=padre)
        return

    _, nom_don, mail_don, dep_don = donante_actual

    win = tk.Toplevel(padre)
    win.title(f"Reportes - {nom_don} (ID #{id_donante})")
    win.geometry("1060x640")
    win.configure(bg=FONDO)

    top = tk.Frame(win, bg=AZUL_OSCURO, height=55)
    top.pack(fill="x")
    tk.Label(top, text="ALDEAS INFANTILES SOS  •  SISTEMA DE REPORTES", bg=AZUL_OSCURO,
             fg=BLANCO, font=("Arial", 12, "bold")).pack(side="left", padx=20, pady=14)
    tk.Label(top, text=f"Donante verificado: {nom_don} (#{id_donante})", bg=AZUL_OSCURO,
             fg=ROSADO, font=("Arial", 10, "bold")).pack(side="right", padx=20)

    izq = tk.Frame(win, bg=BLANCO, width=385)
    izq.pack(side="left", fill="y", padx=15, pady=15)
    izq.pack_propagate(False)

    tk.Label(izq, text="📄 Nuevo Reporte", bg=BLANCO, font=("Arial", 15, "bold")).pack(anchor="w", padx=15, pady=(12, 2))
    tk.Label(izq, text="Selecciona una aldea para calcular sus matrices", bg=BLANCO, fg="#666666", font=("Arial", 9)).pack(anchor="w", padx=15)

    card = tk.Frame(izq, bg="#F0F8FF", highlightbackground=AZUL, highlightthickness=1)
    card.pack(fill="x", padx=15, pady=10, ipady=5, ipadx=8)
    tk.Label(card, text=f"ID Donante: #{id_donante} | Depto: {dep_don}", bg="#F0F8FF", fg=AZUL_OSCURO, font=("Arial", 9, "bold")).pack(anchor="w", padx=5)
    tk.Label(card, text=f"Nombre: {nom_don}", bg="#F0F8FF", font=("Arial", 9)).pack(anchor="w", padx=5)
    tk.Label(card, text=f"Correo: {mail_don}", bg="#F0F8FF", fg="#444444", font=("Arial", 8)).pack(anchor="w", padx=5)

    opciones_prog = [f"{pid} - {nom} - Aldea {ald or 'sin aldea'}" for pid, nom, ald in programas_db]
    tk.Label(izq, text="Programa / Aldea (4 opciones):", bg=BLANCO, font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(6, 2))
    combo_prog = ttk.Combobox(izq, values=opciones_prog, state="readonly", width=38)
    combo_prog.pack(padx=15, fill="x")
    if opciones_prog:
        combo_prog.current(0)

    if compromisos_don:
        _, pid_reciente, *_ = next(iter(compromisos_don))
        for idx, txt in enumerate(opciones_prog):
            if txt.startswith(f"{pid_reciente} - "):
                combo_prog.current(idx)
                break

    hoy = date.today()
    tk.Label(izq, text="Fecha:", bg=BLANCO, font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
    ent_fecha = tk.Entry(izq, font=("Arial", 10), bg="#f0f0f0")
    ent_fecha.insert(0, hoy.strftime("%d/%m/%Y"))
    ent_fecha.config(state="readonly")
    ent_fecha.pack(padx=15, fill="x", ipady=3)

    tk.Label(izq, text="Observaciones:", bg=BLANCO, font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
    txt_obs = tk.Text(izq, height=4, font=("Arial", 10))
    txt_obs.pack(padx=15, fill="x")
    txt_obs.insert("1.0", f"Reporte matricial generado por {nom_don}.")

    der = tk.Frame(win, bg=FONDO)
    der.pack(side="right", fill="both", expand=True, padx=15, pady=15)
    tk.Label(der, text="📊 Resultado del Informe Matemático", bg=FONDO, font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(der, text="Donantes por aldea, matriz trimestral, gastos, Márkov y conciliación.", bg=FONDO, fg="#666666", font=("Arial", 9)).pack(anchor="w", pady=(0, 8))

    salida = tk.Text(der, font=("Consolas", 10), bg=BLANCO)
    salida.pack(fill="both", expand=True)

    def actualizar(guardar=False):
        nonlocal historial
        sel = combo_prog.get()
        if not sel:
            return
        id_prog = int(sel.split(" - ")[0])
        nota = txt_obs.get("1.0", tk.END).strip()

        try:
            filas_aldea = listar_donantes_por_programa(id_prog)
            res = calcular_matrices(filas_aldea, pagos_don)
        except Exception as exc:
            salida.delete("1.0", tk.END)
            salida.insert("1.0", f"Error al calcular: {exc}")
            return

        lineas = [
            "===================================================================",
            f"FECHA: {ent_fecha.get()}  |  {sel}",
            "===================================================================",
            "",
            f"1. DONANTES EN ESTA ALDEA ({len(res['etiquetas'])}):",
        ]

        if res["etiquetas"]:
            for did, nombre, depto, aldea, monto, freq, estado in res["etiquetas"]:
                lineas.append(f"  • {nombre} (ID #{did} | {depto}) -> Aldea {aldea} | Bs. {monto:.2f} ({freq}) [{estado.upper()}]")
        else:
            lineas.append("  • Ningún donante registrado todavía en esta aldea.")

        lineas.extend([
            "",
            "2. MATRIZ DE APORTES TRIMESTRALES (Bs.):",
            "  Donante          Mes 1      Mes 2      Mes 3      Total",
            "  -----------------------------------------------------------",
        ])

        if res["matriz"]:
            for (did, nombre, *_), (f1, f2, f3), tf in zip(res["etiquetas"], res["matriz"], res["tot_filas"]):
                etiq = f"#{did} {nombre[:11]:<11}"
                lineas.append(f"  {etiq}  {f1:8.2f}   {f2:8.2f}   {f3:8.2f}   Bs. {tf:8.2f}")
            m1, m2, m3 = res["tot_meses"]
            lineas.append("  -----------------------------------------------------------")
            lineas.append(f"  TOTAL MES      {m1:8.2f}   {m2:8.2f}   {m3:8.2f}   Bs. {res['tot_trimestre']:8.2f}")
        else:
            lineas.append("  (Sin aportes registrados en esta aldea)")

        m1 = res["tot_meses"][0]
        ga, ge, gs = res["gastos"]
        ca, cp, cc = res["conteo"]
        va, vp, vc = res["v_inicial"]
        m1a, m1p, m1c = res["m1_markov"]
        m6a, m6p, m6c = res["m6_markov"]
        estado_conc = "CUADRADO" if res["diferencia"] == 0 else "PENDIENTE DE COBRO"

        lineas.extend([
            "",
            f"3. DISTRIBUCIÓN DEL GASTO SOCIAL (Base Mes 1 = Bs. {m1:.2f}):",
            f"  • Alimentación (50%): Bs. {ga:.2f}",
            f"  • Educación    (30%): Bs. {ge:.2f}",
            f"  • Salud        (20%): Bs. {gs:.2f}",
            "",
            "4. PROYECCIÓN DE RETENCIÓN (CADENA DE MÁRKOV):",
            f"  • Conteo real -> Activos: {ca} | Pausados: {cp} | Cancelados: {cc}",
            f"  • Inicial     -> Activos: {va:.1f}% | Pausados: {vp:.1f}% | Cancelados: {vc:.1f}%",
                        f"  • Mes 1       -> Activos: {m1a:.1f}% | Pausados: {m1p:.1f}% | Cancelados: {m1c:.1f}%",
            f"  • Mes 6       -> Activos: {m6a:.1f}% | Pausados: {m6p:.1f}% | Cancelados: {m6c:.1f}%",
            "",
            "5. CONCILIACIÓN DE MATRICES (A - B):",
            f"  • Comprometido mensual (A): Bs. {m1:.2f}",
            f"  • Pagos exitosos       (B): Bs. {res['pagado']:.2f}",
            f"  • Diferencia (A - B):       Bs. {res['diferencia']:.2f} ({estado_conc})",
            "",
            f"OBSERVACIONES: {nota}",
        ])

        texto_final = "\n".join(lineas)

        if guardar:
            try:
                id_rep = guardar_reporte(id_prog, id_donante, hoy.strftime("%Y-%m-%d"), texto_final)
                historial = listar_reportes_donante(id_donante)
                messagebox.showinfo("Guardado", f"Reporte #{id_rep} guardado en MySQL.", parent=win)
            except Error as err:
                messagebox.showerror("Error BD", str(err), parent=win)

        if historial:
            texto_final += "\n\nHISTORIAL DE REPORTES GUARDADOS:\n"
            for rid, rprog, rfec, _ in historial[:5]:
                texto_final += f"  • Reporte #{rid} | {rfec} | {rprog}\n"

        salida.delete("1.0", tk.END)
        salida.insert("1.0", texto_final)

    combo_prog.bind("<<ComboboxSelected>>", lambda _e: actualizar(False))

    tk.Button(izq, text="📊 GUARDAR REPORTE EN BD", bg=VERDE, fg=BLANCO,
              font=("Arial", 10, "bold"), pady=10, command=lambda: actualizar(True)).pack(fill="x", padx=15, pady=(12, 6))
    tk.Button(izq, text="Recalcular", bg=FONDO, font=("Arial", 9),
              command=lambda: actualizar(False)).pack(fill="x", padx=15)

    actualizar(False)
