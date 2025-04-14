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

# Ruta para mostrar formulario
@app.route('/alumnos/nuevo')
def nuevo_alumno():
    return render_template('alumnos_form.html')

# Ruta para insertar alumno
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

# Ruta para listar alumnos
@app.route('/alumnos')
def listar_alumnos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, correo, fecha_ingreso FROM alumnos")
    alumnos = cur.fetchall()
    cur.close()
    return render_template('alumnos_lista.html', alumnos=alumnos)

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Editar alumno
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
        return render_template('alumnos_editar.html', alumno=alumno)

# Eliminar alumno
@app.route('/alumnos/eliminar/<int:id>')
def eliminar_alumno(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM alumnos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/alumnos')


if __name__ == '__main__':
    app.run(debug=True)
