from django import forms

class Uploadfileform(forms.Form):
    file = forms.FileField(required=False)