from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.Form):
    SEXO_CHOICES = (('M', 'Masculino'),
                    ('F', 'Femenino')
    )

    dni = forms.CharField(label='DNI', max_length=8)
    name = forms.CharField(label='Nombre', max_length=200, required=True)
    last_name = forms.CharField(label="Apellido", max_length=200, required=True)
    email = forms.EmailField(label='Email', required=True)
    address = forms.CharField(label="Dirección", widget=forms.Textarea)
    phone = forms.CharField(label='Teléfono', max_length=20)
    sexo = forms.ChoiceField(label='sexo', choices=SEXO_CHOICES)
    birthdate = forms.DateField(label='Fecha Nacimiento', input_formats=['%Y-%m-%d'], widget=DateInput())