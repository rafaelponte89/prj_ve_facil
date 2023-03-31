from django.db import models

# Create your models here.

class Arquivos(models.Model):
    nom_arquivo = models.CharField(max_length=200, blank=False, unique=True)
    arquivo = models.FileField(upload_to='csv')
    
    def __str__(self):
        
        return f'{self.nom_arquivo}'