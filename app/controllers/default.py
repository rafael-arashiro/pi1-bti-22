from app import app
from flask import render_template, flash, redirect, url_for, session
from app.models.formulario import Login
from app.models.cadastrar_pessoas import Cadastrar_pessoa, Apagar_pessoa
from app.models.cadastrar_tarefas import Cadastrar_tarefa, Apagar_tarefa
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='darkwhat16',
    database='pi_db'
)

@app.route("/", methods=["GET", "POST"])
def index():
    formulario = Login()
    return render_template("index.html", formulario=formulario)

@app.route("/login", methods=["GET", "POST"])
def login():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

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
        return redirect(url_for("index"))

    mydb.close()

    return render_template("index.html", formulario=formulario)


@app.route("/entrada")
def entrada():
    return render_template("entrada.html", nome=session['nome'])

@app.route("/cadastrar_pessoas")
def cadastrar_pessoas():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    cadastro_pessoa = Cadastrar_pessoa()
    apagar_pessoa = Apagar_pessoa()

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()

    mydb.close()

    return render_template("cadastrar_pessoas.html", nome=session['nome'], cadastro_pessoa=cadastro_pessoa, apagar_pessoa=apagar_pessoa, grupoPessoas=grupoPessoas)

@app.route("/cadastroPessoa", methods=["GET", "POST"])
def cadastroPessoa():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    cadastro_pessoa = Cadastrar_pessoa()

    nome = cadastro_pessoa.nome.data
    password = cadastro_pessoa.password.data
    telefone = cadastro_pessoa.telefone.data
    admin = cadastro_pessoa.admin.data

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO pessoas (Nome,Senha,Telefone,admin) VALUES ('{nome}','{password}',{telefone},{admin}) ON DUPLICATE KEY UPDATE Senha = '{password}', Telefone = {telefone}, admin = {admin}"

    my_cursor.execute(sql)
    mydb.commit()
    
    mydb.close()

    return cadastrar_pessoas()

@app.route("/apagarPessoa", methods=["GET", "POST"])
def apagarPessoa():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    apagar_pessoa = Apagar_pessoa()

    id = apagar_pessoa.id.data

    my_cursor = mydb.cursor()

    sql = f"DELETE FROM pessoas WHERE id={id}"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_pessoas()

@app.route("/cadastrar_tarefas")
def cadastrar_tarefas():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    cadastro_tarefa = Cadastrar_tarefa()

    cursor = mydb.cursor()
    cursor.execute("SELECT Nome FROM pessoas")
    listadenomes = cursor.fetchall()
    cadastro_tarefa.id_pessoa.choices = [(nomes, nomes) for nomes in listadenomes]

    apagar_tarefa = Apagar_tarefa()

    my_cursor_tarefas = mydb.cursor()
    my_cursor_tarefas.execute('SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, tarefas.data, tarefas.hora FROM tarefas INNER JOIN pessoas ON tarefas.id_pessoa=pessoas.id')

    grupoTarefas = my_cursor_tarefas.fetchall()

    mydb.close()

    return render_template("cadastrar_tarefas.html", nome=session['nome'], cadastro_tarefa=cadastro_tarefa, apagar_tarefa=apagar_tarefa, grupoTarefas=grupoTarefas)

@app.route("/cadastroTarefa", methods=["GET", "POST"])
def cadastroTarefa():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    cadastro_tarefa = Cadastrar_tarefa()

    tarefa = cadastro_tarefa.tarefa.data
    id_pessoa = cadastro_tarefa.id_pessoa.data
    local = cadastro_tarefa.local.data
    data = cadastro_tarefa.data.data
    hora = cadastro_tarefa.hora.data
    nome = id_pessoa[2:-3]

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO tarefas (tarefas,id_pessoa,local,data,hora) VALUES ('{tarefa}',(SELECT id FROM pessoas WHERE Nome = '{nome}'),'{local}','{data}','{hora}')"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/apagarTarefa", methods=["GET", "POST"])
def apagarTarefa():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    apagar_tarefa = Apagar_tarefa()

    id = apagar_tarefa.id.data

    my_cursor = mydb.cursor()

    sql = f"DELETE FROM tarefas WHERE id={id}"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()

    my_cursor_tarefas = mydb.cursor()
    my_cursor_tarefas.execute('SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, tarefas.data, tarefas.hora FROM tarefas INNER JOIN pessoas ON tarefas.id_pessoa=pessoas.id WHERE tarefa.data > CURDATE() AND tarefa.data < DATE_ADD(CURDATE(), INTERVAL 14 DAY)')

    grupoTarefas = my_cursor_tarefas.fetchall()

    mydb.close()

    
    return render_template("relatorio.html", nome=session['nome'], grupoPessoas=grupoPessoas, grupoTarefas=grupoTarefas)