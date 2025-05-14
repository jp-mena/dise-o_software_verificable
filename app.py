from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import db_config
import os
import json
from werkzeug.utils import secure_filename
from decimal import Decimal
import random
from datetime import timedelta, time

app = Flask(__name__)

app.secret_key = "supersecretkey"

# Configuración de MySQL
app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
app.config['MYSQL_USER'] = db_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = db_config.MYSQL_DB

mysql = MySQL(app)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#------------------------------ Home ------------------------------#
@app.route('/')
def index():
    return render_template('index.html')


#------------------------------ Alumnos ------------------------------#
@app.route('/alumnos/nuevo')
def nuevo_alumno():
    return render_template('alumnos/nuevo.html')

@app.route('/alumnos/crear', methods=['POST'])
def crear_alumno():
    nombre = request.form['nombre']
    correo = request.form['correo']
    fecha = request.form['fecha_ingreso']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO alumnos(nombre, correo, fecha_ingreso) VALUES (%s, %s, %s)", (nombre, correo, fecha))
    mysql.connection.commit()
    cur.close()
    return redirect('/alumnos')

@app.route('/alumnos')
def listar_alumnos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, correo, fecha_ingreso FROM alumnos")
    alumnos = cur.fetchall()
    cur.close()
    return render_template('alumnos/lista.html', alumnos=alumnos)

