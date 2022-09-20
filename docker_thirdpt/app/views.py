from app import app
from flask import render_template

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def index2():
    return render_template("about.html")

@app.route('/model')
def index3():
    return render_template("model.html")    

@app.route('/analysis')
def index4():
    return render_template("analysis.html")
