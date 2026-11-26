#librerias para conectar a la base de datos  
# Librerías para conectar a la base de datos
import hashlib
import mysql.connector

def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jossdann945",
        database="donaciones",
        port=3306,
        use_pure=True,
    )
    if not conexion.is_connected():
        conexion.close()
        raise ConnectionError("MySQL no estableció la conexión.")
    return conexion

def listar_donantes(busqueda=""):
    condiciones = []
    parametros = []
    if busqueda:
        condiciones.append(
            "(id_donante LIKE %s OR nombre LIKE %s OR email LIKE %s OR departamento LIKE %s)"
        )
        patron = f"%{busqueda}%"
        parametros.extend((patron, patron, patron, patron))

    consulta = "SELECT id_donante, nombre, email, departamento FROM donante"
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


def guardar_donante(nombre, email, departamento, contrasena=None, id_donante=None):
    conexion = conectar()
    cursor = None
    try:
        cursor = conexion.cursor()
        if id_donante is None:
            clave_hash = encriptar_contrasena(contrasena)
            cursor.execute(
                "INSERT INTO donante (nombre, email, departamento, contraseña) "
                "VALUES (%s, %s, %s, %s)",
                (nombre, email, departamento, clave_hash),
            )
        else:
            if contrasena:
                clave_hash = encriptar_contrasena(contrasena)
                cursor.execute(
                    "UPDATE donante SET nombre = %s, email = %s, departamento = %s, "
                    "contraseña = %s WHERE id_donante = %s",
                    (nombre, email, departamento, clave_hash, id_donante),
                )
            else:
                cursor.execute(
                    "UPDATE donante SET nombre = %s, email = %s, departamento = %s "
                    "WHERE id_donante = %s",
                    (nombre, email, departamento, id_donante),
                )
        conexion.commit()
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()

def eliminar_donante(id_donante):
    conexion = conectar()
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM donante WHERE id_donante = %s",
            (id_donante,),
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
