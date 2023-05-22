import requests
from flask import Flask, render_template, request, redirect
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="aleksejkessler",
                        password="8205",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()



@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if len(username) == 0 or len(password) == 0:
                return render_template('account.html', error="Empty")
            cursor.execute("SELECT * FROM service.users WHERE login='{}' AND password='{}'".format(str(username), str(password)))
            records = list(cursor.fetchall())

            if len(records) == 0:
                return render_template('account.html', error="NotFound")

            return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if len(name) == 0 or len(login) == 0 or len(password) == 0:
            return render_template('registration_error.html', error = "Empty")

        try:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            return render_template('registration_error.html', error="NotUnique")

        return redirect('/')

    return render_template('registration.html')

if __name__ == '__main__':
    app.run()
