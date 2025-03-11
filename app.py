from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

DATABASE = 'sessions_db'
app = Flask(__name__)


def connect_to_database(db_file):
    try:
        con = sqlite3.connect(db_file)
        return con
    except Error:
        print("an error has occured connecting to the database")
    return

@app.route('/')
def render_home():  # put application's code here
    return render_template('home.html')

@app.route('/log_in', methods=['POST','GET'])
def render_log_in():  # put application's code here
    return render_template('log_in.html')

@app.route('/sign_up', methods=['POST','GET'])
def render_sign_up():
    if request.method =='POST':
        fname=request.form.get('user_fname').title().strip()
        lname=request.form.get('user_lname').title().strip()
        email=request.form.get('user_email').lower().strip()
        password=request.form.get('user_password')
        password2=request.form.get('user_password2')
        if password!=password2:
            return redirect("/signup?error=passwords+do+not+match")
        if len(password)<8:
            return redirect("/signup?error=password+too+short+must+be+longer+than+8")
        connection = connect_to_database(DATABASE)
        query_insert="INSERT INTO Session_db(fname,lname,password,email)VALUES(?,?,?,?)"
        cur = connection.cursor()
        cur.execute(query_insert,(fname,lname,password,email))
        connection.commit()
        product_list = cur.fetchall()

    return render_template('sign_up.html')
@app.route('/menu')
def render_menu():  # put application's code here
    connection = connect_to_database(DATABASE)
    query = "SELECT First_name, Last_name, password, email FROM session_db"
    cur = connection.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    return render_template('menu.html')


if __name__ == '__main__':
    app.run()