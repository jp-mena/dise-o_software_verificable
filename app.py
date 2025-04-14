from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import db_config

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
app.config['MYSQL_USER'] = db_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = db_config.MYSQL_DB

mysql = MySQL(app)

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
    cur.execute("DELETE FROM alumnos WHERE id = %s", (id,))
    mysql.connection.commit()
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
    cur.execute("DELETE FROM profesores WHERE id = %s", (id,))
    mysql.connection.commit()
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
    cur.execute("DELETE FROM cursos WHERE id = %s", (id,))
    mysql.connection.commit()
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
    cur.execute("DELETE FROM instancias WHERE id = %s", (id,))
    mysql.connection.commit()
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
    cur.execute("DELETE FROM secciones WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/secciones')


if __name__ == '__main__':
    app.run(debug=True)
