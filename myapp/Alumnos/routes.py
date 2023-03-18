
from flask import Blueprint
from flask import Flask, redirect, render_template
from flask import request,flash
from flask import url_for
#import Alumnos.forms

from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect

from models import db #ORM SQLAlchemy
from models import Alumnos
import forms

#Definimos el nombre que tendran nuestros decoradores
alumnos=Blueprint('alumnos',__name__)
#app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
alumnos.secret_key = "clave_secreta"

@alumnos.route("/alumnos",methods=["GET","POST"])
def alumnosGet():
    create_form=forms.UserForm(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=create_form.nombre.data,
                    apellidos=create_form.apellidos.data,
                    email=create_form.email.data)
        #Con esta instruccion guardamos los datos en la bd
        db.session.add(alum)
        db.session.commit()
        flash("El registro se ha guardado exitosamente.", "exito")
        return redirect(url_for('alumnos.ABCompleto'))
    return render_template('alumnos.html',form=create_form)


@alumnos.route("/modificar",methods=["GET","POST"])
def modificar():
    create_fprm=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        print("este es el id: "+id)
        create_fprm.id.data=request.args.get('id')
        create_fprm.nombre.data=alum1.nombre
        create_fprm.apellidos.data=alum1.apellidos
        create_fprm.email.data=alum1.email
    if request.method=='POST':
        id=create_fprm.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_fprm.nombre.data
        alum.apellidos=create_fprm.apellidos.data
        alum.email=create_fprm.email.data
        db.session.add(alum)
        db.session.commit()
        flash("El registro se ha modificado exitosamente.", "exito")
        return redirect(url_for('alumnos.ABCompleto'))
    return render_template('modificar.html',form=create_fprm)

@alumnos.route("/eliminar",methods=["GET","POST"])
def eliminar():
    create_fprm=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        print("este es el id: "+id)
        create_fprm.id.data=request.args.get('id')
        create_fprm.nombre.data=alum1.nombre
        create_fprm.apellidos.data=alum1.apellidos
        create_fprm.email.data=alum1.email
    if request.method=='POST':
        id=create_fprm.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_fprm.nombre.data
        alum.apellidos=create_fprm.apellidos.data
        alum.email=create_fprm.email.data
        db.session.delete(alum)
        db.session.commit()
        flash("El registro se ha eliminado exitosamente.", "exito")
        return redirect(url_for('alumnos.ABCompleto'))
    return render_template('eliminar.html',form=create_fprm)
    

@alumnos.route("/ABCompleto",methods=["GET","POST"])
def ABCompleto():
    create_form=forms.UserForm(request.form)
    alumno=Alumnos.query.all()
    
    return render_template("ABCompleto.html",form=create_form,alumno=alumno)

