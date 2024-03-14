"""
Inteligência Artificial 2
Tópico: Algoritmo Genético em Ambiente Virtual de Aprendizagem

Autores:
- André Vieira Alonso Loli
- Diego Alexandre da Silva
- Maisa Vale Moreira
"""

import random

# Parâmetros do algoritmo genético
tamanho_populacao = 5 # Tamanho da população
comprimento_cromossomo = 4 # Cromossomo: idade(11, 21), tópico de interesse(disciplina)(1, 4), tempo de acesso(0, 23), hora de acesso (8, 22)
limites_cromossomo = ( # Limites Superior e Inferior
                    (11, 21), 
                    (1, 4), 
                    (0, 90),
                    (8, 22),
                    )

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
        preencher_zeros = formata_numero.zfill(8) # Tamanho max 8 bits
        populacao_binaria.append(preencher_zeros)
    return populacao_binaria

def decodificar_populacao(populacao):
    populacao_decimal = []
    for numero in populacao:
        decimal = int(numero, 2)
        populacao_decimal.append(decimal)
    return populacao_decimal

qnt_grupo = int(input('Informe a quantidade de grupos desejada: '))
populacao_criada = criar_populacao(tamanho_populacao, comprimento_cromossomo, qnt_grupo)
populacao_binaria = codificar_populacao(populacao_criada)
populacao_decimal = decodificar_populacao(populacao_binaria)
print('Populacao criada: ', populacao_criada)
print('Populacao binaria', populacao_binaria)
print("População decimal:", populacao_decimal)