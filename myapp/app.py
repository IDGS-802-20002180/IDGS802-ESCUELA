from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask_wtf.csrf import CSRFProtect
import flask
from Alumnos.routes import alumnos
from Maestros.routes import maestros
from config import DevelopmentConfig
from models import db
#from Directivos.routes import dir
#from Maestros.routes import maestros

app=flask.Flask(__name__)
app.config['DEBUG']=True
csrf=CSRFProtect()
app.config.from_object(DevelopmentConfig)

@app.route("/",methods=["GET"])
def index():
    
    return render_template("index.html")

app.register_blueprint(alumnos)
app.register_blueprint(maestros)


if __name__=='__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=3000)