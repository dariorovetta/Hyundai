from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql conexión
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root2"  # Usuario base de datos
app.config["MYSQL_PASSWORD"] = "password"  # Clave base de datos
app.config["MYSQL_DB"] = "flaskcontacts"  # Conexión con base de datos
mysql = MySQL(app)

# Inicializar una sesión
app.secret_key = "mysecretkey"


# Función de mensaje de inicio de la página web
@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    return render_template("index.html", contacts=data)


# Agregar contactos
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        # Escribimos la consulta
        cur.execute("INSERT INTO contacts (fullname, phone, email) "
                    "VALUES (%s, %s, %s)", (fullname, phone, email))
        # Ejecutamos la consulta
        mysql.connection.commit()
        # Asignar mensaje
        flash("Contacto agregado correctamente")
        return redirect(url_for("Index"))


# Editar un dato
@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM contacts WHERE id = {id}")
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact=data[0])


# Crear ruta donde guardar datos editados
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))


# Eliminar un dato
@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
