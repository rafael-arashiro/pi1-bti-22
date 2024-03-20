from app import app
from flask import render_template, flash, redirect, url_for, session
from app import mydb
from app.models.formulario import Login

@app.route("/", methods=["GET", "POST"])
def index():
    formulario = Login()
    return render_template("index.html", formulario=formulario)

@app.route("/login", methods=["GET", "POST"])
def login():
    formulario = Login()
    my_cursor = mydb.cursor()

    if formulario.validate_on_submit():
        nome = formulario.nome.data
        password = formulario.password.data
        my_cursor.execute('SELECT * FROM pessoas WHERE Nome=%s AND Senha=%s', (nome, password))
        record = my_cursor.fetchone()
        if record:
            session['loggedin']=True
            session['username']=record[1]
            return redirect(url_for("entrada"))
    else:
        flash("Nome invalido")
    return render_template("index.html", formulario=formulario)


@app.route("/entrada")
def entrada():
    return render_template("entrada.html", nome=session['nome'])

@app.route("/cadastrar")
def cadastar():

    return render_template("cadastrar.html")

@app.route("/relatorio")
def relatorio():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT Nome, Senha FROM pessoas')

    grupoPessoas = my_cursor.fetchall()
    
    lista = list()

    for usuario in grupoPessoas:
        lista.append(
            {
                'Nome': usuario[0],
                'Senha': usuario[1]
                }
                )
    return render_template("relatorio.html")