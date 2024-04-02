from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired

class Apagar_pessoa(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])

class Apagar_tarefa(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])