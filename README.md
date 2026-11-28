# Gestión de Donantes

Aplicación de escritorio hecha en **Python** para administrar donantes. Usa **Tkinter** para las ventanas y **MySQL** para guardar los datos.

## ¿Qué hace?

- **Registrar** donantes con nombre, correo, país y contraseña.
- **Ver** los donantes en una tabla.
- **Editar** un donante al seleccionarlo en la tabla.
- **Eliminar** el donante seleccionado, previa confirmación.
- **Buscar** por texto y **filtrar** por tipo (Local).

El **tipo de donante** se asigna automáticamente según la ciudad:

| País | Tipo |
|---|---|
| Bolivia | Local |
| Cualquier otro de la lista

## Archivos

| Archivo | Función |
|---|---|
| `main.py` | La interfaz: formulario, tabla, botones y validaciones. |
| `conexion.py` | La comunicación con MySQL: listar, guardar y eliminar donantes. |

## ¿Cómo funciona?

1. El usuario usa la ventana (`main.py`).
2. `main.py` llama a las funciones de `conexion.py`.
3. `conexion1.py` ejecuta la consulta en la base de datos `donaciones`.
4. La tabla de la ventana muestra los datos.

## Requisitos

- Python 3
- Servidor MySQL en ejecución (puerto 3306)
- Conector de MySQL para Python:

```bash
pip install mysql-connector-python
```

## Base de datos

La aplicación usa la base de datos `donaciones` y la tabla `donante`, con estos datos principales:

| Campo | Descripción |
|---|---|
| `id_donante` | Identificador del donante |
| `nombre` | Nombre completo |
| `email` | Correo electrónico |
| `ciudad` | ciudad |
| `tipo` | `local` |

La tabla también debe permitir guardar la contraseña, según lo definido en `conexion.py`.

## Cómo ejecutarlo

1. Inicia en el sistema.
2. Verifica que existan la base de datos y la tabla.
3. En `conexion.py`, coloca tu usuario y contraseña .
4. Ejecuta:

```bash
python main.py
```

## Cómo usarlo

| Acción | Pasos |
|---|---|
| Registrar | Llena el formulario y presiona **Guardar Datos**. |
| Editar | Selecciona un donante, cambia los datos y presiona **Guardar Cambios**. La nueva contraseña es opcional. |
| Eliminar | Selecciona un donante y presiona **Eliminar Seleccionado**. |
| Buscar | Escribe en el buscador o elige un tipo. |
| Limpiar formulario | Presiona **Cancelar** o **+ Nuevo Donante**. |
| Recargar la tabla | Presiona **Actualizar**. |
