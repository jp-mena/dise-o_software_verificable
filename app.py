from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import db_config
import os
import json
from werkzeug.utils import secure_filename


app = Flask(__name__)

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
        SELECT e.id, c.nombre, i.anio, i.semestre, s.numero, e.tipo, e.peso, e.es_opcional
        FROM evaluaciones e
        JOIN secciones s ON e.seccion_id = s.id
        JOIN instancias i ON s.instancia_id = i.id
        JOIN cursos c ON i.curso_id = c.id
    """)
    evaluaciones = cur.fetchall()
    cur.close()
    return render_template('evaluaciones/lista.html', evaluaciones=evaluaciones)

@app.route('/evaluaciones/nuevo', methods=['GET', 'POST'])
def nueva_evaluacion():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        seccion_id = request.form['seccion_id']
        tipo = request.form['tipo']
        peso = request.form['peso']
        es_opcional = 'es_opcional' in request.form
        cur.execute("""
            INSERT INTO evaluaciones (seccion_id, tipo, peso, es_opcional)
            VALUES (%s, %s, %s, %s)
        """, (seccion_id, tipo, peso, es_opcional))
        mysql.connection.commit()
        cur.close()
        return redirect('/evaluaciones')
    else:
        cur.execute("""
            SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
            FROM secciones s
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        secciones = cur.fetchall()
        cur.close()
        return render_template('evaluaciones/nuevo.html', secciones=secciones)

@app.route('/evaluaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_evaluacion(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        seccion_id = request.form['seccion_id']
        tipo = request.form['tipo']
        peso = request.form['peso']
        es_opcional = 'es_opcional' in request.form
        cur.execute("""
            UPDATE evaluaciones
            SET seccion_id=%s, tipo=%s, peso=%s, es_opcional=%s
            WHERE id=%s
        """, (seccion_id, tipo, peso, es_opcional, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/evaluaciones')
    else:
        cur.execute("""
            SELECT s.id, c.nombre, i.anio, i.semestre, s.numero
            FROM secciones s
            JOIN instancias i ON s.instancia_id = i.id
            JOIN cursos c ON i.curso_id = c.id
        """)
        secciones = cur.fetchall()
        cur.execute("SELECT * FROM evaluaciones WHERE id = %s", (id,))
        evaluacion = cur.fetchone()
        cur.close()
        return render_template('evaluaciones/editar.html', evaluacion=evaluacion, secciones=secciones)

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
        SELECT n.id, a.nombre, c.nombre, i.anio, i.semestre, s.numero, e.tipo, n.nota
        FROM notas n
        JOIN alumnos a ON n.alumno_id = a.id
        JOIN evaluaciones e ON n.evaluacion_id = e.id
        JOIN secciones s ON e.seccion_id = s.id
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
            SELECT e.id, c.nombre, i.anio, i.semestre, s.numero, e.tipo
            FROM evaluaciones e
            JOIN secciones s ON e.seccion_id = s.id
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
            SELECT e.id, c.nombre, i.anio, i.semestre, s.numero, e.tipo
            FROM evaluaciones e
            JOIN secciones s ON e.seccion_id = s.id
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



@app.route('/cursos/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_cursos():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()
            for curso in data:
                try:
                    cur.execute("""
                        INSERT INTO cursos (id, codigo, nombre)
                        VALUES (%s, %s, %s)
                    """, (curso['id'], curso['codigo'], curso['nombre']))
                except Exception as e:
                    print(f"Error en curso {curso['codigo']}: {e}")
                    continue

            mysql.connection.commit()
            cur.close()
            return redirect('/cursos')
        else:
            return "Archivo inválido", 400

    return render_template('cursos/carga_masiva.html')

@app.route('/profesores/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_profesores():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()
            for prof in data:
                try:
                    cur.execute("""
                        INSERT INTO profesores (id, nombre, correo)
                        VALUES (%s, %s, %s)
                    """, (prof['id'], prof['nombre'], prof['correo']))
                except Exception as e:
                    print(f"Error profesor {prof['nombre']}: {e}")
                    continue

            mysql.connection.commit()
            cur.close()
            return redirect('/profesores')
        else:
            return "Archivo inválido", 400

    return render_template('profesores/carga_masiva.html')

@app.route('/alumnos/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_alumnos():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            cur = mysql.connection.cursor()
            for alumno in data:
                try:
                    cur.execute("""
                        INSERT INTO alumnos (id, nombre, correo, fecha_ingreso)
                        VALUES (%s, %s, %s, %s)
                    """, (alumno['id'], alumno['nombre'], alumno['correo'], alumno['fecha_ingreso']))
                except Exception as e:
                    print(f"Error alumno {alumno['nombre']}: {e}")
                    continue

            mysql.connection.commit()
            cur.close()
            return redirect('/alumnos')
        else:
            return "Archivo inválido", 400

    return render_template('alumnos/carga_masiva.html')


@app.route('/instancias/carga_masiva', methods=['GET', 'POST'])
def carga_masiva_instancias():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)
            cur = mysql.connection.cursor()
            for instancia in data:
                try:
                    cur.execute("""
                        INSERT INTO instancias (id, curso_id, anio, semestre)
                        VALUES (%s, %s, %s, %s)
                    """, (instancia['id'], instancia['curso_id'], instancia['anio'], instancia['semestre']))
                except Exception as e:
                    print(f"Error instancia ID={instancia['id']}: {e}")
                    continue
            mysql.connection.commit()
            cur.close()
            return redirect('/instancias')
        else:
            return "Archivo inválido", 400
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
            for seccion in data:
                try:
                    cur.execute("""
                        INSERT INTO secciones (id, instancia_id, numero)
                        VALUES (%s, %s, %s)
                    """, (seccion['id'], seccion['instancia_id'], seccion['numero']))
                except Exception as e:
                    print(f"Error sección ID={seccion['id']}: {e}")
                    continue
            mysql.connection.commit()
            cur.close()
            return redirect('/secciones')
        else:
            return "Archivo inválido", 400
    return render_template('secciones/carga_masiva.html')

if __name__ == '__main__':
    app.run(debug=True)
