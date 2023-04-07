from django.shortcuts import render, redirect
from .forms import formArquivo

from django.http import JsonResponse, HttpRequest


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
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        print("ajax",is_ajax)
        caminho = get_file_path(arquivo)
        colunas_tipos = {}
    
        dataframe = pd.read_csv(caminho,sep = '[:,|;]',engine='python', index_col=False)
        
        
        colunas = list(dataframe.columns.values.tolist())
        linhas = len(dataframe.index)
        tipos = dataframe.dtypes.to_list()
        
        i = 0
        for tipo in tipos:
            tipos[i] = tipo
            i = i + 1
            
        for i in range(len(colunas)):
            colunas_tipos[colunas[i]] = tipos[i]
        
        if is_ajax:
            if request.method == 'GET':
                cols = request.GET.getlist("ls_col[]")
                agrupar = request.GET.getlist("ls_agrupar[]")

                dataframe = dataframe[cols]
                print(dataframe)
                al = []
                if len(agrupar):
                    for ag in agrupar:
                        al.append(ag)
                        if ag in cols:
                            dataframe = dataframe.groupby(al).count()
                
                tabela = dataframe.to_html()
                print(al)
                return JsonResponse(tabela, safe=False)
        # agrupar = []
        # if request.GET:
        #     agrupar = request.GET.getlist("ls_agrupar[]")
        #     cols = request.GET.getlist("ls_col[]")
        #     if len(cols):
        #         dataframe = dataframe[cols]
          
        
             
        # html_tabela = dataframe[(dataframe["continent"] == "Africa") & (dataframe["continent"] == "Asia")].head(10).to_html().encode('utf-8')

        # dataframe= dataframe[(dataframe["continent"] == "Africa") | (dataframe["continent"] == "Asia")]
    
        # if len(agrupar):
        #     dataframe = dataframe.groupby(agrupar).count()
        #     print("agrupou")
            
            
       
        
    except FileNotFoundError:
       print('Arquivo não encontrado')
       return redirect('index')
   
    dataframe = dataframe.head(1)
    html_tabela = return_html(dataframe)
  
    
    context = {
        'colunas': colunas_tipos,
        'linhas': linhas,
        'arquivo': arquivo,
        'caminho': caminho,
        'tabela': html_tabela
        
    }    
    
    return render(request, 'analise.html', context)


    


# Lista todos os arquivos que estão salvos no banco
def get_all_files():
    arquivos = Arquivos.objects.all()    
    
    return arquivos

def return_html(object_df):
    
    return object_df.to_html().encode('utf-8')
    
  
    
       
    

