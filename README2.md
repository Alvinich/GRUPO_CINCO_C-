# Gestión de donantes

## Conexión a MySQL

El proyecto usa MySQL Connector/Python y la base de datos `donantes`. Instala la dependencia con:

```powershell
python -m pip install -r requirements.txt
```

Configura la contraseña como variable de entorno en PowerShell; no la guardes en el código:

```powershell
$env:MYSQL_PASSWORD = "tu_contraseña_de_MySQL"
```

La conexión usa `localhost`, el usuario `root`, el puerto `3306` y la base `donantes` de forma predeterminada. Se pueden cambiar con `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PORT` y `MYSQL_DATABASE`.

Prueba la conexión ejecutando:

```powershell
python conexion.py
```

Para abrir la interfaz de donantes conectada a MySQL:

```powershell
python markcup1.py
```

La interfaz muestra los donantes existentes, permite buscarlos y filtrarlos, y deja crear o editar un registro seleccionándolo en la tabla. `markcup.py` sigue siendo un prototipo visual.
