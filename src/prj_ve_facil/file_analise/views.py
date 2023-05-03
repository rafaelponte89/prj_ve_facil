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

global dataframe

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

def get_file_2(request, arquivo):
    
    
    try:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        print("ajax",is_ajax)
        tabela = ''

        caminho = get_file_path(arquivo)
        colunas_tipos = {}
    
        dataframe = pd.read_csv(caminho,sep = '[:,|;]',engine='python')
        
        # dataframe_chart = dataframe.copy()
        
        # dataframe_chart["continent"] = pd.Series(list(range(len(dataframe_chart))))
        # print("dataframe_chart\n", type(dataframe_chart))
        
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
                op = request.GET.get("sel_op")
               
                dataframe = dataframe[cols]
               
                cols_agrup = []
                if len(agrupar):
                    for ag in agrupar:
                        if ag in cols:
                            cols_agrup.append(ag)
                    if op == "contar":
                        dataframe = dataframe.groupby(cols_agrup).count()
                    elif op == "somar":
                        dataframe = dataframe.groupby(cols_agrup).sum()
                    elif op == "media":
                        dataframe = dataframe.groupby(cols_agrup).mean()
                    elif op == "desvio":
                        dataframe = dataframe.groupby(cols_agrup).std()
                            
              
                tabela = dataframe.to_json()
                
                return JsonResponse(tabela, safe=False)
      
            
       
        
    except FileNotFoundError:
       print('Arquivo não encontrado')
       messages.warning(request,"Arquivo não encontrado no caminho!!!")
       return redirect('index')

  
    
    context = {
        'colunas': colunas_tipos,
        'linhas': linhas,
        'arquivo': arquivo,
        'caminho': caminho,
        'tabela': tabela
        
    }    
    
    return render(request, 'analise.html', context)

   

    
# efetua a leitura de um arquivo
def get_file(request, arquivo):
     
    try:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        print("ajax",is_ajax)

        caminho = get_file_path(arquivo)
        colunas_tipos = {}
    
        dataframe = pd.read_csv(caminho,sep = '[:,|;]',engine='python')
        linhas_totais = len(dataframe.index)
        dataframe = dataframe.head(30)
        
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
                op = request.GET.get("sel_op")
                
                dataframe = dataframe[cols]
               
                # cols_agrup = []
                # if len(agrupar):
                #     for ag in agrupar:
                #         if ag in cols:
                #             cols_agrup.append(ag)
                #     if op == "contar":
                #         dataframe = dataframe.groupby(cols_agrup).count()
                #     elif op == "somar":
                #         dataframe = dataframe.groupby(cols_agrup).sum()
                #     elif op == "media":
                #         dataframe = dataframe.groupby(cols_agrup).mean()
                #     elif op == "desvio":
                #         dataframe = dataframe.groupby(cols_agrup).std()
                            
                # print(dataframe)
                # print(type(dataframe))
                tabela_html = dataframe.to_html()
                print(tabela_html)
                # tabela = dataframe.to_json()
               
                return JsonResponse(tabela_html, safe=False)
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

  
    
    context = {
        'colunas': colunas_tipos,
        'linhas': linhas,
        'arquivo': arquivo,
        'caminho': caminho,
        'linhas_totais': linhas_totais
        
    }    
    
    return render(request, 'analise.html', context)


def transform(operacao):
    op, col = operacao.split("_")
    series = None
    if op == "contar":
        series = dataframe.groupby(col).value_counts()
    elif op == "somar":
        series = dataframe.groupby(col).sum()
    elif op == "media":
        series = dataframe.groupby(col).mean()
    elif op == "desvio":
        series = dataframe.groupby(col).std()
        
    return series

def transform_2(op, cols):
    
    if op == "contar":
        dataframe = dataframe.groupby(cols).value_counts()
    elif op == "somar":
        dataframe = dataframe.groupby(cols).sum()
    elif op == "media":
        dataframe = dataframe.groupby(cols).mean()
    elif op == "desvio":
        dataframe = dataframe.groupby(cols).std()
    print(dataframe)
    return dataframe

# Lista todos os arquivos que estão salvos no banco
def get_all_files():
    arquivos = Arquivos.objects.all()    
    
    return arquivos

def return_html(object_df):
    
    return object_df.to_html().encode('utf-8')
    
  
    
       
    

