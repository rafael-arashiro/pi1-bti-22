from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired

class Cadastrar_pessoa(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    telefone = IntegerField("telefone", validators=[DataRequired()])
    admin = BooleanField("admin")


class Cadastrar_tarefa(FlaskForm):
    tarefa = StringField("tarefa", validators=[DataRequired()])
    id_pessoa = IntegerField("id_pessoa", validators=[DataRequired()])
    data = DateField("data", validators=[DataRequired()])