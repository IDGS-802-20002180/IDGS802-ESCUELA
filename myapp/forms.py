from wtforms import Form
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    id=IntegerField('id')
    nombre=StringField('nombre')
    apellidos=StringField('apellidos')
    email=EmailField('correo')
    
class MaestrosForm(Form):
    idM=IntegerField('id')
    nombreM=StringField('nombre')
    apellidosM=StringField('apellidos')
    emailM=EmailField('correo')