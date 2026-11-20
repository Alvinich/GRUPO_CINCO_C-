# Sistemas de Captación de Fondos y Gestión de Donantes: Aldeas Infantiles

En Aldeas Infantiles SOS, los sistemas de captación de fondos y gestión de donantes son el conjunto de estrategias, herramientas tecnológicas y procesos administrativos utilizados para obtener recursos económicos y mantener una relación sólida y transparente con quienes apoyan a la organización. 

Su objetivo principal es garantizar la autosostenibilidad financiera para proteger el derecho de niñas, niños y adolescentes a vivir en familia.

### 1. Requisitos previos

Asegúrese de tener instaladas las siguientes herramientas en su equipo:
* **Python 3.14.10 (marque la opción *"Add Python to PATH"* durante la instalación).
* **MySQL Server** y **MySQL Workbench** (marque la version 8.0) (puede instalarlos juntos mediante el *MySQL Installer for Windows*).
* **Git** (opcional, para clonar el repositorio).
---

| N° | Integrante | Rol en el Proyecto | Usuario de GitHub |
| :--- | :--- | :--- | :--- |
| 1 | Mejia Loayza Jose Daniel | Scrum Master, Developer | @JoseMejia24 |
| 2 | Mendoza Flores Grabiel Adalid | Product Owner, Developer | @RealAndres11 |
| 3 | Fabian Chuquimia Alvaro Marvin | Developer | @Alvinich |
| 4 | Cori Copa Cristian Josue | Líder de Documentación, Developer | @josuecoricopa |
<<<<<<< HEAD
| 5 | Alcoreza Mamani Pablo Sebastian | Snakero, Developer | @Sebas160710 |
=======
| 5 | Alcoreza Mamani Pablo Sebastian | Snikero, Developer | @Sebas160710 |
## Instalación paso a paso (Windows + MySQL Workbench + Python)

### 2. Descargar el proyecto

* **Opción A — con Git:**
  Ubíquese en la carpeta donde desea guardar sus proyectos y ejecute:
  ```bash
  git clone https://github.com/Alvinich/GRUPO_CINCO_C-.git
  ```

* **Opción B — sin Git:**
  En la página del repositorio presione **Code** → **Download ZIP**, descomprima el archivo.

La estructura principal debe quedar así:

```text
GRUPO_CINCO_C-\
├── base_de_datos\
├── BITACORA.md
├── README.md
├── conexión.py
└── main.py...
```
### 3. Iniciar MySQL e instalar dependencias de Python

1. Asegúrese de que el servicio de *MySQL* esté activo en su equipo y abra *MySQL Workbench* iniciando sesión en su conexión local (localhost, usuario root).
2. Abra una terminal (CMD o PowerShell) dentro de la carpeta del proyecto e instale las librerías necesarias de Python:
   bash
   pip install mysql-connector-python

### 4. Importar la base de datos

1. Abra *MySQL Workbench* y conéctese a su servidor local.
2. Cree una base de datos llamada "Donaciones" (o ejecute directamente el script si ya incluye la instrucción CREATE DATABASE).
3. En el menú superior haga clic en *Server* → *Data Import* (o *File* → *Open SQL Script...*).
4. Seleccione *Import from Self-Contained File* y elija el archivo .sql ubicado dentro de la carpeta:
   text
   GRUPO_CINCO_C-\base_de_datos\archivo_base_datos.sql
   
5. En *Default Target Schema, seleccione la base de datos creada y presione **Start Import* (o ejecute el script con el ícono del rayo ⚡). Debe aparecer el mensaje de confirmación sin errores y las tablas visibles en el panel izquierdo (*Schemas*).
Alternativa por consola:
bash
mysql -u root -p aldeas_infantiles < "ruta\de\tu\carpeta\GRUPO_CINCO_C-\base_de_datos\archivo_base_datos.sql"


### 5. Abrir el sistema

1. Verifique en el archivo *conexión.py* que el usuario, contraseña y nombre de la base de datos coincidan con su configuración de MySQL Workbench.
2. Ejecute el archivo principal desde la terminal:
   bash
   python main.py
   Esto abrirá la pantalla de inicio del sistema.
