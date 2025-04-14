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


if __name__ == '__main__':
    app.run(debug=True)
