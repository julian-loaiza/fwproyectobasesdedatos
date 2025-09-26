🚀 Aplicación de Gestión de Proyectos con Flask

Una aplicación web moderna desarrollada con Flask y Python para gestionar proyectos y docentes de manera eficiente. Permite realizar operaciones CRUD completas a través de una interfaz web intuitiva y responsiva.

🏗️ Arquitectura del Proyecto

El proyecto implementa una arquitectura cliente-servidor robusta:

🔧 Backend (Servidor): Construido con Flask, maneja toda la lógica de negocio y enrutamiento

🗄️ Base de Datos: PostgreSQL para almacenamiento persistente y confiable

🎨 Frontend (Cliente): Plantillas Jinja2 con Bootstrap 5 para diseño responsivo

⚙️ Configuración: Variables de entorno con archivo .env para máxima seguridad

📁 Estructura de Archivos
/tu_proyecto/
│
├── 📄 app.py              # Lógica principal de Flask
├── 📋 requirements.txt    # Dependencias de Python
├── 🔐 .env                # Configuración de BD
│
└── 📂 templates/
    ├── 🏠 layout.html     # Plantilla base
    ├── 🏡 index.html      # Página de inicio
    ├── 👨‍🏫 docentes.html   # Gestión de docentes
    └── 📊 proyectos.html  # Gestión de proyectos

📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:

🐍 Python 3.7+ y pip instalados

🐘 PostgreSQL servidor en ejecución

🚀 Guía de Instalación y Ejecución
1. 📥 Clonar el Proyecto
git clone <tu-repositorio>
cd tu_proyecto

2. 🔧 Crear Entorno Virtual
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# 🐧 macOS / Linux:
source venv/bin/activate
# 🪟 Windows:
.\venv\Scripts\activate

3. 📦 Instalar Dependencias
pip install -r requirements.txt


💡 Nota: Asegúrate de que requirements.txt contenga: Flask, psycopg2-binary, python-dotenv

4. 🗄️ Configurar la Base de Datos
a. Crear la Base de Datos:
CREATE DATABASE proyectos_informaticos;

b. Crear las Tablas:
-- 👨‍🏫 Tabla para los docentes
CREATE TABLE docente (
    codigo SERIAL PRIMARY KEY,
    documento VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    titulo VARCHAR(100),
    anosexperiencia INT
);

-- 📊 Tabla para los proyectos
CREATE TABLE proyecto (
    codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    aliado VARCHAR(100),
    descripcion TEXT,
    presupuesto NUMERIC(12, 2),
    horasestimadas INT,
    fechainicio DATE,
    fechafin DATE,
    docentejefe INT,
    CONSTRAINT fk_proyecto_docente
        FOREIGN KEY (docentejefe)
        REFERENCES docente(codigo)
        ON DELETE SET NULL
);

5. 🔐 Configurar Variables de Entorno

Crea un archivo .env en la raíz del proyecto:

# 🔑 Credenciales para PostgreSQL
DB_HOST=localhost
DB_NAME=proyectos_informaticos
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña_segura
DB_PORT=5432

6. ▶️ Ejecutar la Aplicación
python app.py

7. 🌐 Acceder a la Aplicación

Abre tu navegador y visita: http://127.0.0.1:5000

🎯 Funcionalidades

✅ CRUD Completo para docentes y proyectos

🎨 Interfaz Responsiva con Bootstrap 5

🔒 Configuración Segura con variables de entorno

🗄️ Base de Datos Relacional con PostgreSQL

🚀 Fácil Despliegue y configuración

🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.