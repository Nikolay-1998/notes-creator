from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANET"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)
db = SQL("sqlite:///database.db")

@app.route("/")
def index():
    if not session.get("correo"):
        return redirect("/login")
    return render_template("menu.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        correo=request.form.get("correo")
        contra=request.form.get("contra")
        usuarios = db.execute("SELECT correo, contra FROM usuarios WHERE correo = ? ", correo)
        #comparar el pasword, contra el guardado, contra el que ingrese el usuario
        #si la contraseña coincide se redireciona a index.html, sino al login
        #creacion de usuario donde este se puedan registrar
        #encryptar la contraseña con un hash
        #implementar eliminar - ok
        #planear la presentasion de forma organizada
        #presentar un power point del total de la exposisición
        #pw_hash = generate_password_hash(contra)
        if len(usuarios) == 1 and check_password_hash(usuarios[0]["contra"],contra):
            session["correo"] = correo
            return redirect("/")
        else:
            return render_template("login.html", message= "The user dosen't exist or the password is incorrect")
    return render_template("login.html")


@app.route("/notas", methods=["GET","POST"])
def notas():
    if not session.get("correo"):
        return redirect("/login")
    if request.method == "POST":
        nota=request.form.get("nota")
        db.execute("INSERT INTO Notas (correo,nota) VALUES (?,?)", session.get("correo"), nota)
    notas = db.execute("SELECT id,nota FROM notas WHERE correo = ? ", session.get("correo"))
    return render_template("notas.html",notas=notas)

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not session.get("correo"):
        return redirect("/login")
    if request.method == "POST":
        nota_id=request.form.get("nota_id")
        db.execute("DELETE FROM notas WHERE id = ?",nota_id)
    notas = db.execute("SELECT id,nota FROM notas WHERE correo = ? ", session.get("correo"))
    return redirect("/notas")

#modificar la base de datos para crear un id unico que se utilize para eliminar o editar la nota
#layout, paguinas, para vincular a flask
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        correo=request.form.get("correo")
        contra=request.form.get("contra")
        contra_copia=request.form.get("contra_copia")
        if contra != contra_copia:
            return render_template("registro.html",message="La contraseña no coincide")
        usuarios = db.execute("SELECT correo FROM usuarios WHERE correo = ? ", correo)
        if len(usuarios) == 0:
            pw_hash = generate_password_hash(contra)
            db.execute("INSERT INTO  usuarios(correo,contra) values(?,?)",correo,pw_hash)
        else:
            return render_template("registro.html", message="Ya existe ese usuario")
        return redirect("/")
    else:
        return render_template("registro.html")

@app.route("/logout")
def logout():
    session["correo"] = None
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)