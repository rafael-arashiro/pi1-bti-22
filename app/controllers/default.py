from app import app
from flask import render_template, flash, redirect, url_for, session
from app.models.formulario import Login
from app.models.cadastrar_pessoas import Cadastrar_pessoa, Apagar_pessoa
from app.models.cadastrar_tarefas import Cadastrar_tarefa, Apagar_tarefa, Alocar_pessoa
import mysql.connector

mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

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
            session['admin']=record[4]
            return redirect(url_for("entrada"))
    else:
        return redirect(url_for("index"))

    mydb.close()

    return render_template("index.html", formulario=formulario)


@app.route("/entrada")
def entrada():
    return render_template("entrada.html", nome=session['nome'], admin=session['admin'])

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

    my_cursor_associado = mydb.cursor()

    sql = f"DELETE FROM pessoas_tarefas WHERE pessoa_id={id}"

    my_cursor_associado.execute(sql)
    mydb.commit()

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

    pessoas_tarefas = Alocar_pessoa()
    
    cursor = mydb.cursor()
    cursor.execute("SELECT Nome FROM pessoas")
    listadenomes = cursor.fetchall()
    pessoas_tarefas.pessoa_id.choices = [(nomes, nomes) for nomes in listadenomes]

    my_cursor_pessoas_tarefas_dois = mydb.cursor()
    my_cursor_pessoas_tarefas_dois.execute("SELECT tarefas FROM tarefas")
    listadetarefas = my_cursor_pessoas_tarefas_dois.fetchall()
    pessoas_tarefas.tarefa_id.choices = [(tarefas, tarefas) for tarefas in listadetarefas]
    

    apagar_tarefa = Apagar_tarefa()

    my_cursor_tarefas = mydb.cursor()
    my_cursor_tarefas.execute('SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, tarefas.data, tarefas.hora FROM tarefas, pessoas INNER JOIN pessoas_tarefas WHERE tarefas.id=pessoas_tarefas.tarefa_id AND pessoas.id=pessoas_tarefas.pessoa_id ORDER BY id')

    grupoTarefas = my_cursor_tarefas.fetchall()

    mydb.close()

    return render_template("cadastrar_tarefas.html", nome=session['nome'], cadastro_tarefa=cadastro_tarefa, pessoas_tarefas=pessoas_tarefas, apagar_tarefa=apagar_tarefa, grupoTarefas=grupoTarefas)

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

    sql = f"INSERT INTO tarefas (tarefas,local,data,hora) VALUES ('{tarefa}','{local}','{data}','{hora}')"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/pessoaTarefa", methods=["GET", "POST"])
def pessoaTarefa():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    pessoas_tarefas = Alocar_pessoa()

    pessoa_id = pessoas_tarefas.pessoa_id.data
    tarefa_id = pessoas_tarefas.tarefa_id.data
    nome = pessoa_id[2:-3]
    tarefa = tarefa_id[2:-3]

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO pessoas_tarefas VALUES ((SELECT id FROM pessoas WHERE Nome = '{nome}'),(SELECT id FROM tarefas WHERE tarefas = '{tarefa}'))"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/apagarTarefa", methods=["GET", "POST"])
def apagarTarefa():

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    apagar_tarefa = Apagar_tarefa()

    id = apagar_tarefa.id.data

    my_cursor_associado = mydb.cursor()

    sql = f"DELETE FROM pessoas_tarefas WHERE tarefa_id={id}"

    my_cursor_associado.execute(sql)
    mydb.commit()

    my_cursor = mydb.cursor()

    sql = f"DELETE FROM tarefas WHERE id={id}"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():

    nome=session['nome']

    mydb = mysql.connector.connect(host='pi1bti22.mysql.pythonanywhere-services.com',user='pi1bti22',password='741258abc',database='pi1bti22$pi_db')

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()

    my_cursor_tarefas_admin = mydb.cursor()
    my_cursor_tarefas_admin.execute('SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, tarefas.data, tarefas.hora FROM tarefas, pessoas INNER JOIN pessoas_tarefas WHERE tarefas.id=pessoas_tarefas.tarefa_id AND pessoas.id=pessoas_tarefas.pessoa_id AND tarefas.data > CURDATE() AND tarefas.data < DATE_ADD(CURDATE(), INTERVAL 14 DAY)')

    grupoTarefasAdmin = my_cursor_tarefas_admin.fetchall()

    my_cursor_tarefas = mydb.cursor()
    sql = f"SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, tarefas.data, tarefas.hora FROM tarefas, pessoas INNER JOIN pessoas_tarefas WHERE tarefas.id=pessoas_tarefas.tarefa_id AND pessoas.id=pessoas_tarefas.pessoa_id AND pessoas.id=(SELECT id FROM pessoas WHERE Nome = '{nome}')"
    my_cursor_tarefas.execute(sql)

    grupoTarefas = my_cursor_tarefas.fetchall()

    mydb.close()

    
    return render_template("relatorio.html", nome=session['nome'], admin=session['admin'], grupoPessoas=grupoPessoas, grupoTarefasAdmin=grupoTarefasAdmin, grupoTarefas=grupoTarefas)