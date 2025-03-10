from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
@app.route('/')
def render_home():  # put application's code here
    return render_template('home.html')