import pandas as pd
import random
import numpy as np
import pandas as pd
import random

# ETAPA 1 - GERAR POPULACAO

# Definir os parâmetros do problema
num_cromossomos = 100
num_alunos = 100
num_grupos = 5
pmut = 0.03

# 1. Gerar uma lista fixa de alunos
alunos = []
for i in range(num_alunos):
    aluno = {
        "Identificação": f"Aluno_{i+1}",
        "Grupo": None,
        "Idade": random.randint(17, 75),
        "Disciplina": random.randint(1, 4),
        "Tempo de Acesso": random.randint(0, 180),  
        "Hora de Acesso": random.randint(0, 23),
    }
    alunos.append(aluno)

# Inicializar os cromossomos
cromossomos = []
for _ in range(num_cromossomos):
    cromossomo = []
    
    # 2. Selecionar aleatoriamente os alunos para cada cromossomo
    random.shuffle(alunos)
    grupos_por_aluno = num_alunos // num_grupos
    for i, aluno in enumerate(alunos):
        aluno_com_grupo = aluno.copy()
        aluno_com_grupo["Grupo"] = (i // grupos_por_aluno) + 1
        cromossomo.append(aluno_com_grupo)
        
    cromossomos.append(cromossomo)

df_cromossomos = pd.DataFrame(cromossomos)

# Salvar dataframe para csv
df_cromossomos.to_csv('01_cromossomos.csv')
print("Cromossomos gerados e salvos em cromossomos.csv")

# ETAPA 2 - NORMALIZAR CARACTERISTICAS

def normalizar_caracteristicas(data):
    min_idade = float('inf')
    max_idade = float('-inf')
    min_disciplina = float('inf')
    max_disciplina = float('-inf')
    min_tempo_accesso = float('inf')
    max_tempo_accesso = float('-inf')
    min_hora = float('inf')
    max_hora = float('-inf')

    for cromossomo in data:
        for aluno in cromossomo:
            min_idade = min(min_idade, aluno["Idade"])
            max_idade = max(max_idade, aluno["Idade"])
            min_disciplina = min(min_disciplina, aluno["Disciplina"])
            max_disciplina = max(max_disciplina, aluno["Disciplina"])
            min_tempo_accesso = min(min_tempo_accesso, aluno["Tempo de Acesso"])
            max_tempo_accesso = max(max_tempo_accesso, aluno["Tempo de Acesso"])
            min_hora = min(min_hora, aluno["Hora de Acesso"])
            max_hora = max(max_hora, aluno["Hora de Acesso"])

    for cromossomo in data:
        for aluno in cromossomo:
            aluno["Idade"] = round((aluno["Idade"] - min_idade) / (max_idade - min_idade), 3)
            aluno["Disciplina"] = round((aluno["Disciplina"] - min_disciplina) / (max_disciplina - min_disciplina), 3)
            aluno["Tempo de Acesso"] = round((aluno["Tempo de Acesso"] - min_tempo_accesso) / (max_tempo_accesso - min_tempo_accesso), 3)
            aluno["Hora de Acesso"] = round((aluno["Hora de Acesso"] - min_hora) / (max_hora - min_hora), 3)

    return data

cromossomos = normalizar_caracteristicas(cromossomos)

df_cromossomos_normalizados = pd.DataFrame(cromossomos, columns=[f"Aluno_{i+1}" for i in range(num_alunos)])
df_cromossomos_normalizados.index.name = 'Cromossomo'

df_cromossomos_normalizados.to_csv('02_cromossomos_normalizados.csv')
print("Cromossomos normalizados gerados e salvos em cromossomos_normalizados.csv")

# ETAPA 3 - GERAR CENTROIDE DAS CARACTERISTICAS

def calcular_media_caracteristicas(data):
    medias = []

    for i, cromossomo in enumerate(data, start=1):
        for grupo in range(1, num_grupos + 1):
            grupo_dados = []

            for aluno in cromossomo:
                if aluno["Grupo"] == grupo:
                    grupo_dados.append(aluno)

            if len(grupo_dados) > 0:
                grupo_media = {
                    "Cromossomo": f"{i}",  
                    "Grupo": grupo,
                    "Média Idade": round(sum(aluno["Idade"] for aluno in grupo_dados) / len(grupo_dados), 3),
                    "Média Disciplina": round(sum(aluno["Disciplina"] for aluno in grupo_dados) / len(grupo_dados), 3),
                    "Média Tempo de Acesso": round(sum(aluno["Tempo de Acesso"] for aluno in grupo_dados) / len(grupo_dados), 3),
                    "Média Hora de Acesso": round(sum(aluno["Hora de Acesso"] for aluno in grupo_dados) / len(grupo_dados), 3)
                }
            else:
                grupo_media = {
                    "Cromossomo": f"{i}",  
                    "Grupo": grupo,
                    "Média Idade": 0,
                    "Média Disciplina": 0,
                    "Média Tempo de Acesso": 0,
                    "Média Hora de Acesso": 0
                }
            medias.append(grupo_media)

    return medias

medias_grupos_cromossomos = calcular_media_caracteristicas(cromossomos)

df_medias = pd.DataFrame(medias_grupos_cromossomos)
df_medias = df_medias[["Cromossomo", "Grupo", "Média Idade", "Média Disciplina", "Média Tempo de Acesso", "Média Hora de Acesso"]]

# ETAPA 3.1 - CALCULAR A DISTANCIA EUCLIDIANA ENTRE CARACTERISTICA DO ALUNO E O CENTROIDE DA CARACTERISTICA DE CADA GRUPO

for i, cromossomo in enumerate(cromossomos, start=1):
    for aluno in cromossomo:
        grupo_aluno = aluno["Grupo"]
        
        media_grupo = df_medias.loc[(df_medias['Cromossomo'] == str(i)) & (df_medias['Grupo'] == grupo_aluno)]
        
        for caracteristica in ["Idade", "Disciplina", "Tempo de Acesso", "Hora de Acesso"]:
            diferenca_absoluta = round(abs(aluno[caracteristica] - media_grupo[f"Média {caracteristica}"].values[0]), 3)
            aluno[caracteristica] = diferenca_absoluta

df_cromossomos_normalizados_atualizado = pd.DataFrame(cromossomos, columns=[f"Aluno_{i+1}" for i in range(num_alunos)])
df_cromossomos_normalizados_atualizado.index.name = 'Cromossomo'

df_cromossomos_normalizados_atualizado.to_csv('03_01_cromossomos_normalizados_atualizado.csv')
print("Cromossomos normalizados atualizados gerados e salvos em cromossomos_normalizados_atualizado.csv")

# ETAPA 3.2 - SOMAR DISTANCIAS E OBTER VALOR TOTAL DO CROMOSSOMO
def calcular_total_valor_cromossomo(data):
    aptidoes = []
    for i, cromossomo in enumerate(data, start=1):
        for aluno in cromossomo:
            aptidao = sum(aluno[caracteristica] for caracteristica in ["Idade", "Disciplina", "Tempo de Acesso", "Hora de Acesso"])
            aptidoes.append({"Cromossomo": f"{i}", "Aptidão": aptidao})
    return aptidoes

aptidoes_cromossomos = calcular_total_valor_cromossomo(cromossomos)

df_aptidao = pd.DataFrame(aptidoes_cromossomos)
df_aptidao = df_aptidao.groupby('Cromossomo').sum().reset_index()
df_aptidao.to_csv('03_02_aptidao_cromossomos.csv', index=False)
print("Aptidão dos cromossomos calculada e salva em aptidao_cromossomos.csv")

# ETAPA 3.3 - APLICAR A FUNCAO DE FITNESS DO ARTIGO
def calcular_fitness(df_aptidao):
    df_aptidao['Fitness'] = 100 / (1 + df_aptidao['Aptidão'])
    return df_aptidao

df_aptidao = calcular_fitness(df_aptidao)
df_aptidao.to_csv('03_03_aptidao_cromossomos_com_fitness.csv', index=False)
print("Aptidão dos cromossomos com função de fitness calculada e salva em aptidao_cromossomos_com_fitness.csv")

# ETAPA 4 - ROULETTE WHEEL SELECTION

def selecao_roleta(df_aptidao, num_selecionados):
    df_aptidao['Probabilidade'] = df_aptidao['Fitness'] / df_aptidao['Fitness'].sum()

    selecionados = []
    for _ in range(num_selecionados):
        ponto = random.random()
        acumulado = 0
        for cromossomo, prob in df_aptidao[['Cromossomo', 'Probabilidade']].values:
            acumulado += prob
            if acumulado >= ponto:
                selecionados.append(int(cromossomo))  # Convertendo para inteiro aqui
                break

    return selecionados

num_cromossomos_selecionados = 10

cromossomos_selecionados = selecao_roleta(df_aptidao, num_cromossomos_selecionados)
print("Cromossomos selecionados: ", cromossomos_selecionados)

# Filtrar o DataFrame df_cromossomos_normalizados_atualizado
df_cromossomos_selecionados = df_cromossomos_normalizados_atualizado[df_cromossomos_normalizados_atualizado.index.isin(cromossomos_selecionados)]

# Salvando o novo DataFrame em um arquivo CSV
df_cromossomos_selecionados.to_csv('04_cromossomos_selecionados.csv', index=True)
print("Cromossomos selecionados salvos em cromossomos_selecionados.csv")

# Criar um novo DataFrame com apenas as colunas 'Identificação' e 'Grupo' de cada aluno
df_identificacao_grupo = df_cromossomos_selecionados.applymap(lambda x: {'Identificação': x['Identificação'], 'Grupo': x['Grupo']})

# Salvar o novo DataFrame em um arquivo CSV
df_identificacao_grupo.to_csv('04_identificacao_grupo_alunos.csv', index=True)
print("Identificação e grupo dos alunos salvos em identificacao_grupo_alunos.csv")

# ETAPA 5 - CRUZAMENTO

def cruzamento_cromossomos(df_identificacao_grupo, mask):
    num_cromossomos = len(df_identificacao_grupo)

    # Inicializar lista para armazenar os filhos
    filhos = []

    # Iterar sobre pares de pais
    for i in range(0, num_cromossomos, 2):
        pai1 = df_identificacao_grupo.iloc[i]
        pai2 = df_identificacao_grupo.iloc[i + 1]

        # Inicializar os filhos com as mesmas identificações dos pais
        filho1 = pai1.copy()
        filho2 = pai2.copy()

        # Aplicar a regra de cruzamento para cada posição do cromossomo
        for j, bit in enumerate(mask):
            if bit == 0:
                filho1[j]['Grupo'] = pai1[j]['Grupo']
                filho2[j]['Grupo'] = pai2[j]['Grupo']
            else:
                filho1[j]['Grupo'] = pai2[j]['Grupo']
                filho2[j]['Grupo'] = pai1[j]['Grupo']

        # Adicionar os filhos à lista
        filhos.extend([filho1, filho2])

    return filhos[:num_cromossomos]

# Máscara de cruzamento - vamos assumir que é uma lista de 0s e 1s com o mesmo comprimento que o cromossomo
mask = [random.randint(0, 1) for _ in range(len(df_identificacao_grupo.columns))]

# Realizar o cruzamento
filhos = cruzamento_cromossomos(df_identificacao_grupo, mask)

# Criar um DataFrame com os filhos
df_filhos = pd.DataFrame(filhos)

# Mostrar o resultado
df_filhos.to_csv('05_resultado_cruzamento.csv', index=True)
print("Resultado do cruzamento salvo em 05_resultado_cruzamento.csv")

# ETAPA 6 - MUTACAO

def mutacao(df_filhos, pmut):
    for index, row in df_filhos.iterrows():
        for i, aluno in enumerate(row):
            if random.random() < pmut:  # Verifica se a mutação ocorrerá para este aluno
                grupo_atual = aluno['Grupo']
                novo_grupo = grupo_atual
                while novo_grupo == grupo_atual:
                    novo_grupo = random.randint(1, num_grupos)  # Gera um novo grupo diferente do grupo atual
                df_filhos.at[index, f'Aluno_{i+1}']['Grupo'] = novo_grupo  # Atualiza o grupo mutado
    return df_filhos

# Aplicar mutação nos filhos
df_filhos_mutados = mutacao(df_filhos, pmut)

# Salvar o DataFrame com os filhos mutados em um arquivo CSV
df_filhos_mutados.to_csv('06_filhos_mutados.csv', index=True)
print("Filhos com mutação aplicada salvos em 06_filhos_mutados.csv")