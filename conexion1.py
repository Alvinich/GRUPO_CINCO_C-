import hashlib
import mysql.connector

def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jossdann945",
        database="donaciones",
        port=3306,
        use_pure=True,
    )

def ejecutar(consulta, parametros=(), traer_datos=False):
    """Abre la conexión, ejecuta la consulta y la cierra siempre."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        if traer_datos:
            return cursor.fetchall()
        conexion.commit()
    finally:
        conexion.close()

def listar_donantes(busqueda=""):
    patron = f"%{busqueda}%"
    return ejecutar(
        "SELECT id_donante, nombre, email, departamento FROM donante "
        "WHERE id_donante LIKE %s OR nombre LIKE %s "
        "OR email LIKE %s OR departamento LIKE %s "
        "ORDER BY id_donante DESC",
        (patron, patron, patron, patron),
        traer_datos=True,
    )

def guardar_donante(nombre, email, departamento, contrasena=None, id_donante=None):
    if id_donante is None:  # Nuevo donante
        ejecutar(
            "INSERT INTO donante (nombre, email, departamento, contrasena) "
            "VALUES (%s, %s, %s, %s)",
            (nombre, email, departamento, encriptar_contrasena(contrasena)),
        )
    elif contrasena:  # Editar y cambiar contraseña
        ejecutar(
            "UPDATE donante SET nombre = %s, email = %s, departamento = %s, "
            "contrasena = %s WHERE id_donante = %s",
            (nombre, email, departamento, encriptar_contrasena(contrasena), id_donante),
        )
    else:  # Editar sin cambiar contraseña
        ejecutar(
            "UPDATE donante SET nombre = %s, email = %s, departamento = %s "
            "WHERE id_donante = %s",
            (nombre, email, departamento, id_donante),
        )

def eliminar_donante(id_donante):
    ejecutar("DELETE FROM donante WHERE id_donante = %s", (id_donante,))
def listar_programas():
    return ejecutar(
        "SELECT id_programa, nombre, aldea FROM programa ORDER BY id_programa",
        traer_datos=True,
    )

def guardar_programa(nombre, aldea, id_programa=None):
    if id_programa is None:
        ejecutar(
            "INSERT INTO programa (nombre, aldea) VALUES (%s, %s)",
            (nombre, aldea),
        )
    else:
        ejecutar(
            "UPDATE programa SET nombre = %s, aldea = %s WHERE id_programa = %s",
            (nombre, aldea, id_programa),
        )

def eliminar_programa(id_programa):
    ejecutar("DELETE FROM programa WHERE id_programa = %s", (id_programa,))
def listar_compromisos_combo():
    return ejecutar(
        "SELECT c.id_compromiso, d.nombre, p.nombre, c.monto "
        "FROM compromiso c "
        "JOIN donante d ON d.id_donante = c.id_donante "
        "JOIN programa p ON p.id_programa = c.id_programa "
        "ORDER BY c.id_compromiso DESC",
        traer_datos=True,
    )

def listar_metodos():
    return ejecutar(
        "SELECT id_metodo, nombre FROM metodo_pago ORDER BY id_metodo",
        traer_datos=True,
    )

def listar_pagos():
    return ejecutar(
        "SELECT pa.id_pago, pa.id_compromiso, pa.id_metodo, m.nombre, pa.monto, "
        "pa.fecha, pa.estado, pa.conciliado, pa.referencia_pasarela "
        "FROM pago pa JOIN metodo_pago m ON m.id_metodo = pa.id_metodo "
        "ORDER BY pa.id_pago DESC",
        traer_datos=True,
    )

def guardar_pago(id_compromiso, id_metodo, monto, fecha, estado,
                 referencia, conciliado, id_pago=None):
    if id_pago is None:
        ejecutar(
            "INSERT INTO pago (id_compromiso, id_metodo, monto, fecha, estado, "
            "referencia_pasarela, conciliado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (id_compromiso, id_metodo, monto, fecha, estado, referencia, int(conciliado)),
        )
    else:
        ejecutar(
            "UPDATE pago SET id_compromiso = %s, id_metodo = %s, monto = %s, fecha = %s, "
            "estado = %s, referencia_pasarela = %s, conciliado = %s WHERE id_pago = %s",
            (id_compromiso, id_metodo, monto, fecha, estado, referencia,
             int(conciliado), id_pago),
        )

def eliminar_pago(id_pago):
    ejecutar("DELETE FROM pago WHERE id_pago = %s", (id_pago,))
# ---------- Compromisos ----------
def guardar_compromiso(id_donante, id_programa, monto, frecuencia, fecha_inicio, estado):
    ejecutar(
        "INSERT INTO compromiso (id_donante, id_programa, monto, frecuencia, fecha_inicio, estado) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (id_donante, id_programa, monto, frecuencia, fecha_inicio, estado),
    )


# ---------- Programas ----------
def listar_programas():
    return ejecutar(
        "SELECT id_programa, nombre, aldea FROM programa ORDER BY id_programa",
        traer_datos=True,
    )


def guardar_programa(nombre, aldea, id_programa=None):
    if id_programa is None:
        ejecutar(
            "INSERT INTO programa (nombre, aldea) VALUES (%s, %s)",
            (nombre, aldea),
        )
    else:
        ejecutar(
            "UPDATE programa SET nombre = %s, aldea = %s WHERE id_programa = %s",
            (nombre, aldea, id_programa),
        )


def eliminar_programa(id_programa):
    ejecutar("DELETE FROM programa WHERE id_programa = %s", (id_programa,))


# ---------- Pagos ----------
def listar_compromisos_combo():
    return ejecutar(
        "SELECT c.id_compromiso, d.nombre, p.nombre, c.monto "
        "FROM compromiso c "
        "JOIN donante d ON d.id_donante = c.id_donante "
        "JOIN programa p ON p.id_programa = c.id_programa "
        "ORDER BY c.id_compromiso DESC",
        traer_datos=True,
    )


def listar_metodos():
    return ejecutar(
        "SELECT id_metodo, nombre FROM metodo_pago ORDER BY id_metodo",
        traer_datos=True,
    )


def listar_pagos():
    return ejecutar(
        "SELECT pa.id_pago, pa.id_compromiso, pa.id_metodo, m.nombre, pa.monto, "
        "pa.fecha, pa.estado, pa.conciliado, pa.referencia_pasarela "
        "FROM pago pa JOIN metodo_pago m ON m.id_metodo = pa.id_metodo "
        "ORDER BY pa.id_pago DESC",
        traer_datos=True,
    )


def guardar_pago(id_compromiso, id_metodo, monto, fecha, estado,
                 referencia, conciliado, id_pago=None):
    if id_pago is None:
        ejecutar(
            "INSERT INTO pago (id_compromiso, id_metodo, monto, fecha, estado, "
            "referencia_pasarela, conciliado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (id_compromiso, id_metodo, monto, fecha, estado, referencia, int(conciliado)),
        )
    else:
        ejecutar(
            "UPDATE pago SET id_compromiso = %s, id_metodo = %s, monto = %s, fecha = %s, "
            "estado = %s, referencia_pasarela = %s, conciliado = %s WHERE id_pago = %s",
            (id_compromiso, id_metodo, monto, fecha, estado, referencia,
             int(conciliado), id_pago),
        )

def eliminar_pago(id_pago):
    ejecutar("DELETE FROM pago WHERE id_pago = %s", (id_pago,))
PROGRAMAS_INICIALES = (
    ("Cuidado Alternativo", "La Paz"),
    ("Educación y Desarrollo", "Cochabamba"),
    ("Salud y Nutrición", "Santa Cruz"),
    ("Fortalecimiento Familiar", "Tarija"),
)

def asegurar_programas():
    """Si la tabla programa está vacía, agrega los programas iniciales."""
    if not ejecutar("SELECT id_programa FROM programa LIMIT 1", traer_datos=True):
        for nombre, aldea in PROGRAMAS_INICIALES:
            ejecutar("INSERT INTO programa (nombre, aldea) VALUES (%s, %s)",
                     (nombre, aldea))
def guardar_reporte(id_programa, id_donante, fecha, contenido):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO reporte (id_programa, id_donante, fecha, contenido)
            VALUES (%s, %s, %s, %s)
            """,
            (id_programa, id_donante, fecha, contenido),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def listar_reportes_donante(id_donante):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT r.id_reporte, p.nombre, r.fecha, r.contenido
            FROM reporte r
            JOIN programa p ON r.id_programa = p.id_programa
            WHERE r.id_donante = %s
            ORDER BY r.id_reporte DESC
            """,
            (id_donante,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def listar_donantes_por_programa(id_programa):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT d.id_donante, d.nombre, d.departamento, p.aldea,
                   c.monto, c.frecuencia, c.estado
            FROM compromiso c
            JOIN donante d ON c.id_donante = d.id_donante
            JOIN programa p ON c.id_programa = p.id_programa
            WHERE c.id_programa = %s
            ORDER BY c.id_compromiso DESC
            """,
            (id_programa,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def obtener_resumen_donante(id_donante):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT c.id_compromiso, p.id_programa, p.nombre, p.aldea,
                   c.monto, c.frecuencia, c.estado
            FROM compromiso c
            JOIN programa p ON c.id_programa = p.id_programa
            WHERE c.id_donante = %s
            ORDER BY c.id_compromiso DESC
            """,
            (id_donante,),
        )
        compromisos = cursor.fetchall()

        cursor.execute(
            """
            SELECT pg.id_pago, pg.id_compromiso, pg.monto, pg.fecha, pg.estado
            FROM pago pg
            JOIN compromiso c ON pg.id_compromiso = c.id_compromiso
            WHERE c.id_donante = %s
            ORDER BY pg.fecha DESC
            """,
            (id_donante,),
        )
        pagos = cursor.fetchall()
        return compromisos, pagos
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    conectar().close()
    print("¡Conexión exitosa con MySQL!")