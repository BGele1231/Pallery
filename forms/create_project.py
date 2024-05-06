from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    image_url = StringField("Ссылка на фото")
    annotation = TextAreaField("Аннотация")
    docs_url = StringField("Ссылка на документ")
    submit = SubmitField('Опубликовать')
