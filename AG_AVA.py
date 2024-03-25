"""
Inteligência Artificial 2
Tópico: Algoritmo Genético em Ambiente Virtual de Aprendizagem

Autores:
- Luis André Vieira Alonso Loli
- Diego Alexandre da Silva
- Maisa Vale Moreira

•4°
Lista de exercício prático: Implementação do cruzamento em ponto único e
mutação, na linguagem de programação escolhida.
"""

import random
import csv
import os
import math

nome_arquivo = 'casos_teste.csv'  #Nome do arquivo

# Obtém o diretório do script atual
def abrir_arquivo(arquivo):
    diretorio_atual = os.path.dirname(__file__)
    caminho_arquivo = os.path.join(diretorio_atual, arquivo)
    return caminho_arquivo

def extrair_dados(endereco):
    dados_formatados = ()
  
    with open(endereco, newline='') as arquivo: #Endereco arquivo csv
        leitura_csv = csv.DictReader(arquivo)
        for linha in leitura_csv:
            matricula = linha["Matricula"]
            idade = linha["Idade"]
            disciplina = linha["Disciplina"]
            tempo_acesso = linha["Tempo de Acesso(minutos)"]
            hora_acesso = linha["Hora de Acesso"]

            matricula_int = int(matricula)
            idade_int = int(idade)
            disciplina_int = int(disciplina)
            tempo_acesso_int = int(tempo_acesso)
            hora_acesso_int = int(hora_acesso)

            novo_elemento = (matricula_int, idade_int, disciplina_int, tempo_acesso_int, hora_acesso_int)
            dados_formatados = (*dados_formatados, novo_elemento)
        return dados_formatados

def max_min(dados):
    parametros_populacao = ()
    comprimento_cromossomo = 0
    for i in range(len(dados)):
        for x in range(len(dados[0])):
            elemento = dados[i][x]      
            if i == 0:
                if x == 0:
                    matricula_max = elemento
                    matricula_min = elemento
                elif x == 1:
                    idade_max = elemento
                    idade_min = elemento
                    comprimento_cromossomo+=1
                elif x == 2:
                    disciplina_min = elemento
                    disciplina_max = elemento
                    comprimento_cromossomo+=1
                elif x == 3:    
                    tempo_acesso_min = elemento
                    tempo_acesso_max = elemento
                    comprimento_cromossomo+=1
                elif x == 4:    
                    hora_acesso_min = elemento
                    hora_acesso_max = elemento
                    comprimento_cromossomo+=1
            else:                   
                if x == 0:
                    if(elemento > matricula_max):
                            matricula_max = elemento
                    if(elemento < matricula_min):
                            matricula_min = elemento    
                elif x==1:    
                    if(elemento > idade_max):
                        idade_max = elemento
                    if(elemento < idade_min):
                        idade_min = elemento 
                elif x==2:    
                    if(elemento > disciplina_max):
                        disciplina_max = elemento
                    if(elemento < disciplina_min):
                        disciplina_min = elemento 
                elif x==3:    
                    if(elemento > tempo_acesso_max):
                        tempo_acesso_max = elemento
                    if(elemento < tempo_acesso_min):
                        tempo_acesso_min = elemento 
                else:   
                    if(elemento > hora_acesso_max):
                        hora_acesso_max = elemento
                    if(elemento < hora_acesso_min):
                        hora_acesso_min = elemento
    
    parametros_dict = {
        'tamanho_populacao': (len(dados)),
        'comprimento_cromossomo': (comprimento_cromossomo),
        'matricula': (matricula_min, matricula_max),
        'idade': (idade_min, idade_max),
        'disciplina': (disciplina_min, disciplina_max),
        'tempo_acesso': (tempo_acesso_min, tempo_acesso_max),
        'hora_acesso': (hora_acesso_min, hora_acesso_max)
    }

    return parametros_dict
    #print("Mínimo e máximo para a idade:", parametros_dict['idade'])   

def criar_populacao(tamanho_populacao, comprimento_cromossomo, limite_cromossomo ):
    populacao = []
    for y in range(tamanho_populacao):
        for x in range(comprimento_cromossomo):
          numero_aleatorio = random.randint(1, limite_cromossomo)
          populacao.append(numero_aleatorio)
    return populacao

def codificar_populacao(populacao):
    populacao_binaria = []
    for numero in populacao:
        numero_binario = bin(numero)
        formata_numero = numero_binario[2:] # retira_0b 
        preencher_zeros = formata_numero.zfill(4) # Tamanho max 8 bits
        populacao_binaria.append(preencher_zeros)
    return populacao_binaria

def decodificar_populacao(populacao):
    populacao_decimal = []
    for numero in populacao:
        decimal = int(numero, 2)
        populacao_decimal.append(decimal)
    return populacao_decimal

