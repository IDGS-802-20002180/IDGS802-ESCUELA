
from flask import Blueprint
from flask import Flask, redirect, render_template
from flask import request,flash
from flask import url_for
from db import get_connection
from sqlalchemy import text

#import Alumnos.forms

from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect

from models import db #ORM SQLAlchemy
from models import Maestros
import forms

#Definimos el nombre que tendran nuestros decoradores
maestros=Blueprint('maestros',__name__)
#app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
maestros.secret_key = "clave_secreta"

@maestros.route("/maestros",methods=["GET","POST"])
def maestros_post():
    create_form = forms.MaestrosForm(request.form)
    error = ''
    if request.method == 'POST':
        alum = Maestros(nombre=create_form.nombreM.data,
                        apellidos=create_form.apellidosM.data,
                        email=create_form.emailM.data)
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call agregar_maestro(%s,%s,%s)',
                                (alum.nombre, alum.apellidos, alum.email))
            connection.commit()
            connection.close()
            flash("El registro se ha guardado exitosamente.", "exito")
            return redirect(url_for('maestros.ABCompleto2'))
        except Exception as ex:
            error='ERROR {}'.format(ex)
            print(error)
            flash("El registro no se logro guardar.", "error")
        return redirect(url_for('maestros.ABCompleto2'))
    return render_template('maestros.html', form=create_form, error=error)


@maestros.route("/modificarM", methods=["GET", "POST"])
def modificarM():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'GET':
        id_maestro = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call mostrarUnoMaestros(%s)',(id_maestro))
                maestro=cursor.fetchall()
            connection.commit()
            connection.close()
            create_form.idM.data=request.args.get('id')
            create_form.nombreM.data=maestro[0][1]
            create_form.apellidosM.data=maestro[0][2]
            create_form.emailM.data=maestro[0][3]
        except Exception as ex:
            print('ERROR{}'.format(ex))
    if request.method == 'POST':
        id_maestro = create_form.idM.data
        nombre = create_form.nombreM.data
        apellidos = create_form.apellidosM.data
        email = create_form.emailM.data
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call modificar_maestro(%s,%s,%s,%s)',(id_maestro,nombre,apellidos,email))
                connection.commit()
                connection.close()
                flash("El registro se ha modificado exitosamente.", "exito")
        except Exception as ex:
            print('ERROR{}'.format(ex))
            flash("El registro no logro modificarse.", "error")
        return redirect(url_for('maestros.ABCompleto2'))
    return render_template('modificarM.html', form=create_form)


@maestros.route("/eliminarM",methods=["GET","POST"])
def eliminarM():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'GET':
        id_maestro = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call mostrarUnoMaestros(%s)',(id_maestro))
                maestro=cursor.fetchall()
            connection.commit()
            connection.close()
            create_form.idM.data=request.args.get('id')
            create_form.nombreM.data=maestro[0][1]
            create_form.apellidosM.data=maestro[0][2]
            create_form.emailM.data=maestro[0][3]
        except Exception as ex:
            print('ERROR{}'.format(ex))
       
    if request.method == 'POST':
        id_maestro = create_form.idM.data
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call eliminar_maestro(%s)',(id_maestro))
                connection.commit()
                connection.close()
                flash("El registro se ha eliminado exitosamente.", "exito")
        except Exception as ex:
            print('ERROR{}'.format(ex))
        return redirect(url_for('maestros.ABCompleto2'))
    return render_template('eliminarM.html', form=create_form)
    

@maestros.route("/ABCompleto2", methods=["GET", "POST"])
def ABCompleto2():
    create_form = forms.MaestrosForm(request.form)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call mostrarTodosMaestros()')
            resultset = cursor.fetchall()
            
        connection.commit()
        connection.close()
        
        # Convertir resultset a una lista de diccionarios
        maestros = []
        for row in resultset:
            maestro = {'idM':row[0],'nombreM': row[1], 'apellidosM': row[2], 'emailM': row[3]}
            maestros.append(maestro)
        
    except Exception as ex:
        print(ex)
        
    return render_template("ABCompleto2.html", form=create_form, maestros=maestros)


