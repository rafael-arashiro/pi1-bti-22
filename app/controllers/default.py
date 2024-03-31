from app import app
from flask import render_template, flash, redirect, url_for, session
from app import mydb
from app.models.formulario import Login
from app.models.cadastrar import Cadastrar_pessoa, Cadastrar_tarefa
from app.models.apagar import Apagar_pessoa, Apagar_tarefa

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
            session['nome']=record[1]
            return redirect(url_for("entrada"))
    else:
        flash("Nome invalido")
    return render_template("index.html", formulario=formulario)


@app.route("/entrada")
def entrada():
    return render_template("entrada.html", nome=session['nome'])

@app.route("/cadastrar")
def cadastrar():
    cadastro_pessoa = Cadastrar_pessoa()
    cadastro_tarefa = Cadastrar_tarefa()

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()
    my_cursor.close()

    my_cursor_tarefas = mydb.cursor()
    my_cursor_tarefas.execute('SELECT * FROM tarefas')

    grupoTarefas = my_cursor_tarefas.fetchall()
    my_cursor_tarefas.close()

    return render_template("cadastrar.html", nome=session['nome'], cadastro_pessoa=cadastro_pessoa, cadastro_tarefa=cadastro_tarefa, grupoPessoas=grupoPessoas, grupoTarefas=grupoTarefas)

@app.route("/cadastroPessoa", methods=["GET", "POST"])
def cadastroPessoa():
    cadastro_pessoa = Cadastrar_pessoa()

    nome = cadastro_pessoa.nome.data
    password = cadastro_pessoa.password.data
    telefone = cadastro_pessoa.telefone.data
    admin = cadastro_pessoa.admin.data

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO pessoas (Nome,Senha,Telefone,admin) VALUES ('{nome}','{password}',{telefone},{admin})"

    my_cursor.execute(sql)
    mydb.commit()

    return cadastrar()

@app.route("/cadastroTarefa", methods=["GET", "POST"])
def cadastroTarefa():
    cadastro_tarefa = Cadastrar_tarefa()

    tarefa = cadastro_tarefa.tarefa.data
    id_pessoa = cadastro_tarefa.id_pessoa.data
    data = cadastro_tarefa.data.data

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO tarefas (tarefas,id_pessoa,data) VALUES ('{tarefa}','{id_pessoa}','{data}')"

    my_cursor.execute(sql)
    mydb.commit()

    return cadastrar()

@app.route("/apagar")
def apagar():
    apagar_pessoa = Apagar_pessoa()
    apagar_tarefa = Apagar_tarefa()

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()
    my_cursor.close()

    my_cursor_tarefas = mydb.cursor()
    my_cursor_tarefas.execute('SELECT * FROM tarefas')

    grupoTarefas = my_cursor_tarefas.fetchall()
    my_cursor_tarefas.close()

    return render_template("apagar.html", nome=session['nome'], apagar_pessoa=apagar_pessoa, apagar_tarefa=apagar_tarefa, grupoPessoas=grupoPessoas, grupoTarefas=grupoTarefas)

@app.route("/apagarPessoa", methods=["GET", "POST"])
def apagarPessoa():
    apagar_pessoa = Apagar_pessoa()

    id = apagar_pessoa.id.data
 
    my_cursor = mydb.cursor()

    sql = f"DELETE FROM pessoas WHERE id={id}"

    my_cursor.execute(sql)
    mydb.commit()

    return apagar()

@app.route("/apagarTarefa", methods=["GET", "POST"])
def apagarTarefa():
    apagar_tarefa = Apagar_tarefa()

    id = apagar_tarefa.id.data
    
    my_cursor = mydb.cursor()

    sql = f"DELETE FROM tarefas WHERE id={id}"

    my_cursor.execute(sql)
    mydb.commit()

    return apagar()

@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()
    my_cursor.close()

    my_cursor_tarefas = mydb.cursor()
    my_cursor_tarefas.execute('SELECT * FROM tarefas WHERE data > CURDATE() AND data < DATE_ADD(CURDATE(), INTERVAL 14 DAY)')

    grupoTarefas = my_cursor_tarefas.fetchall()
    my_cursor_tarefas.close()

    
    return render_template("relatorio.html", nome=session['nome'], grupoPessoas=grupoPessoas, grupoTarefas=grupoTarefas)