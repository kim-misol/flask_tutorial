from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    widgets,
    fields,
    FormField,
    FileField,
    SelectField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Email address', validators=[DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Email address', validators=[DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Submit')
    # name = StringField('Name', validators=[DataRequired()])
    # nickname = StringField('Nickname', validators=[DataRequired()])


class Div:
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        return widgets.HTMLString(f'<div {widgets.html_params(name=field.name, **kwargs)}></div>')


class WysiwygWidget(Div):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' wysiwyg'
        else:
            kwargs.setdefault('class', 'wysiwyg')
        return super(WysiwygWidget, self).__call__(field, **kwargs)


class WysiwygField(fields.StringField):
    widget = WysiwygWidget()


class PostEditForm(FlaskForm):
    # SAVELIST = [
    #     ('save', u"Save"),
    #     ('draft', u"Save (Private)"),
    # ]
    title = StringField(u"Title")
    content = StringField(u"Content")
    submit = SubmitField('Submit')
    # content_preview = StringField(u"Content preview")
    # file = FileField("Attachment")
    # save_type = SelectField("Save As", choices=SAVELIST)


class PostCreateForm(FlaskForm):
    submit = SubmitField('Create New Post')
