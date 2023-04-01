from django.shortcuts import render, redirect
from .forms import formArquivo


import pandas as pd
import numpy as np
from .models import Arquivos
from django.contrib import messages
from bs4 import BeautifulSoup
import html.parser
# Create your views here.

# def set_cols(request, cols):
   
#     valor = request.GET["form"]
#     print(cols)
#     return index(request)

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

def drop_cols(cols):
    for col in cols:
        if col not in cols:
            dataframe.drop(col)
    
    print(dataframe.head(5))
    
# efetua a leitura de um arquivo
def get_file(request, arquivo):
   
    global dataframe
  
    
    try:
        caminho = get_file_path(arquivo)
        colunas_tipos = {}
    
        dataframe = pd.read_csv(caminho,sep = '[:,|;]',engine='python')
        
       
        
        colunas = list(dataframe.columns.values.tolist())
        linhas = len(dataframe.index)
        tipos = dataframe.dtypes.to_list()
        
        i = 0
        for tipo in tipos:
            tipos[i] = tipo
            i = i + 1
            
        for i in range(len(colunas)):
            colunas_tipos[colunas[i]] = tipos[i]
       
        if request.POST:
            for col in colunas_tipos.keys():
                if col not in request.POST:
                    dataframe = dataframe.drop(columns=[col])
            
             
        html_tabela = dataframe.head(10).to_html().encode('utf-8')
        json_tabela = dataframe.head(5).to_json()
        
    except FileNotFoundError:
       print('Arquivo não encontrado')
       return redirect('index')
    

    context = {
        'colunas': colunas_tipos,
        'linhas': linhas,
        'arquivo': arquivo,
        'caminho': caminho,
        'tabela': html_tabela,
        'jtabela': json_tabela
    }
    
    # print(json_tabela)
    
    
    return render(request, 'analise.html', context)

# Lista todos os arquivos que estão salvos no banco
def get_all_files():
    arquivos = Arquivos.objects.all()    
    
    return arquivos
    
  
    
       
    

