from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, NumberRange


class InputCodeAndKeyForm(FlaskForm):
    inputKey = StringField('Введите ключ: ', validators=[DataRequired()], default='')
    inputCode = IntegerField('Введите код: ', validators=[DataRequired(), NumberRange(0, 3000)], default=0)
    submit = SubmitField('Проверить')