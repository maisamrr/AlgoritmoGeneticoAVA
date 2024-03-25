import csv
import random
import os

# Parâmetros de geração
idade_faixa = (11, 21)
disciplina_faixa = (1, 4)
tempo_acesso_faixa = (0, 90) 
hora_acesso_faixa = (8, 22)
tamanho_populacao = 100

# Função para gerar dados aleatórios
def gerar_dados_aleatorios(matricula):
    idade = random.randint(idade_faixa[0], idade_faixa[1])
    disciplina = random.randint(disciplina_faixa[0], disciplina_faixa[1])
    tempo_acesso = random.randint(tempo_acesso_faixa[0], tempo_acesso_faixa[1])
    hora_acesso = random.randint(hora_acesso_faixa[0], hora_acesso_faixa[1])
    return [matricula, idade, disciplina, tempo_acesso, hora_acesso]

# Obtém o diretório do script atual
diretorio_atual = os.path.dirname(__file__)

# Gerar dados e escrever no arquivo CSV no diretório 
nome_arquivo = 'casos_teste.csv'  # Nome do arquivo
caminho_arquivo = os.path.join(diretorio_atual, nome_arquivo)
with open(caminho_arquivo, mode='w', newline='') as arquivo:
    writer = csv.writer(arquivo)
    writer.writerow(['Matricula', 'Idade', 'Disciplina', 'Tempo de Acesso(minutos)', 'Hora de Acesso'])
    for matricula in range(1, tamanho_populacao + 1):
        writer.writerow(gerar_dados_aleatorios(matricula))