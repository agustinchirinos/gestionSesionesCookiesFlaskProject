import base64

from flask import render_template, request, redirect, url_for, make_response, session
from flask_login import login_user, logout_user, current_user

import app
from . import sesiones
from .forms import LoginForm,UsuarioForm
from .models import Usuario


@sesiones.route("/logoutsession/")
def logoutsession():
    return redirect(url_for('sesiones.index'))

@sesiones.route("/registrar/", methods=["get","post"])
def registrar():
    error = ""
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        try:
            usuario = Usuario()
            usuario.username = form.username.data
            usuario.set_password(form.password.data)
            usuario.dni = form.dni.data
            usuario.nombre = form.nombre.data
            usuario.apellidos = form.apellidos.data
            usuario.create()
            return redirect(url_for("sesiones.loginsession"))
        except Exception as e:
            return render_template("registrar.html", form=form, error=e.__str__())
    return render_template("registrar.html", form=form, error=error)

@sesiones.route("/loginsession/", methods=["GET","POST"])
def loginsession():
    form = LoginForm(request.form)
    return render_template('loginsession.html', form=form)

@sesiones.route("/mostrarsession/")
def mostrarsession():
    nombre = ""
    apellidos = ""
    return render_template("mostrarsession.html",nombre=nombre,apellidos=apellidos)

@sesiones.route("/createsession/")
def createsession():
    return render_template('createsession.html')

@sesiones.route("/mostrarcookie/")
def mostrarcookie():
    nombre = ""
    apellidos = ""
    return render_template("mostrarcookie.html",nombre=nombre,apellidos=apellidos)

@sesiones.route("/createcookie/")
def createcookie():
    response = make_response(render_template('createcookie.html'))
    return response

@sesiones.route("/xssreflejado/", methods=["GET","POST"])
def xssreflejado():
    if request.method == "POST":
        comentario = request.form.get("comentario")
        return comentario
    return render_template("xssreflejado.html")

@sesiones.route('/welcome/')
def welcome():  # put application's code here
    return render_template('welcome.html')

@sesiones.route('/')
def index():  # put application's code here
    return render_template('index.html')

