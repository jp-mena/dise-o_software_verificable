Sistema de Gestión Académica (SGA)
----------------------------------

Proyecto en Flask + MySQL para registrar cursos, profesores, alumnos y evaluaciones. Parte 1 del curso ICC5130 – Diseño de Software Verificable.

REQUISITOS
----------

Antes de empezar, asegúrate de tener instalados:

- Python 3.9 o superior
- MySQL (cliente y servidor)
- Git

Recomendado: usar Linux o WSL si estás en Windows.

INSTALACIÓN Y CONFIGURACIÓN
----------------------------

1. Clonar el repositorio

    git clone https://github.com/tu-usuario/sga_proyecto.git
    cd sga_proyecto

2. Crear y activar entorno virtual

    python3 -m venv venv
    source venv/bin/activate

3. Instalar dependencias

    pip install -r requirements.txt

   Si no tienes un requirements.txt, puedes instalar manualmente:

    pip install Flask flask-mysqldb

CONFIGURACIÓN DE BASE DE DATOS
-------------------------------

1. Iniciar MySQL

    sudo systemctl start mysql

2. Crear la base de datos

    sudo mysql

    CREATE DATABASE sga_db;
    EXIT;

3. Crear las tablas

    sudo mysql sga_db < schema.sql

CONFIGURAR CONEXIÓN A LA BASE DE DATOS
--------------------------------------

Editar el archivo db_config.py:

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'sga_db'

EJECUTAR LA APLICACIÓN
-----------------------

    python app.py

Abrir navegador en http://127.0.0.1:5000

FUNCIONALIDADES DISPONIBLES
---------------------------

- Formulario para registrar alumnos
- Listado de alumnos
- CRUD futuros para profesores, cursos y evaluaciones

ARCHIVOS IMPORTANTES
--------------------

- app.py
- db_config.py
- schema.sql
- templates/

NO SUBIR venv/
--------------

.gitignore sugerido:

    venv/
    __pycache__/
    *.pyc
    .env