def normalizar(parametros_populacao, dados_teste):
    lista_normalizada = []
    lista_normalizada_conjunta = []

    tamanho_populacao = parametros_populacao['tamanho_populacao']
    comprimento_cromossomo = parametros_populacao['comprimento_cromossomo']

    dif_idade  = parametros_populacao['idade'][1] - parametros_populacao['idade'][0]
    dif_disciplina = parametros_populacao['disciplina'][1] - parametros_populacao['disciplina'][0]
    dif_tempo_acesso  = parametros_populacao['tempo_acesso'][1] - parametros_populacao['tempo_acesso'][0]
    dif_hora_acesso  = parametros_populacao['hora_acesso'][1] - parametros_populacao['hora_acesso'][0]

    for x in range(0, tamanho_populacao):
        for y in range(1, comprimento_cromossomo+1):
            if y == 1:
                valor_atual = dados_teste[x][y]
                menor_valor = parametros_populacao['idade'][0]
                normalizacao_idade = (valor_atual - menor_valor) / dif_idade   
                lista_normalizada.append(normalizacao_idade)
            elif y==2:
                valor_atual = dados_teste[x][y]
                menor_valor = parametros_populacao['disciplina'][0]
                normalizacao_disciplina = (valor_atual - menor_valor) / dif_disciplina      
                lista_normalizada.append(normalizacao_disciplina)
            elif y==3:
                valor_atual = dados_teste[x][y]
                menor_valor = parametros_populacao['tempo_acesso'][0]
                normalizacao_tempo_acesso = (valor_atual - menor_valor) / dif_tempo_acesso   
                lista_normalizada.append(normalizacao_tempo_acesso)
            elif y==4:
                valor_atual = dados_teste[x][y]
                menor_valor = parametros_populacao['hora_acesso'][0]
                normalizacao_hora_acesso = (valor_atual - menor_valor) / dif_hora_acesso  
                lista_normalizada.append(normalizacao_hora_acesso)

    lista_final = [lista_normalizada[i:i+4] for i in range(0, len(lista_normalizada), 4)]#lista_formatada
    return lista_final

def centroide(lista_normalizada):
    tamanho_lista = len(lista_normalizada)
    lista_centroide = []
    soma = 0.0
    calculo_centroide = 0.0
   
    for x in range(0, len(lista_normalizada[0])):
        for y in range(0, tamanho_lista ):
            soma = soma + lista_normalizada[y][x]  
        calculo_centroide = soma / len(lista_normalizada[0])
        lista_centroide.append(calculo_centroide)
        soma = 0.0

    return lista_centroide

def distancia_euclidiana(lista_normalizada, lista_centroide):
    lista_distancia_euclidiana = []
    distancia = 0.0
    sub_parcial = 0.0
    potencia = 0.0
    soma = 0.0
   
    for x in range(0, len(lista_normalizada)):
        for y in range (0, len(lista_centroide)):
            sub_parcial = lista_normalizada[x][y] - lista_centroide[y]
            potencia = sub_parcial * sub_parcial
            soma = soma + potencia  
        distancia = math.sqrt(soma)
        lista_distancia_euclidiana.append(distancia)
        soma = 0.0
    return lista_distancia_euclidiana  

def funcao_fitness(parametros_algoritmo, dados_formatado):

    lista_normalizada = normalizar(parametros_algoritmo, dados_formatado)
    lista_centroide = centroide(lista_normalizada)
    lista_euclidiana = distancia_euclidiana(lista_normalizada, lista_centroide)
    
    lista_fitness = []

    beta = 100

    for x in range(0, len(lista_euclidiana)):
        calculo_funcao = beta / (1 + lista_euclidiana [x] )
        lista_fitness.append(calculo_funcao) 
    return lista_fitness

