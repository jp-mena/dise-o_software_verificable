# Sistema de Gestión Académica – Proyecto ICC5130 (Parte 1)

Este sistema web permite administrar alumnos, profesores, cursos, instancias, secciones, inscripciones, evaluaciones y notas. Desarrollado con Flask y MySQL como parte del curso ICC5130.

---

## ✅ Requisitos

- Python 3.10+
- MySQL Server
- pip (gestor de paquetes de Python)

---

## 🚀 Instrucciones de instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

2. **Crear un entorno virtual**

```bash
python3 -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Crear la base de datos en MySQL**

Abre MySQL y crea la base de datos:

```sql
CREATE DATABASE sga_db;
```

Luego ejecuta el archivo SQL:

```bash
mysql -u TU_USUARIO -p sga_db < schema.sql
```

5. **(Opcional) Poblar la base de datos con datos de ejemplo**

Puedes cargar datos de prueba como alumnos, profesores, cursos, evaluaciones y notas ejecutando:

```bash
mysql -u TU_USUARIO -p sga_db < populate.sql
```

6. **Configurar credenciales en `db_config.py`**

Transforma el archivo `db_config.py.example` a  `db_config.py` y modifica los valores:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'tu_usuario'
MYSQL_PASSWORD = 'tu_contraseña'
MYSQL_DB = 'sga_db'
```

7. **Ejecutar la aplicación**

```bash
python app.py
```

7. **Abrir en el navegador**

Ir a: [http://localhost:5000](http://localhost:5000)

---

## 📁 Estructura principal

```
├── app.py
├── db_config.py
├── requirements.txt
├── schema.sql
├── populate.sql
├── /templates/
│   ├── index.html
│   ├── base.html
│   └── (carpetas por entidad)
└── /static/
    └── js/
```

---
