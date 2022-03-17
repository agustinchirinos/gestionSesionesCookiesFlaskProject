import base64

from flask import render_template, request, redirect, url_for, make_response, session
from flask_login import login_user, logout_user, current_user, login_required

import app
from . import sesiones
from .forms import LoginForm,UsuarioForm
from .models import Usuario

@app.login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id)

@sesiones.route("/logoutsession/")
def logoutsession():
    logout_user()
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
    if current_user.is_authenticated:
        return redirect(url_for('sesiones.welcome'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usuario = Usuario.get_by_username(username)
        if usuario and usuario.check_password(password):
            login_user(usuario, form.recuerdame.data)
            return redirect(url_for('sesiones.welcome'))
    return render_template('loginsession.html', form=form)

@sesiones.route("/mostrarsession/", methods=["GET","POST"])
def mostrarsession():
    nombre = ""
    apellidos = ""
    if "nombre" in session.keys() and "apellidos" in session.keys():
        nombre = session["nombre"]
        apellidos = session["apellidos"]
    if request.method == "POST":
        session.clear()
    return render_template("mostrarsession.html",nombre=nombre,apellidos=apellidos)

@sesiones.route("/createsession/")
def createsession():
    session["nombre"] = "AGUSTIN"
    session["apellidos"] = "IGLESIAS"
    return render_template('createsession.html')

@sesiones.route("/mostrarcookie/", methods=["GET","POST"])
def mostrarcookie():
    if request.method == "POST":
        response = make_response(render_template('mostrarcookie.html'))
        response.delete_cookie("nombre")
        response.delete_cookie("apellidos")
        nombre=""
        apellidos=""
        return response
    else:
        nombre = request.cookies.get("nombre")
        apellidos = request.cookies.get("apellidos")
    return render_template("mostrarcookie.html",nombre=nombre,apellidos=apellidos)

@sesiones.route("/createcookie/", methods=["GET","POST"])
def createcookie():
    response = make_response(render_template('createcookie.html'))
    if request.method == "POST":
        response.set_cookie("nombre",request.form.get("nombre"))
        response.set_cookie("apellidos", request.form.get("apellidos"))
    return response

@sesiones.route("/xssreflejado/", methods=["GET","POST"])
def xssreflejado():
    if request.method == "POST":
        comentario = request.form.get("comentario")
        return comentario
    return render_template("xssreflejado.html")

@sesiones.route('/welcome/')
@login_required
def welcome():  # put application's code here
    # if not current_user.is_authenticated:
    #     return redirect(url_for('sesiones.loginsession'))
    return render_template('welcome.html')

@sesiones.route('/')
def index():  # put application's code here
    return render_template('index.html')

