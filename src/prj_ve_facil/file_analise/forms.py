from django import forms
from .models import Arquivos


class formArquivo(forms.ModelForm):
    nom_arquivo = forms.CharField(required=True, label="Nome do Arquivo")
    arquivo = forms.FileField(required=True, label="Procurar Arquivo")
    
    arquivo.widget.attrs.update({"class":"form-control"})
    nom_arquivo.widget.attrs.update({"class":"form-control"})
    
    class Meta:
        model = Arquivos
        fields = ['nom_arquivo','arquivo']
