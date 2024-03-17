from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class InputCodeForm(FlaskForm):
    inputCode = IntegerField('Поиск', validators=[DataRequired(), NumberRange(0, 3000)], default=0)
    submit = SubmitField('Проверить')