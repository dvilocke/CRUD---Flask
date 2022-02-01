from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#Recursos: https://bootswatch.com/
#Recursos: https://getbootstrap.com/docs/5.1/components/navbar/
#Recursos: https://uigradients.com/#ColorsOfSky
app = Flask(__name__)

#mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#SESION = una sension es simplemente datos que guardan
#nuestra aplicaicion de servidor para luego poder reutilizarlos
#lo podemos guardar en cookies, memoria del navegador, servidor, memoria de la aplicacion
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    return render_template('index.html', contacts = cur.fetchall())

@app.route('/add/', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        #me permite ejecutar las consultas
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)',
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added succesfull')

        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/edit/<int:id>')
def get_contact(id):
    cur =  mysql.connection.cursor()
    cur.execute(f'SELECT * FROM contacts WHERE id={int(id)}')
    data = cur.fetchall()
    return render_template('edit-contact.html', data=data[0])

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur =  mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact Update Successfully')
        return redirect(url_for('index'))


@app.route('/delete/<int:id>/')
def delete_contact(id):
    cur =  mysql.connection.cursor()
    cur.execute(f'DELETE FROM contacts WHERE id = {id}')
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))




