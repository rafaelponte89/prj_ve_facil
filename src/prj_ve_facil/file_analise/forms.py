from django import forms
from .models import Arquivos


class formArquivo(forms.ModelForm):
    nom_arquivo = forms.CharField(required=True)
    arquivo = forms.FileField(required=True)
    
    class Meta:
        model = Arquivos
        fields = ['nom_arquivo','arquivo']
