from django.shortcuts import render, redirect
from .forms import formArquivo


import pandas as pd
import numpy as np
from .models import Arquivos
from django.contrib import messages
from bs4 import BeautifulSoup
import html.parser
# Create your views here.

# Formulário para adicionar arquivos 
def frmAddArquivo(request):
    if request.method == "POST":
        arquivo = request.FILES['arquivo']
        if arquivo.name.endswith('.csv'):
            form = formArquivo(request.POST, request.FILES)
            if form.is_valid():
                form.save()      
    else:
    
       
        form = formArquivo()
        
    return form
    
def index(request):
    
    form = frmAddArquivo(request)
    arquivos = get_all_files()

    context = {
        'form':form,
        'arquivos': arquivos
    }
    return render(request, 'index.html',context)

# retorna o caminho do arquivo dado o nome
def get_file_path(name_arquivo):
    arquivo = Arquivos.objects.get(nom_arquivo=name_arquivo)
    
    return arquivo.arquivo.path
    
# efetua a leitura de um arquivo
def get_file(request, arquivo):
   
    global dataframe
     
    try:
        caminho = get_file_path(arquivo)
        colunas_tipos = {}
    
        dataframe = pd.read_csv(caminho,sep = '[:,|_;]',engine='python')
        
        colunas = list(dataframe.columns.values.tolist())
        linhas = len(dataframe.index)
        
        tipos = dataframe.dtypes.to_list()
        # print(dataframe)
        i = 0
        # print(colunas)
        for tipo in tipos:
            if tipo == 'int64':
                tipos[i] = 'Número Inteiro'
            elif tipo == 'object':
                tipos[i] = 'Objeto'
            elif tipo == 'float64':
                tipos[i] = 'Número Decimal'
                
            i = i + 1
        for i in range(len(colunas)):
            colunas_tipos[colunas[i]] = tipos[i]
        
        # print(colunas_tipos)
       
    except FileNotFoundError:
       print('Arquivo não encontrado')
       return redirect('index')
   
    outra = []
    # for i in range(linhas):
    #     outra.append(dataframe.loc[i].to_list())    
        
    # for l in outra:
    #     print(l)
    html_tabela = dataframe.head(10).to_html().encode('utf-8')
   

    context = {
        'colunas': colunas_tipos,
        'linhas': linhas,
        'arquivo': arquivo,
        'caminho': caminho,
        'tabela': html_tabela
    }
    # dados = dataframe.to_numpy()
    # print(dataframe[["codigo.1","ocorrencia2"]].value_counts())
    # print(dataframe.head(10))
    
    
  
   
    
    return render(request, 'analise.html', context)

# Lista todos os arquivos que estão salvos no banco
def get_all_files():
    arquivos = Arquivos.objects.all()    
    
    return arquivos
    
  
    
       
    