def selecao_roleta(populacao_fitness):
    
    giro_roleta = 25
    
    lista_parcelada= []
    fitness_percentual = []
    selecao_parcial = []
    populacao_fitness.sort()
    #print("Valores ordenados em ordem crescente:", populacao_fitness)
    parcelada= 1
    media_limite = 0.0
    pares_individuos = 0.5
    indice = 0
    
    for x in range(1, len(populacao_fitness)):
        y = x-1
        media_limite = media_limite + (populacao_fitness[x] - populacao_fitness[y])    
    media_limite = media_limite / len(populacao_fitness)
    #print('Media_limite: ', media_limite)

    for x in range(1, len(populacao_fitness)):
        y = x-1
        if (populacao_fitness[x] - populacao_fitness[y]) <= media_limite:
            parcelada+=1  
        else:
           indice+=1
           lista_parcelada.append(parcelada)
           parcelada=1
        if(x == (len(populacao_fitness)-1)):
            lista_parcelada.append(parcelada)

    for x in range(len(lista_parcelada)):
        fitness_percentual.append((lista_parcelada[x] / len(populacao_fitness)) * 100)
    
    #print('fitness_percentual: ', fitness_percentual)
    soma = []
    numeros_sorteados = []
    giro_atual = 0
    roleta_gira = random.randint(0, (len(fitness_percentual)-1))
    numeros_sorteados.append(roleta_gira)
    soma.append(fitness_percentual[roleta_gira])
    
    while (sum(soma) < (sum(fitness_percentual)*pares_individuos)) and (giro_atual <= giro_roleta):
        giro_atual+=1
        while roleta_gira in numeros_sorteados:
            roleta_gira = random.randint(0, (len(fitness_percentual)-1))
        soma.append(fitness_percentual[roleta_gira])
        numeros_sorteados.append(roleta_gira)       
    numeros_sorteados.sort()
    #print(numeros_sorteados)
    #print(lista_parcelada)

    lista_concatenada = []
    indice_inicio = 0

    for tamanho in lista_parcelada:
        lista_concatenada.append(populacao_fitness[indice_inicio:indice_inicio+tamanho])
        indice_inicio += tamanho
    
    valores_selecionados = []
    for indice in numeros_sorteados:
        valores_selecionados.extend(lista_concatenada[indice])

    return valores_selecionados


def cruzamento_ponto_unico(pais):
    # Função para realizar o cruzamento de ponto único em um algoritmo genético
    # Pais: lista contendo dois indivíduos selecionados para reprodução
    
    pai = pais[0]
    mae = pais[1]

    print("Pai: ", pai)
    print("Mae: ", mae)

    comprimento_cromossomo = len(pai)
    
    # Definindo um ponto de corte aleatório dentro do cromossomo
    ponto_corte = random.randint(1, comprimento_cromossomo - 1)
    print('Ponto corte[inicio-direita]: ',ponto_corte)
    
    # Realizando o cruzamento de ponto único para gerar os dois filhos
    filho_1 = pai[:ponto_corte] + mae[ponto_corte:]
    filho_2 = mae[:ponto_corte] + pai[ponto_corte:]
    
    print("Filho 1:", filho_1)
    print("Filho 2:", filho_2)

    return (filho_1)

def mutacao(individuo, taxa_mutacao):
    # Convertendo a taxa de mutação para uma probabilidade entre 0 e 1
    taxa_mutacao = min(1, max(0, taxa_mutacao))
    print('Taxa Mutacao: ', taxa_mutacao)
    valor_aleatorio = 0
    # Realizando a mutação para cada gene do cromossomo
    cromossomo_mutado = ""
    for gene in individuo:
        valor_aleatorio = random.random()
        print('Valor Aleatorio Gene: ', valor_aleatorio)
        if  valor_aleatorio < taxa_mutacao:
            # Se a probabilidade de mutação for menor que a taxa de mutação,
            cromossomo_mutado += str(1 - int(gene))
        else:
            cromossomo_mutado += gene

    print('Individuo Original: ', individuo)
    print('Individuo Mutado: ',cromossomo_mutado)
    return cromossomo_mutado


def main():
    qnt_grupo = int(input('Informe a quantidade de grupos desejada: '))
    arquivo_csv = abrir_arquivo(nome_arquivo)
    #to do verificar arquivo correto ou fechar
    dados_formatado = extrair_dados(arquivo_csv)
    parametros_algoritmo = max_min(dados_formatado)
    tamanho_populacao = (parametros_algoritmo['tamanho_populacao'])
    comprimento_cromossomo = (parametros_algoritmo['comprimento_cromossomo'])
    
    populacao_criada = criar_populacao(tamanho_populacao, comprimento_cromossomo, qnt_grupo)
    populacao_binaria = codificar_populacao(populacao_criada)
    populacao_decimal = decodificar_populacao(populacao_binaria)
    print('Populacao criada: ', populacao_criada)
    print('Populacao binaria', populacao_binaria)
    #print("População decimal:", populacao_decimal)

    populacao_fitness = funcao_fitness(parametros_algoritmo, dados_formatado)
    #print('Valores Fitness: ', populacao_fitness)
    populacao_roleta = selecao_roleta(populacao_fitness)
    #print('Populacao Roleta:', populacao_roleta)
    populacao_teste_cruzamento = (populacao_binaria[0], populacao_binaria[1])
    print('---Cruzamento---')
    populacao_cruzamento = cruzamento_ponto_unico(populacao_teste_cruzamento)
    taxa_mutacao = 0.5
    print('---Mutação---')
    cromossomo_mutado = mutacao(populacao_cruzamento, taxa_mutacao)
    
if __name__ == "__main__":
    main()