@app.route('/alumnos/editar/<int:id>', methods=['GET', 'POST'])
def editar_alumno(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        fecha = request.form['fecha_ingreso']
        cur.execute("""
            UPDATE alumnos 
            SET nombre = %s, correo = %s, fecha_ingreso = %s 
            WHERE id = %s
        """, (nombre, correo, fecha, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/alumnos')
    else:
        cur.execute("SELECT * FROM alumnos WHERE id = %s", (id,))
        alumno = cur.fetchone()
        cur.close()
        return render_template('alumnos/editar.html', alumno=alumno)

@app.route('/alumnos/eliminar/<int:id>')
def eliminar_alumno(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM alumnos WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar alumno con ID={id}: {e}")
    cur.close()
    return redirect('/alumnos')



#------------------------------ Profesores ------------------------------#
@app.route('/profesores')
def listar_profesores():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profesores")
    profesores = cur.fetchall()
    cur.close()
    return render_template('profesores/lista.html', profesores=profesores)

@app.route('/profesores/nuevo', methods=['GET', 'POST'])
def nuevo_profesor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO profesores (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        mysql.connection.commit()
        cur.close()
        return redirect('/profesores')
    return render_template('profesores/nuevo.html')

@app.route('/profesores/editar/<int:id>', methods=['GET', 'POST'])
def editar_profesor(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        cur.execute("UPDATE profesores SET nombre=%s, correo=%s WHERE id=%s", (nombre, correo, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/profesores')
    else:
        cur.execute("SELECT * FROM profesores WHERE id = %s", (id,))
        profesor = cur.fetchone()
        cur.close()
        return render_template('profesores/editar.html', profesor=profesor)

@app.route('/profesores/eliminar/<int:id>')
def eliminar_profesor(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM profesores WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar profesor con ID={id}: {e}")
    cur.close()
    return redirect('/profesores')



#------------------------------ Cursos ------------------------------#
@app.route('/cursos')
def listar_cursos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cursos")
    cursos = cur.fetchall()
    cur.close()
    return render_template('cursos/lista.html', cursos=cursos)

@app.route('/cursos/nuevo', methods=['GET', 'POST'])
def nuevo_curso():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cursos (codigo, nombre) VALUES (%s, %s)", (codigo, nombre))
        mysql.connection.commit()
        cur.close()
        return redirect('/cursos')
    return render_template('cursos/nuevo.html')

@app.route('/cursos/editar/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        cur.execute("UPDATE cursos SET codigo=%s, nombre=%s WHERE id=%s", (codigo, nombre, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/cursos')
    else:
        cur.execute("SELECT * FROM cursos WHERE id = %s", (id,))
        curso = cur.fetchone()
        cur.close()
        return render_template('cursos/editar.html', curso=curso)

@app.route('/cursos/eliminar/<int:id>')
def eliminar_curso(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM cursos WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar curso con ID={id}: {e}")
    cur.close()
    return redirect('/cursos')




#------------------------------ Instancias ------------------------------#

# Listar instancias (con nombre del curso)
@app.route('/instancias')
def listar_instancias():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT instancias.id, cursos.nombre, instancias.anio, instancias.semestre
        FROM instancias
        JOIN cursos ON instancias.curso_id = cursos.id
    """)
    instancias = cur.fetchall()
    cur.close()
    return render_template('instancias/lista.html', instancias=instancias)

# Crear nueva instancia
@app.route('/instancias/nuevo', methods=['GET', 'POST'])
def nueva_instancia():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        curso_id = request.form['curso_id']
        anio = request.form['anio']
        semestre = request.form['semestre']
        cur.execute("INSERT INTO instancias (curso_id, anio, semestre) VALUES (%s, %s, %s)", (curso_id, anio, semestre))
        mysql.connection.commit()
        cur.close()
        return redirect('/instancias')
    else:
        cur.execute("SELECT id, nombre FROM cursos")
        cursos = cur.fetchall()
        cur.close()
        return render_template('instancias/nuevo.html', cursos=cursos)

# Editar instancia
@app.route('/instancias/editar/<int:id>', methods=['GET', 'POST'])
def editar_instancia(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        curso_id = request.form['curso_id']
        anio = request.form['anio']
        semestre = request.form['semestre']
        cur.execute("""
            UPDATE instancias
            SET curso_id = %s, anio = %s, semestre = %s
            WHERE id = %s
        """, (curso_id, anio, semestre, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/instancias')
    else:
        cur.execute("SELECT id, nombre FROM cursos")
        cursos = cur.fetchall()
        cur.execute("SELECT * FROM instancias WHERE id = %s", (id,))
        instancia = cur.fetchone()
        cur.close()
        return render_template('instancias/editar.html', instancia=instancia, cursos=cursos)

# Eliminar instancia
@app.route('/instancias/eliminar/<int:id>')
def eliminar_instancia(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM instancias WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar instacia con ID={id}: {e}")
    cur.close()
    return redirect('/instancias')




#------------------------------ Secciones ------------------------------#

# Listar secciones
@app.route('/secciones')
def listar_secciones():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT secciones.id, cursos.nombre, instancias.anio, instancias.semestre, secciones.numero
        FROM secciones
        JOIN instancias ON secciones.instancia_id = instancias.id
        JOIN cursos ON instancias.curso_id = cursos.id
    """)
    secciones = cur.fetchall()
    cur.close()
    return render_template('secciones/lista.html', secciones=secciones)

# Crear nueva sección
@app.route('/secciones/nuevo', methods=['GET', 'POST'])
def nueva_seccion():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        instancia_id = request.form['instancia_id']
        numero = request.form['numero']
        cur.execute("INSERT INTO secciones (instancia_id, numero) VALUES (%s, %s)", (instancia_id, numero))
        mysql.connection.commit()
        cur.close()
        return redirect('/secciones')
    else:
        cur.execute("""
            SELECT instancias.id, cursos.nombre, instancias.anio, instancias.semestre
            FROM instancias
            JOIN cursos ON instancias.curso_id = cursos.id
        """)
        instancias = cur.fetchall()
        cur.close()
        return render_template('secciones/nuevo.html', instancias=instancias)

# Editar sección
@app.route('/secciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_seccion(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        instancia_id = request.form['instancia_id']
        numero = request.form['numero']
        cur.execute("""
            UPDATE secciones
            SET instancia_id = %s, numero = %s
            WHERE id = %s
        """, (instancia_id, numero, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/secciones')
    else:
        cur.execute("""
            SELECT instancias.id, cursos.nombre, instancias.anio, instancias.semestre
            FROM instancias
            JOIN cursos ON instancias.curso_id = cursos.id
        """)
        instancias = cur.fetchall()
        cur.execute("SELECT * FROM secciones WHERE id = %s", (id,))
        seccion = cur.fetchone()
        cur.close()
        return render_template('secciones/editar.html', seccion=seccion, instancias=instancias)

# Eliminar sección
@app.route('/secciones/eliminar/<int:id>')
def eliminar_seccion(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM secciones WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar seccion con ID={id}: {e}")
    cur.close()
    return redirect('/secciones')

#------------------------------ Asignaciones de Profesores ------------------------------#

# Ver todas las asignaciones
@app.route('/asignaciones')
def listar_asignaciones():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ap.id, c.nombre, i.anio, i.semestre, s.numero, p.nombre
        FROM asignaciones_profesores ap
        JOIN secciones s ON ap.seccion_id = s.id
        JOIN instancias i ON s.instancia_id = i.id
        JOIN cursos c ON i.curso_id = c.id
        JOIN profesores p ON ap.profesor_id = p.id
    """)
    asignaciones = cur.fetchall()
    cur.close()
    return render_template('asignaciones/lista.html', asignaciones=asignaciones)

# Crear nueva asignación
@app.route('/asignaciones/nuevo', methods=['GET', 'POST'])
def nueva_asignacion():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        profesor_id = request.form['profesor_id']
        seccion_id = request.form['seccion_id']
        cur.execute("INSERT INTO asignaciones_profesores (seccion_id, profesor_id) VALUES (%s, %s)", (seccion_id, profesor_id))
        mysql.connection.commit()
        cur.close()
        return redirect('/asignaciones')
    else:
        cur.execute("SELECT id, nombre FROM profesores")
        profesores = cur.fetchall()
        cur.execute("""
            SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
            FROM secciones s
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        secciones = cur.fetchall()
        cur.close()
        return render_template('asignaciones/nuevo.html', profesores=profesores, secciones=secciones)

# Editar asignación
@app.route('/asignaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_asignacion(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        profesor_id = request.form['profesor_id']
        seccion_id = request.form['seccion_id']
        cur.execute("""
            UPDATE asignaciones_profesores
            SET profesor_id = %s, seccion_id = %s
            WHERE id = %s
        """, (profesor_id, seccion_id, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/asignaciones')
    else:
        cur.execute("SELECT id, nombre FROM profesores")
        profesores = cur.fetchall()
        cur.execute("""
            SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
            FROM secciones s
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        secciones = cur.fetchall()
        cur.execute("SELECT * FROM asignaciones_profesores WHERE id = %s", (id,))
        asignacion = cur.fetchone()
        cur.close()
        return render_template('asignaciones/editar.html', profesores=profesores, secciones=secciones, asignacion=asignacion)

# Eliminar asignación
@app.route('/asignaciones/eliminar/<int:id>')
def eliminar_asignacion(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM asignaciones WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar asignacion con ID={id}: {e}")
    cur.close()
    return redirect('/asignaciones')






#------------------------------ Inscripciones ------------------------------#

@app.route('/inscripciones')
def listar_inscripciones():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT i.id, a.nombre, c.nombre, ins.anio, ins.semestre, s.numero
        FROM inscripciones i
        JOIN alumnos a ON i.alumno_id = a.id
        JOIN secciones s ON i.seccion_id = s.id
        JOIN instancias ins ON s.instancia_id = ins.id
        JOIN cursos c ON ins.curso_id = c.id
    """)
    inscripciones = cur.fetchall()
    cur.close()
    return render_template('inscripciones/lista.html', inscripciones=inscripciones)

@app.route('/inscripciones/nuevo', methods=['GET', 'POST'])
def nueva_inscripcion():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        alumno_id = request.form['alumno_id']
        seccion_id = request.form['seccion_id']
        cur.execute("INSERT INTO inscripciones (seccion_id, alumno_id) VALUES (%s, %s)", (seccion_id, alumno_id))
        mysql.connection.commit()
        cur.close()
        return redirect('/inscripciones')
    else:
        cur.execute("SELECT id, nombre FROM alumnos")
        alumnos = cur.fetchall()
        cur.execute("""
            SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
            FROM secciones s
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        secciones = cur.fetchall()
        cur.close()
        return render_template('inscripciones/nuevo.html', alumnos=alumnos, secciones=secciones)

@app.route('/inscripciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_inscripcion(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        alumno_id = request.form['alumno_id']
        seccion_id = request.form['seccion_id']
        cur.execute("""
            UPDATE inscripciones
            SET alumno_id = %s, seccion_id = %s
            WHERE id = %s
        """, (alumno_id, seccion_id, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/inscripciones')
    else:
        cur.execute("SELECT id, nombre FROM alumnos")
        alumnos = cur.fetchall()
        cur.execute("""
            SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
            FROM secciones s
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        secciones = cur.fetchall()
        cur.execute("SELECT * FROM inscripciones WHERE id = %s", (id,))
        inscripcion = cur.fetchone()
        cur.close()
        return render_template('inscripciones/editar.html', inscripcion=inscripcion, alumnos=alumnos, secciones=secciones)

@app.route('/inscripciones/eliminar/<int:id>')
def eliminar_inscripcion(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM inscripciones WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar inscripcion con ID={id}: {e}")
    cur.close()
    return redirect('/inscripciones')


#------------------------------ Evaluaciones ------------------------------#

@app.route('/evaluaciones')
def listar_evaluaciones():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.id, t.nombre AS topico_nombre, s.numero AS seccion_numero, c.nombre AS curso_nombre,
               i.anio, i.semestre, e.orden, e.valor, e.obligatoria, e.tipo, tps.seccion_id
        FROM evaluaciones e
        JOIN topicos_por_seccion tps ON e.topico_seccion_id = tps.id
        JOIN topicos t ON tps.topico_id = t.id
        JOIN secciones s ON tps.seccion_id = s.id
        JOIN instancias i ON s.instancia_id = i.id
        JOIN cursos c ON i.curso_id = c.id
        ORDER BY e.orden
    """)
    evaluaciones = cur.fetchall()
    cur.close()
    return render_template('evaluaciones/lista.html', evaluaciones=evaluaciones)



@app.route('/evaluaciones/nuevo', methods=['GET', 'POST'])
def nueva_evaluacion():
    cur = mysql.connection.cursor()
    
    # Inicializamos combinaciones vacías
    combinaciones = []

    if request.method == 'POST':
        topico_seccion_id = request.form['topico_seccion_id']
        tipo = request.form['tipo']  # 'peso' o 'porcentaje'
        valor = request.form['valor']  # El valor de la evaluación
        obligatoria = 'obligatoria' in request.form

        # Validar si el valor es negativo
        if Decimal(valor) < 0:
            flash("El valor de la evaluación no puede ser negativo.", 'error')
            return redirect('/evaluaciones/nuevo')

        # Si el tipo es porcentaje, validar que la suma no exceda 100
        if tipo == 'porcentaje':
            cur.execute("""
                SELECT SUM(valor)
                FROM evaluaciones
                JOIN topicos_por_seccion tps ON evaluaciones.topico_seccion_id = tps.id
                WHERE tps.id = %s
            """, (topico_seccion_id,))
            total_porcentaje = cur.fetchone()[0] or 0

            # Verificar si la suma total de porcentajes supera 100
            if Decimal(total_porcentaje) + Decimal(valor) > 100:
                flash("La suma de los porcentajes no puede superar 100.", 'error')
                return redirect('/evaluaciones/nuevo')

        # Obtener el orden de la evaluación automáticamente
        cur.execute("""
            SELECT MAX(orden)
            FROM evaluaciones
            WHERE topico_seccion_id = %s
        """, (topico_seccion_id,))
        max_orden = cur.fetchone()[0] or 0
        nuevo_orden = max_orden + 1  # El siguiente orden será uno más que el máximo actual

        # Insertar la nueva evaluación
        cur.execute("""
            INSERT INTO evaluaciones (topico_seccion_id, orden, valor, tipo, obligatoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (topico_seccion_id, nuevo_orden, valor, tipo, obligatoria))  # Orden se maneja automáticamente
        mysql.connection.commit()
        cur.close()

        flash("Evaluación creada con éxito", 'success')
        return redirect('/evaluaciones')

    else:
        cur.execute("""
            SELECT tps.id, t.nombre, s.numero, c.nombre, i.anio, i.semestre
            FROM topicos_por_seccion tps
            JOIN topicos t ON tps.topico_id = t.id
            JOIN secciones s ON tps.seccion_id = s.id
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        combinaciones = cur.fetchall()
        cur.close()
        return render_template('evaluaciones/nuevo.html', combinaciones=combinaciones)



@app.route('/evaluaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_evaluacion(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        topico_seccion_id = request.form['topico_seccion_id']
        orden = request.form['orden']
        valor = request.form['valor']
        obligatoria = 'obligatoria' in request.form
        cur.execute("""
            UPDATE evaluaciones
            SET topico_seccion_id=%s, orden=%s, valor=%s, obligatoria=%s
            WHERE id=%s
        """, (topico_seccion_id, orden, valor, obligatoria, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/evaluaciones')
    else:
        cur.execute("""
            SELECT tps.id, t.nombre, s.numero, c.nombre, i.anio, i.semestre
            FROM topicos_por_seccion tps
            JOIN topicos t ON tps.topico_id = t.id
            JOIN secciones s ON tps.seccion_id = s.id
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        combinaciones = cur.fetchall()
        cur.execute("SELECT * FROM evaluaciones WHERE id = %s", (id,))
        evaluacion = cur.fetchone()
        cur.close()
        return render_template('evaluaciones/editar.html', combinaciones=combinaciones, evaluacion=evaluacion)

@app.route('/evaluaciones/eliminar/<int:id>')
def eliminar_evaluacion(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM evaluaciones WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar evaluacion con ID={id}: {e}")
    cur.close()
    return redirect('/evaluaciones')

#------------------------------ Notas ------------------------------#

@app.route('/notas')
def listar_notas():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT n.id, a.nombre AS alumno_nombre, c.nombre AS curso_nombre, i.anio, i.semestre, s.numero AS seccion_numero, t.nombre AS topico_nombre, e.orden AS evaluacion_orden, n.nota
        FROM notas n
        JOIN alumnos a ON n.alumno_id = a.id
        JOIN evaluaciones e ON n.evaluacion_id = e.id
        JOIN topicos_por_seccion tps ON e.topico_seccion_id = tps.id
        JOIN topicos t ON tps.topico_id = t.id
        JOIN secciones s ON tps.seccion_id = s.id
        JOIN instancias i ON s.instancia_id = i.id
        JOIN cursos c ON i.curso_id = c.id
    """)
    notas = cur.fetchall()
    cur.close()
    return render_template('notas/lista.html', notas=notas)


@app.route('/notas/nuevo', methods=['GET', 'POST'])
def nueva_nota():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        evaluacion_id = request.form['evaluacion_id']
        alumno_id = request.form['alumno_id']
        nota = request.form['nota']
        cur.execute("""
            INSERT INTO notas (evaluacion_id, alumno_id, nota)
            VALUES (%s, %s, %s)
        """, (evaluacion_id, alumno_id, nota))
        mysql.connection.commit()
        cur.close()
        return redirect('/notas')
    else:
        cur.execute("SELECT id, nombre FROM alumnos")
        alumnos = cur.fetchall()
        cur.execute("""
            SELECT e.id, c.nombre, i.anio, i.semestre, s.numero, t.nombre, e.orden
            FROM evaluaciones e
            JOIN topicos_por_seccion tps ON e.topico_seccion_id = tps.id
            JOIN topicos t ON tps.topico_id = t.id
            JOIN secciones s ON tps.seccion_id = s.id
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        evaluaciones = cur.fetchall()
        cur.close()
        return render_template('notas/nuevo.html', alumnos=alumnos, evaluaciones=evaluaciones)

@app.route('/notas/editar/<int:id>', methods=['GET', 'POST'])
def editar_nota(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        evaluacion_id = request.form['evaluacion_id']
        alumno_id = request.form['alumno_id']
        nota = request.form['nota']
        cur.execute("""
            UPDATE notas
            SET evaluacion_id=%s, alumno_id=%s, nota=%s
            WHERE id=%s
        """, (evaluacion_id, alumno_id, nota, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/notas')
    else:
        cur.execute("SELECT id, nombre FROM alumnos")
        alumnos = cur.fetchall()
        cur.execute("""
            SELECT e.id, c.nombre, i.anio, i.semestre, s.numero, t.nombre, e.orden
            FROM evaluaciones e
            JOIN topicos_por_seccion tps ON e.topico_seccion_id = tps.id
            JOIN topicos t ON tps.topico_id = t.id
            JOIN secciones s ON tps.seccion_id = s.id
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        evaluaciones = cur.fetchall()
        cur.execute("SELECT * FROM notas WHERE id = %s", (id,))
        nota = cur.fetchone()
        cur.close()
        return render_template('notas/editar.html', nota=nota, alumnos=alumnos, evaluaciones=evaluaciones)

@app.route('/notas/eliminar/<int:id>')
def eliminar_nota(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM notas WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"No se pudo eliminar nota con ID={id}: {e}")
    cur.close()
    return redirect('/notas')

#------------------------------ Carga masiva ------------------------------#

@app.route('/alumnos/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_alumnos():
    if request.method == 'POST':
        file = request.files.get('file')
        
        # Verificar si el archivo es un JSON
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()

            # Iterar sobre los alumnos del JSON y realizar la inserción
            for alumno in data['alumnos']:
                try:
                    # Convertir anio_ingreso a formato de fecha
                    fecha_ingreso = f"{alumno['anio_ingreso']}-01-01"  # Añadir el mes y el día por defecto

                    # Insertar el alumno en la base de datos
                    cur.execute("""
                        INSERT INTO alumnos (id, nombre, correo, fecha_ingreso)
                        VALUES (%s, %s, %s, %s)
                    """, (alumno['id'], alumno['nombre'], alumno['correo'], fecha_ingreso))
                except Exception as e:
                    # Manejar error (por ejemplo, si el alumno ya existe)
                    print(f"Error al insertar alumno {alumno['nombre']}: {e}")
                    continue  # Continuar con el siguiente alumno

            mysql.connection.commit()
            cur.close()

            flash("Carga masiva de alumnos exitosa", 'success')
            return redirect('/alumnos')
        else:
            flash("Archivo inválido. Solo se permiten archivos JSON.", 'error')
            return redirect('/alumnos/carga_masiva')

    return render_template('alumnos/carga_masiva.html')

@app.route('/profesores/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_profesores():
    if request.method == 'POST':
        file = request.files.get('file')
        
        # Verificar si el archivo es un JSON
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()

            # Iterar sobre los profesores del JSON y realizar la inserción
            for prof in data['profesores']:
                try:
                    # Insertar el profesor en la base de datos
                    cur.execute("""
                        INSERT INTO profesores (id, nombre, correo)
                        VALUES (%s, %s, %s)
                    """, (prof['id'], prof['nombre'], prof['correo']))
                except Exception as e:
                    # Manejar error (por ejemplo, si el profesor ya existe)
                    print(f"Error al insertar profesor {prof['nombre']}: {e}")
                    continue  # Continuar con el siguiente profesor

            mysql.connection.commit()
            cur.close()

            flash("Carga masiva de profesores exitosa", 'success')
            return redirect('/profesores')
        else:
            flash("Archivo inválido. Solo se permiten archivos JSON.", 'error')
            return redirect('/profesores/carga_masiva')

    return render_template('profesores/carga_masiva.html')


@app.route('/cursos/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_cursos():
    if request.method == 'POST':
        file = request.files.get('file')
        
        # Verificar si el archivo es un JSON
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()

            # Iterar sobre los cursos del JSON y realizar la inserción
            for curso in data['cursos']:
                try:
                    # Insertar el curso en la base de datos
                    cur.execute("""
                        INSERT INTO cursos (id, codigo, nombre)
                        VALUES (%s, %s, %s)
                    """, (curso['id'], curso['codigo'], curso['descripcion']))
                    
                    # Insertar los requisitos del curso
                    for requisito in curso['requisitos']:
                        cur.execute("""
                            INSERT INTO requisitos (curso_id, requisito_id)
                            VALUES (%s, (SELECT id FROM cursos WHERE codigo = %s))
                        """, (curso['id'], requisito))

                except Exception as e:
                    # Manejar error (por ejemplo, si el curso ya existe)
                    print(f"Error al insertar curso {curso['codigo']}: {e}")
                    continue  # Continuar con el siguiente curso

            mysql.connection.commit()
            cur.close()

            flash("Carga masiva de cursos exitosa", 'success')
            return redirect('/cursos')
        else:
            flash("Archivo inválido. Solo se permiten archivos JSON.", 'error')
            return redirect('/cursos/carga_masiva')

    return render_template('cursos/carga_masiva.html')



@app.route('/instancias/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_instancias():
    if request.method == 'POST':
        file = request.files.get('file')
        
        # Verificar si el archivo es un JSON
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()

            # Iterar sobre las instancias y realizar la inserción
            for instancia in data['instancias']:
                try:
                    # Insertar la instancia en la base de datos
                    cur.execute("""
                        INSERT INTO instancias (id, curso_id, anio, semestre)
                        VALUES (%s, %s, %s, %s)
                    """, (instancia['id'], instancia['curso_id'], data['año'], data['semestre']))

                except Exception as e:
                    # Manejar error (por ejemplo, si la instancia ya existe o el curso_id no existe)
                    print(f"Error al insertar instancia con ID={instancia['id']}: {e}")
                    continue  # Continuar con la siguiente instancia

            mysql.connection.commit()
            cur.close()

            flash("Carga masiva de instancias exitosa", 'success')
            return redirect('/instancias')
        else:
            flash("Archivo inválido. Solo se permiten archivos JSON.", 'error')
            return redirect('/instancias/carga_masiva')

    return render_template('instancias/carga_masiva.html')


@app.route('/secciones/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_secciones():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()

            # Cargar secciones y sus evaluaciones
            for seccion_data in data['secciones']:
                try:
                    instancia_curso_id = seccion_data['instancia_curso']
                    profesor_id = seccion_data['profesor_id']
                    evaluaciones = seccion_data['evaluacion']

                    # Insertar la sección
                    cur.execute("""
                        INSERT INTO secciones (instancia_id, numero, modo_evaluacion)
                        VALUES (%s, %s, %s)
                    """, (instancia_curso_id, seccion_data['id'], evaluaciones['tipo']))
                    mysql.connection.commit()
                    seccion_id = cur.lastrowid  # Obtener el ID de la sección insertada

                    # Insertar asignación de profesor a la sección
                    cur.execute("""
                        INSERT INTO asignaciones_profesores (seccion_id, profesor_id)
                        VALUES (%s, %s)
                    """, (seccion_id, profesor_id))
                    mysql.connection.commit()

                    # Ahora se insertan los tópicos y sus evaluaciones
                    combinacion_topicos = evaluaciones['combinacion_topicos']
                    for topico_data in combinacion_topicos:
                        topico_id = topico_data['id']
                        topico_nombre = topico_data['nombre']
                        topico_valor = topico_data['valor']

                        # Insertamos el tópico solo si no existe
                        cur.execute("SELECT id FROM topicos WHERE id = %s", (topico_id,))
                        existing_topico = cur.fetchone()

                        if not existing_topico:  # Si no existe, lo insertamos
                            cur.execute("""
                                INSERT INTO topicos (id, nombre)
                                VALUES (%s, %s)
                            """, (topico_id, topico_nombre))
                            mysql.connection.commit()

                        # Insertamos la relación entre el tópico y la sección
                        cur.execute("""
                            INSERT INTO topicos_por_seccion (topico_id, seccion_id, porcentaje_total)
                            VALUES (%s, %s, %s)
                        """, (topico_id, seccion_id, topico_valor))
                        mysql.connection.commit()

                        topico_seccion_id = cur.lastrowid  # Obtener el ID de la relación topico-sección

                        # Insertamos las evaluaciones para este tópico
                        topico = seccion_data['evaluacion']['topicos'][str(topico_id)]
                        for index, valor in enumerate(topico['valores']):
                            obligatoria = topico['obligatorias'][index]
                            tipo = topico['tipo']  # 'peso' o 'porcentaje'

                            cur.execute("""
                                INSERT INTO evaluaciones (topico_seccion_id, orden, valor, tipo, obligatoria)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (topico_seccion_id, index + 1, valor, tipo, obligatoria))
                            mysql.connection.commit()

                except Exception as e:
                    mysql.connection.rollback()
                    print(f"Error al insertar la sección con ID={seccion_data['id']}: {e}")
                    continue  # Continúa con la siguiente sección si ocurre un error

            mysql.connection.commit()
            cur.close()
            flash("Secciones y evaluaciones cargadas exitosamente", 'success')
            return redirect('/secciones')
        else:
            return "Archivo inválido", 400

    return render_template('secciones/carga_masiva.html')



@app.route('/notas/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_notas():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()

            for nota_data in data['notas']:
                try:
                    alumno_id = nota_data['alumno_id']
                    topico_id = nota_data['topico_id']
                    instancia_id = nota_data['instancia']
                    nota = nota_data['nota']

                    # Obtener el topico_seccion_id (relación entre topico y seccion)
                    cur.execute("""
                        SELECT tps.id
                        FROM topicos_por_seccion tps
                        JOIN secciones s ON tps.seccion_id = s.id
                        JOIN instancias i ON s.instancia_id = i.id
                        WHERE tps.topico_id = %s AND i.id = %s
                    """, (topico_id, instancia_id))
                    topico_seccion_id = cur.fetchone()

                    if not topico_seccion_id:
                        print(f"Error: No se encontró el topico_seccion_id para el tópico {topico_id} y la instancia {instancia_id}.")
                        continue  # Si no existe la relación, seguimos con el siguiente dato

                    topico_seccion_id = topico_seccion_id[0]  # Obtener el valor de la primera columna del resultado

                    # Verificar si el alumno ya está inscrito en la sección correspondiente
                    cur.execute("""
                        SELECT 1
                        FROM inscripciones
                        WHERE alumno_id = %s AND seccion_id IN (
                            SELECT s.id
                            FROM secciones s
                            JOIN instancias i ON s.instancia_id = i.id
                            WHERE i.id = %s
                        )
                    """, (alumno_id, instancia_id))

                    # Si el alumno no está inscrito en la sección, lo inscribimos
                    if not cur.fetchone():
                        print(f"El alumno {alumno_id} no está inscrito en la sección correspondiente a la instancia {instancia_id}. Se procederá a inscribirlo.")
                        cur.execute("""
                            INSERT INTO inscripciones (seccion_id, alumno_id)
                            SELECT s.id, %s
                            FROM secciones s
                            JOIN instancias i ON s.instancia_id = i.id
                            WHERE i.id = %s
                        """, (alumno_id, instancia_id))
                        mysql.connection.commit()

                    # Insertar la nota para la evaluación
                    cur.execute("""
                        INSERT INTO notas (evaluacion_id, alumno_id, nota)
                        SELECT e.id, %s, %s
                        FROM evaluaciones e
                        WHERE e.topico_seccion_id = %s
                    """, (alumno_id, nota, topico_seccion_id))
                    mysql.connection.commit()

                except Exception as e:
                    mysql.connection.rollback()
                    print(f"Error al insertar nota para el alumno {alumno_id} y el tópico {topico_id}: {e}")
                    continue  # Si ocurre un error, seguimos con el siguiente dato

            mysql.connection.commit()
            cur.close()
            flash("Notas cargadas exitosamente", 'success')
            return redirect('/notas')
        else:
            return "Archivo inválido", 400

    return render_template('notas/carga_masiva.html')



#------------------------------ Tópicos ------------------------------#

@app.route('/topicos')
def listar_topicos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM topicos")
    topicos = cur.fetchall()
    cur.close()
    return render_template('topicos/lista.html', topicos=topicos)

@app.route('/topicos/nuevo', methods=['GET', 'POST'])
def nuevo_topico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO topicos (nombre) VALUES (%s)", (nombre,))
        mysql.connection.commit()
        cur.close()
        return redirect('/topicos')
    return render_template('topicos/nuevo.html')

@app.route('/topicos/editar/<int:id>', methods=['GET', 'POST'])
def editar_topico(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        cur.execute("UPDATE topicos SET nombre = %s WHERE id = %s", (nuevo_nombre, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/topicos')
    else:
        cur.execute("SELECT * FROM topicos WHERE id = %s", (id,))
        topico = cur.fetchone()
        cur.close()
        return render_template('topicos/editar.html', topico=topico)

@app.route('/topicos/eliminar/<int:id>')
def eliminar_topico(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM topicos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/topicos')

#------------------------------ Asignar Tópico a Sección ------------------------------#

@app.route('/topicos/asignar', methods=['GET', 'POST'])
def asignar_topico_a_seccion():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        seccion_id = request.form['seccion_id']
        topico_id = request.form['topico_id']
        porcentaje_total = request.form['porcentaje_total']
        cur.execute("""
            INSERT INTO topicos_por_seccion (topico_id, seccion_id, porcentaje_total)
            VALUES (%s, %s, %s)
        """, (topico_id, seccion_id, porcentaje_total))
        mysql.connection.commit()
        cur.close()
        return redirect('/topicos/asignaciones')

    # Mostrar formulario GET
    cur.execute("SELECT id, nombre FROM topicos")
    topicos = cur.fetchall()
    cur.execute("""
        SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
        FROM secciones s
        JOIN instancias i ON s.instancia_id = i.id
        JOIN cursos c ON i.curso_id = c.id
    """)
    secciones = cur.fetchall()
    cur.close()
    return render_template('topicos_por_seccion/nuevo.html', topicos=topicos, secciones=secciones)


@app.route('/topicos/asignaciones')
def listar_topicos_asignados():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            s.numero,               -- Número de la sección
            c.nombre,               -- Nombre del curso
            i.anio,                 -- Año
            i.semestre,             -- Semestre
            t.nombre,               -- Nombre del tópico
            tps.porcentaje_total,   -- Porcentaje o peso del tópico
            e.tipo,                 -- Tipo de evaluación (peso o porcentaje) desde la tabla de evaluaciones
            tps.id                  -- ID de la relación (topico-sección)
        FROM topicos_por_seccion tps
        JOIN secciones s ON tps.seccion_id = s.id
        JOIN instancias i ON s.instancia_id = i.id
        JOIN cursos c ON i.curso_id = c.id
        JOIN topicos t ON tps.topico_id = t.id
        JOIN evaluaciones e ON e.topico_seccion_id = tps.id  -- Unimos la tabla de evaluaciones para traer el tipo
    """)
    asignaciones = cur.fetchall()
    cur.close()
    return render_template('topicos_por_seccion/lista.html', asignaciones=asignaciones)



@app.route('/topicos/asignar/editar/<int:id>', methods=['GET', 'POST'])
def editar_topico_asignado(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        topico_id = request.form['topico_id']
        seccion_id = request.form['seccion_id']
        porcentaje_total = request.form['porcentaje_total']
        cur.execute("""
            UPDATE topicos_por_seccion
            SET topico_id = %s, seccion_id = %s, porcentaje_total = %s
            WHERE id = %s
        """, (topico_id, seccion_id, porcentaje_total, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/topicos/asignaciones')
    else:
        cur.execute("SELECT id, nombre FROM topicos")
        topicos = cur.fetchall()
        cur.execute("""
            SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
            FROM secciones s
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        secciones = cur.fetchall()
        cur.execute("SELECT * FROM topicos_por_seccion WHERE id = %s", (id,))
        asignacion = cur.fetchone()
        cur.close()
        return render_template('topicos_por_seccion/editar.html', topicos=topicos, secciones=secciones, asignacion=asignacion)


@app.route('/topicos/asignar/eliminar/<int:id>')
def eliminar_topico_asignado(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM topicos_por_seccion WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/topicos/asignaciones')

#------------------------------ Salas ------------------------------#

@app.route('/salas')
def listar_salas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM salas")
    salas = cur.fetchall()
    cur.close()
    return render_template('salas/lista.html', salas=salas)


@app.route('/salas/nuevo', methods=['GET', 'POST'])
def nueva_sala():
    if request.method == 'POST':
        nombre = request.form['nombre']
        capacidad = request.form['capacidad']

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO salas (nombre, capacidad)
                VALUES (%s, %s)
            """, (nombre, capacidad))
            mysql.connection.commit()
            flash("Sala creada con éxito.", 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error al crear la sala: {e}", 'error')
        finally:
            cur.close()

        return redirect('/salas')

    return render_template('salas/nuevo.html')


@app.route('/salas/editar/<int:id>', methods=['GET', 'POST'])
def editar_sala(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        capacidad = request.form['capacidad']

        try:
            cur.execute("""
                UPDATE salas
                SET nombre = %s, capacidad = %s
                WHERE id = %s
            """, (nombre, capacidad, id))
            mysql.connection.commit()
            flash("Sala actualizada con éxito.", 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error al actualizar la sala: {e}", 'error')
        finally:
            cur.close()

        return redirect('/salas')

    cur.execute("SELECT * FROM salas WHERE id = %s", (id,))
    sala = cur.fetchone()
    cur.close()
    return render_template('salas/editar.html', sala=sala)


@app.route('/salas/eliminar/<int:id>', methods=['POST'])
def eliminar_sala(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM salas WHERE id = %s", (id,))
        mysql.connection.commit()
        flash("Sala eliminada exitosamente", 'success')  # Confirmación de eliminación exitosa
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error al eliminar la sala con ID={id}: {e}", 'danger')  # Si ocurre un error, se muestra un mensaje
    cur.close()
    return redirect('/salas')


@app.route('/salas/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_salas():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()

            # Cargar las salas del JSON
            for sala_data in data['salas']:
                try:
                    nombre = sala_data['nombre']
                    capacidad = sala_data['capacidad']

                    # Insertar la sala
                    cur.execute("""
                        INSERT INTO salas (id, nombre, capacidad)
                        VALUES (%s, %s, %s)
                    """, (sala_data['id'], nombre, capacidad))
                    mysql.connection.commit()

                except Exception as e:
                    mysql.connection.rollback()
                    print(f"Error al insertar la sala {sala_data['nombre']}: {e}")
                    continue  # Continúa con la siguiente sala si ocurre un error

            mysql.connection.commit()
            cur.close()
            flash("Salas cargadas exitosamente", 'success')
            return redirect('/salas')
        else:
            return "Archivo inválido", 400

    return render_template('salas/carga_masiva.html')


#------------------------------ Asignar horarios ------------------------------#


# Para obtener las secciones y asignarles horarios
@app.route('/asignar_horarios', methods=['GET'])
def asignar_horarios():
    cur = mysql.connection.cursor()

    # Obtener las secciones que no tienen horario asignado
    cur.execute("""
        SELECT s.id, s.instancia_id, c.nombre, s.numero, s.modo_evaluacion
        FROM secciones s
        JOIN instancias i ON s.instancia_id = i.id
        JOIN cursos c ON i.curso_id = c.id
        WHERE s.id NOT IN (SELECT seccion_id FROM horarios)
    """)
    secciones = cur.fetchall()

    # Obtener las salas disponibles
    cur.execute("SELECT id, nombre, capacidad FROM salas")
    salas = cur.fetchall()

    # Asignar horarios
    for seccion in secciones:
        seccion_id = seccion[0]
        curso_nombre = seccion[2]
        numero_seccion = seccion[3]

        # Obtener el número de créditos (horas de clase) para este curso
        cur.execute("""
            SELECT creditos
            FROM cursos
            WHERE nombre = %s
        """, (curso_nombre,))
        creditos = cur.fetchone()[0]

        # Generar la cantidad de horas que se necesitan para esta sección
        horas_requeridas = creditos  # Asumimos que cada crédito es 1 hora de clase

        # Seleccionar una sala con suficiente capacidad
        sala = random.choice(salas)

        # Generar los horarios posibles
        horarios_disponibles = [
            {'dia': 'lunes', 'hora_inicio': time(9, 0), 'hora_fin': time(11, 0)},
            {'dia': 'martes', 'hora_inicio': time(9, 0), 'hora_fin': time(11, 0)},
            # Otras combinaciones de horarios
        ]

        # Asignar horarios a esta sección
        for horario in horarios_disponibles[:horas_requeridas]:
            cur.execute("""
                INSERT INTO horarios (seccion_id, sala_id, dia, hora_inicio, hora_fin)
                VALUES (%s, %s, %s, %s, %s)
            """, (seccion_id, sala[0], horario['dia'], horario['hora_inicio'], horario['hora_fin']))

        mysql.connection.commit()

    cur.close()
    return redirect('/calendario')




if __name__ == '__main__':
    app.run(debug=True)
