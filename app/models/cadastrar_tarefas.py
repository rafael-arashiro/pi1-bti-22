from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired

class Cadastrar_tarefa(FlaskForm):
    tarefa = StringField("tarefa", validators=[DataRequired()])
    id_pessoa = SelectField("id_pessoa", validators=[DataRequired()])
    local = StringField("local")
    data = DateField("data", validators=[DataRequired()])
    hora = TimeField("hora")

class Apagar_tarefa(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
