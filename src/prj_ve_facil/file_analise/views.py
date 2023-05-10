from django.shortcuts import render, redirect
from .forms import formArquivo

from django.http import JsonResponse

import pandas as pd

from .models import Arquivos
from django.contrib import messages
import os
# Create your views here.

global dataframe

# Formulário para adicionar arquivos 
def frmAddArquivo(request):
    
    form = formArquivo()
    if request.method == "POST":
        arquivo = request.FILES['arquivo']
        if arquivo.name.endswith('.csv'):
            form = formArquivo(request.POST, request.FILES)
            if form.is_valid():
                
                form.save()
                messages.success(request,"Salvo com Sucesso!!!")   
   
        else:
            messages.warning(request,"A extensão do arquivo precisa ser '.CSV'")   
    
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

def analisar(request, arquivo,cod=1):
    
    try:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        print("ajax",is_ajax)
        tabela = ''

        caminho = get_file_path(arquivo)
        colunas_tipos = {}

        if cod == 1:
            dataframe = pd.read_csv(caminho,sep = '[:,|;]',engine='python')
        else:
            dataframe = pd.read_csv(caminho,sep = '[:,|;]',engine='python').head(30)

        
        colunas = ren_cols(dataframe)
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
                dataframe = dataframe[cols]
                param = request.GET.getlist("ls_param[]")
                query = ''
                print("Parametros", param)
                for i in range(len(param)) :
                
                    if param[i] != '' and i > 0 and i < len(param)-1:
                        query = query + ' ' + cols[i] + ' == "' + param[i] + '" &'
                    elif param[i] != '':
                        query = query + ' ' + cols[i] + ' == "' + param[i] + '" '
                        
                #     query = 'coluna1 =="parametro1" & coluna2 == "parametro2"' 
               
                # 10/05/2023 bug na manipulação de colunas, elas precisam 
                if len(query): 
                        dataframe = dataframe.query(query)
                        print("Qurey: ", query)
                        print("Dataframe: ", dataframe)   
                if cod == 1:
                    
                    agrupar = request.GET.getlist("ls_agrupar[]")
                    op = request.GET.get("sel_op")
                    cols_agrup = []
                    if len(agrupar):
                        for ag in agrupar:
                            if ag in cols:
                                cols_agrup.append(ag)
                        dataframe = executar_op(op, cols_agrup, dataframe)
                    
                         
                    tabela = dataframe.to_json()
                else:
                    tabela = dataframe.to_html()
                    
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
    
# pega arquivo
def get_file_2(request, arquivo):
    return analisar(request, arquivo, cod=1)

# efetua a leitura de um arquivo joga na tabela
def get_file(request, arquivo):
    return analisar(request,arquivo,cod=2)

# deleta referencias ao arquivo
def del_file(request,id):
  
    arquivo = Arquivos.objects.get(pk=id)
       
    try:
        try:
            caminho = get_file_path(arquivo)
            os.remove(caminho)
        except:
            print("Caminho não encontrado")
        
        finally:
            arquivo.delete()
       
    except:
        print("Metadados não existe")
        
 
    messages.info(request,"As referências ao arquivo foram deletadas!")

    return redirect("index")
  
# renomeia colunas e retorna novo dataframe com colunas renomeadas      
def ren_cols(dataframe):
    
    colunas = list(dataframe.columns.values.tolist())
    novo_nome = ''
    simbolos = [' ','(',')','.']
    for col in colunas:
        novo_nome = col
        for s in simbolos:
            if s in col:
                novo_nome = novo_nome.replace(s, '_')   
                    
        dataframe.rename(columns={col: novo_nome}, inplace = True)
    colunas = list(dataframe.columns.values.tolist())
    
    return colunas

# executar operações de agrupamento e devolver novo dataframe
def executar_op(op, cols_agrup, dataframe):
    
    if op == "contar":
        dataframe = dataframe.groupby(cols_agrup).count()
    elif op == "somar":
        dataframe = dataframe.groupby(cols_agrup).sum()
    elif op == "media":
        dataframe = dataframe.groupby(cols_agrup).mean()
    elif op == "desvio":
        dataframe = dataframe.groupby(cols_agrup).std()
    
    return dataframe

# Lista todos os arquivos que estão salvos no banco
def get_all_files():
    arquivos = Arquivos.objects.all()    
    
    return arquivos

def return_html(object_df):
    
    return object_df.to_html().encode('utf-8')
    
  
    
       
    

