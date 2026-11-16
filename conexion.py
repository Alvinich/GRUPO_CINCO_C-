import os

import mysql.connector


def conectar():
    password = os.environ.get("MYSQL_PASSWORD")
    if password is None:
        raise ValueError("Configura la variable de entorno MYSQL_PASSWORD.")

    conexion = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=password,
        database=os.environ.get("MYSQL_DATABASE", "donantes"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        use_pure=True,
    )
    if not conexion.is_connected():
        conexion.close()
        raise ConnectionError("MySQL no estableció la conexión.")
    return conexion


def listar_donantes(busqueda="", tipo=""):
    condiciones = []
    parametros = []

    if busqueda:
        condiciones.append("(nombre LIKE %s OR email LIKE %s OR pais LIKE %s)")
        patron = f"%{busqueda}%"
        parametros.extend((patron, patron, patron))

    if tipo:
        condiciones.append("tipo = %s")
        parametros.append(tipo)

    consulta = (
        "SELECT id_donante, nombre, email, pais, tipo "
        "FROM donante"
    )
    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    consulta += " ORDER BY id_donante DESC"

    conexion = conectar()

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(consulta, tuple(parametros))
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def guardar_donante(nombre, email, pais, tipo, id_donante=None):
    conexion = conectar()

    cursor = None
    try:
        cursor = conexion.cursor()
        if id_donante is None:
            cursor.execute(
                "INSERT INTO donante (nombre, email, pais, tipo) "
                "VALUES (%s, %s, %s, %s)",
                (nombre, email, pais, tipo),
            )
        else:
            cursor.execute(
                "UPDATE donante SET nombre = %s, email = %s, pais = %s, "
                "tipo = %s WHERE id_donante = %s",
                (nombre, email, pais, tipo, id_donante),
            )
        conexion.commit()
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


if __name__ == "__main__":
    conexion = conectar()

    if conexion:
        print("¡Conexión exitosa con MySQL!")
        conexion.close()
        print("Conexión cerrada.")
