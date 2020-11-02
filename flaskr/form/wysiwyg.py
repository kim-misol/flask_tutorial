from wtforms import fields, widgets


class Div(object):
    """
    div.
    """

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
