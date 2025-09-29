# Casino Vicario

Un sistema de escritorio para la gestión de un casino, incluyendo registro de usuarios, juegos, apuestas y transacciones.

## Características

-   Registro e Inicio de Sesión de Usuarios.
-   Gestión de Perfil de Usuario con imagen.
-   Dashboard con información del usuario.
-   Juego de Máquina Tragamonedas (Slot Machine).
-   Registro y visualización de Apuestas y Transacciones.
-   Temas personalizables (Claro y Oscuro).

## Prerrequisitos

-   Python 3.8 o superior.
-   `pip` (gestor de paquetes de Python).
-   Un servidor de base de datos MySQL.

## Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Vicario
```

### 2. Crear y Activar un Entorno Virtual

Es una buena práctica trabajar en un entorno virtual para aislar las dependencias del proyecto.

**En Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

Instala todas las librerías necesarias que se encuentran en el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos

El sistema utiliza una base de datos MySQL. Asegúrate de tener una base de datos creada. Por defecto, el sistema buscará una llamada `casino_vicario`.

### 5. Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto (en la misma carpeta que `Main.py`). Este archivo contendrá las credenciales para conectar a tu base de datos.

Añade el siguiente contenido al archivo `.env` y ajústalo con tus propias credenciales:

```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_de_mysql
DB_NAME=casino_vicario
```

**Nota:** Si tu usuario de MySQL no tiene contraseña, deja `DB_PASSWORD` vacío (`DB_PASSWORD=`).

## Cómo Ejecutar la Aplicación

Una vez que hayas completado todos los pasos de instalación y configuración, puedes iniciar la aplicación ejecutando el archivo `Main.py`.

```bash
python Main.py
```

Se abrirá la ventana principal de la aplicación y podrás empezar a interactuar con ella.

## Estructura del Proyecto

El proyecto sigue una arquitectura similar a Modelo-Vista-Controlador (MVC) para separar las responsabilidades:

-   `Main.py`: Punto de entrada de la aplicación.
-   `models/`: Contiene la lógica de negocio y la interacción con la base de datos.
-   `views/`: Contiene todas las clases que definen la interfaz gráfica de usuario (GUI).
-   `controllers/`: Actúa como intermediario entre los modelos y las vistas.
-   `assets/`: Almacena recursos estáticos como imágenes.
-   `requirements.txt`: Lista de dependencias de Python.
-   `.env`: Archivo de configuración para las credenciales (no incluido en el repositorio).
