from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

DATABASE = 'sessions_db'
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key=("wdjidwdwkdwa")

def is_logged_in():
    if (session.get('user_id') is None):
        print("Not logged in")
        return False
    else:
        print("Logged in")
        return True

def connect_to_database(db_file):
    try:
        con = sqlite3.connect(db_file)
        return con
    except Error:
        print("an error has occured connecting to the database")
    return


@app.route('/')
def render_home():  # put application's code here
    return render_template('home.html', logged_in=is_logged_in())


@app.route('/log_in', methods=['POST', 'GET'])
def render_log_in():  # put application's code here
    if is_logged_in():
        return redirect('/booking')
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password=request.form['password']
        query="SELECT Student_id,fname,lname,password,email FROM session_db WHERE email=?"
        con=connect_to_database(DATABASE)
        cur=con.cursor()
        cur.execute(query,(email))
        user_info=cur.fetcall()
        print(user_info)
        cur.close()
        try:
            user_id=user_info[0]
            first_name=user_info[1]
            user_password=user_info[2]
        except IndexError:
            return redirect("/login?error=email+or+password+inalid")

        if not bcrypt.check_password_hash(user_password,password):
            return redirect("/login?error=email+or+password+inalid")

        session["email"]=email
        session["user_id"]=user_id
        session["first_name"]=first_name
        print(session)
        return redirect("/")


    return render_template('log_in.html',logged_in=is_logged_in())

@app.route('/student_log_in', methods=['POST', 'GET'])
def render_student_log_in():  # put application's code here
    if is_logged_in():
        return redirect('/booking')
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password=request.form['password']
        query="SELECT Student_id,fname,lname,password,email FROM session_db WHERE email=?"
        con=connect_to_database(DATABASE)
        cur=con.cursor()
        cur.execute(query,(email))
        user_info=cur.fetcall()
        print(user_info)
        cur.close()
        try:
            user_id=user_info[0]
            first_name=user_info[1]
            user_password=user_info[2]
        except IndexError:
            return redirect("/login?error=email+or+password+inalid")

        if not bcrypt.check_password_hash(user_password,password):
            return redirect("/login?error=email+or+password+inalid")

        session["email"]=email
        session["user_id"]=user_id
        session["first_name"]=first_name
        print(session)
        return redirect("/")


    return render_template('student_log_in.html',logged_in=is_logged_in())

@app.route('/sign_up', methods=['POST', 'GET'])
def render_sign_up():
    if request.method == 'POST':
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password = request.form.get('user_password')
        password2 = request.form.get('user_password2')
        if password != password2:
            return redirect("/signup?error=passwords+do+not+match")
        if len(password) < 8:
            return redirect("/signup?error=password+too+short+must+be+longer+than+8")
        hashed_password=bcrypt.generate_password_hash(password)
        connection = connect_to_database(DATABASE)
        query_insert = "INSERT INTO Session_db(fname,lname,password,email)VALUES(?,?,?,?)"
        cur = connection.cursor()
        cur.execute(query_insert, (fname, lname, hashed_password, email))
        connection.commit()
        return render_template('log_in.html',logged_in=is_logged_in())

    return render_template('sign_up.html')


@app.route('/booking', methods=['POST', 'GET'])
def render_booking():
    if request.method == 'POST':
        time_u = request.form.get('booking_date')
        where = request.form.get('where').title().strip()
        connection = connect_to_database(DATABASE)
        query_insert = "INSERT INTO booking_db(date_u,location)VALUES(?,?)"
        cur = connection.cursor()
        cur.execute(query_insert, (time_u, where))
        connection.commit()

    return render_template('booking.html')
@app.route('/print_booking')
def render_current_booking():
    connection = connect_to_database(DATABASE)
    query = "SELECT date_u,location FROM booking_db"
    cur = connection.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    print(product_list)
    return render_template('show_booking.html',booking_list=product_list)

@app.route('/log_out', methods=['POST', 'GET'])
def logout():
    print(f'session values{session}')
    session.clear()
    print(session)
    return redirect("/?message=See+you+next+time")

if __name__ == '__main__':
    app.run()
