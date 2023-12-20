#CRIAR EXERCICIOS
    #SERIES POR EXERCICO (CARGA, REPETIÇÕES)
#LISTAR EXERCICIOS
from PySimpleGUI import PySimpleGUI as sg
import mysql.connector
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

caminho_imagem = 'imagem_redimensionada.png'

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='8j3L1PCmnbAQa4UTkhg8',
    database='build'
)

cursor = conexao.cursor()
musculos = ['Peitoral', 'Costas', 'Quadriceps' ,'Posterior', 'Ombros', 'Tricéps','Bicéps', 'Abdominais', 'Panturilhas',]
      
def obter_nome_do_exercicio(id_exercicio):
    # Consulta o banco de dados para obter o ID do exercício pelo nome
    comando = f"SELECT nome FROM exercicio WHERE ExercicioID = '{id_exercicio}'"
    cursor.execute(comando)
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]  # Retorna o ID do exercício
    else:
        return None  # Retorna None se o exercício não for encontrado

def addSet():
    #SELECIONAR TODOS OS EXERCICIOS
    comando = f"SELECT nome FROM exercicio"
    cursor.execute(comando)
    resultados = cursor.fetchall()


    nome_exer = [resultado[0] for resultado in resultados]
    layout = [
        [sg.Text('Informe o exercício:'), sg.Combo(nome_exer, key='-NOME-', size=(15,8))],
        [sg.Text('Informe quantas séries você realizou neste exercício:'), sg.InputText(key='-SERIES-')],
        [sg.Text('Escolha a data que foi executada:'), sg.InputText(key='-DATA-', enable_events=True), sg.CalendarButton('Calendário', target='-DATA-', format='%Y-%m-%d')],
        [sg.Button('OK')]
    ]

    window = sg.Window('Criar Exercício', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'OK':
            name = values['-NOME-']
            series = values['-SERIES-']
            dia = values['-DATA-']

            #SELECIONAR O EXERCICIOID DA TABELA EXERCICIO QUANDO O NOME = {VAR_NOME} fazer um def novo?
            comando = f"SELECT ExercicioID FROM exercicio WHERE Nome = '{name}'"
            cursor.execute(comando)
            ExercicioID = cursor.fetchall()[0][0]
            
            #LOOP de execução para cada séries da {VAR_SERIES}
            for n in range(1, int(series) + 1):
                carga = sg.popup_get_text(f'Informe a carga na {n}ª série:')
                repeticao = sg.popup_get_text(f'Informe a quantidade de repetições na {n}ª série:')

                 #inserir na tabela series, o Exercicio ID, Reps, Peso, Dia
                comando = f'INSERT INTO series (ExercicioID, Reps, Peso, dia) VALUES ("{ExercicioID}", {repeticao}, {carga},"{dia}")'
                cursor.execute(comando)
                conexao.commit()
            
            sg.popup('Exercício listado com sucesso!', title='Aviso')

            window.close()
            break

    window.close()         
def delExer():
    # Deletar dados da tabela 'treino' que referenciam a tabela 'exercicio'
    comando = f'DELETE FROM treino'
    cursor.execute(comando)
    conexao.commit()

    # Deletar dados da tabela 'exercicio'
    comando = f'DELETE FROM exercicio'
    cursor.execute(comando)
    conexao.commit()

    # Deletar dados da tabela 'series'
    comando = f'DELETE FROM series'
    cursor.execute(comando)
    conexao.commit()

    sg.popup('Exercício deletado com sucesso!', title='Aviso')
def listarExer():
    # Selecionar apenas o nome da tabela exercicio
    comando = 'SELECT Nome FROM exercicio'
    cursor.execute(comando)
    exercicios = cursor.fetchall()
    #Listar um a um os exercicios
    exercise_info = '\n'.join([exercicio[0] for exercicio in exercicios])
    
  
    

    # Criar a janela de listagem
    layout = [
        
        [sg.Multiline(exercise_info, size=(40, 10), disabled=True)],
        
        [sg.Text('Informe o nome do exercício:'), sg.InputText(key='-NOME-', size=(8,8))],
        [sg.Text('Selecione o músculo alvo:'), sg.Combo(musculos, key='-MUSCULO-', size=(8,8))],
        [sg.Button('Adicionar Exércicio'), ]
    ]

    window = sg.Window('Lista de Exercícios', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        #VERIFICAÇÃO PARA VE SE OS CAMPOS ESTÃO PREENCHIDOS
        elif event == 'Adicionar Exércicio' and values['-NOME-'].strip() != '' and values['-MUSCULO-'].strip() != '':
            nome = values['-NOME-']
            target = values['-MUSCULO-']
            comando = f'INSERT INTO exercicio (nome, target) VALUES ("{nome}","{target}")'
            cursor.execute(comando)
            conexao.commit()
            window.close()
            listarExer()
        elif values['-NOME-'].strip() == '' or values['-MUSCULO-'].strip() == '':
            sg.popup('INFORME TODOS OS CAMPOS!')
            
    window.close()  
def setofmuscle():
    target_inf = ''
    for x in musculos:
        target_inf += f'{x}\n'
        comando = f"SELECT series FROM exercicio WHERE target = '{x}'"
        cursor.execute(comando)
        target = cursor.fetchall()
        valor = 0
        for tar in target:
            valor += tar[0]
        target_inf += f'{valor}\n'
        
    layout = [
    [sg.Text('Séries por musculo')],
    [sg.Multiline(target_inf, size=(40, 10), disabled=True)]
    ]

    window = sg.Window('Séries por musculo', layout, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
    


         
        
    
  #PAINEL
def history():
    comando = f'SELECT DISTINCT nome, ExercicioID FROM exercicio'
    cursor.execute(comando)
    resultados = cursor.fetchall()

    lista_musculos = [resultado[0] for resultado in resultados]
    mapeamento_exercicio_id = {resultado[0]: resultado[1] for resultado in resultados}
    

    layout = [
        [sg.Text('Selecione o músculo para ver o histórico:'), sg.Combo(lista_musculos, key='-MUSCULO-', size=(15, 8))],
        [sg.Button('OK')]
    ]

    window = sg.Window('Exercícios', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'OK':
            tg = values['-MUSCULO-']
            if tg in mapeamento_exercicio_id:
                exercicio_id_selecionado = mapeamento_exercicio_id[tg]

                comando = f'SELECT * FROM series WHERE ExercicioID ="{exercicio_id_selecionado}"'
                cursor.execute(comando)
                resultados = cursor.fetchall()

                columns = ['serieID', 'ExercicioID', 'Reps', 'Peso', 'Data']
                df = pd.DataFrame(resultados, columns=columns)

                # Converter a coluna Data para o tipo datetime
                df['Data'] = pd.to_datetime(df['Data'])
                
                # Ordernar tabela df 7 dias pela data
                df = df.sort_values(by='Data')

              

                # Filtrar os últimos 7 dias
                data_limite = pd.Timestamp.now() - pd.DateOffset(days=7)
                df_ultimos_7_dias = df[df['Data'] >= data_limite]

                
                df.sort_values(by='Data')
                # Calcular o aumento da carga nos últimos 7 dias
                
                carga_inicial = float(df_ultimos_7_dias['Peso'].iloc[0])
                carga_final = float(df_ultimos_7_dias['Peso'].iloc[-1])
                aumento_carga_percentual = ((carga_final-carga_inicial)/carga_inicial)*100

                print(f'Aumento da carga nos últimos 7 dias: {aumento_carga_percentual}%')
                # Calcular a carga máxima nos últimos 7 dias
                carga_maxima_7_dias = df_ultimos_7_dias['Peso'].max()

                print(f'Carga máxima nos últimos 7 dias: {carga_final:} kg')
                print(f'Carga inicial: {carga_inicial}')
                print(df_ultimos_7_dias)

                # Plotar um gráfico de linha (plano cartesiano) para Peso
                plt.figure(figsize=(12, 8))
                
                   # Gráfico para Carga (Peso)
                plt.subplot(2, 1, 1)
                sns.lineplot(x='Data', y='Peso', data=df, label='Carga (kg)', color='blue')
                plt.title(f'Histórico de Carga para {tg} por Dia')
                plt.xlabel('Data')
                plt.ylabel('Carga (kg)')
                plt.legend()
                plt.xticks(rotation=45)

                # Gráfico para Repetições (Reps)
                plt.subplot(2, 1, 2)
                sns.lineplot(x='Data', y='Reps', data=df, label='Repetições', color='red')
                plt.title(f'Histórico de Repetições para {tg} por Dia')
                plt.xlabel('Data')
                plt.ylabel('Repetições')
                plt.legend()
                plt.xticks(rotation=45)

                plt.tight_layout()
                plt.show()

    window.close()
def  workout():
     #LISTAR EXERCICIOS
    comando = 'SELECT * FROM exercicio'
    cursor.execute(comando)
    exercicios = cursor.fetchall()

    exercise_info = ""
    
    exercise_info = [exercicio[1] for exercicio in exercicios]
    
   
    comando = 'SELECT * FROM treino'
    cursor.execute(comando)
    treinos = cursor.fetchall()
    treino_info = ''
    treino_info = [treino[2] for treino in treinos]
    treino_info = set(treino_info)
    treino_info = list(treino_info)
    
    
    layout = [
        [sg.Text('Treino:'), sg.Combo(treino_info, key='-TREINO-', size=(8,8), enable_events=True)],
        [sg.Text('Selecione o exércicio:'), sg.Combo(exercise_info, key='-NOME-', size=(35,8)), sg.Button('ADICIONAR', key='-ADD-')],
        [sg.Text('Selecione as séries por sessão:'), sg.InputText(key='-SERIES-', enable_events=True)],
        [sg.Multiline('', size=(40, 10), key='-RESULTADOS-', disabled=True)],
        [sg.Button('OK')]
    ]

    window = sg.Window('Criar Exercício', layout)
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            window.close()
            break
        elif event == '-ADD-':
            listarExer()
        elif event == '-TREINO-':
            treino_selecionado = values['-TREINO-']
            exercicio_dict = {}
            comando = f"SELECT * FROM treino WHERE Nome = '{treino_selecionado}'"
            cursor.execute(comando)
            treinos_preexistentes = cursor.fetchall()
            
            
            for treino in treinos_preexistentes:
                id_exercicio = treino[1]
                
                nome_do_exercicio = obter_nome_do_exercicio(id_exercicio)
                exercicio_dict[nome_do_exercicio] = treino[3]
                
           
            window['-RESULTADOS-'].update(value='\n'.join([f"{chave}: Seriés: {valor}" for chave, valor in exercicio_dict.items()]))

            
        elif event == 'OK':
            name = values['-NOME-']
            treino = values['-TREINO-']
            series = values['-SERIES-']
            
            comando = f"SELECT ExercicioID FROM exercicio WHERE Nome = '{name}'"
            cursor.execute(comando)
            ExercicioID = cursor.fetchall()[0][0]
            
            comando = f'INSERT INTO treino (ExercicioID, Nome, series) VALUES ("{ExercicioID}","{treino}", {series})'
            cursor.execute(comando)
            conexao.commit() # edita o banco de dados

            

            window.close()
            break
       
sg.theme('Reddit')
layout = [
    [sg.Text('TREINAMENTO ESPECIALIZADO', size=(30, 1), justification='center', font=("Helvetica", 25),auto_size_text=True, text_color='black')],
    [
        sg.Column([
            [sg.Button('HISTÓRICO', size=(50,2))],
            [sg.Button('ADICIONAR SERIES', size=(50,2))],
            [sg.Button('LISTAR EXÉRCICOS', size=(50,2))],
            [sg.Button('SERIES POR AGRUPAMENTO MUSCULAR', size=(50,2))],
            [sg.Button('DELETAR TUDO', size=(50,2))],
           
        ]),sg.VerticalSeparator(),
       
        sg.Column([
            [sg.Image(key='-IMAGE-', source=caminho_imagem)], 
            [sg.Button('TREINO', size=(50,2))],
            
                   ])
    ]
]
window = sg.Window('TREINAMENTO ESPECIALIZADO', layout, size=(800, 700))
# Loop de eventos para processar "eventos" e obter os "valores" das entradas
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    elif event == 'ADICIONAR SERIES':
        addSet()
        pass
    elif event == 'LISTAR EXÉRCICOS':
        # A lógica para listar exercícios seria implementada aqui
        listarExer() 
    elif event == 'DELETAR TUDO':
        delExer()
    elif event == 'SERIES POR AGRUPAMENTO MUSCULAR':
        setofmuscle()
    elif event == 'HISTÓRICO':
         history()
    elif event == 'TREINO':
         workout()
window.close()  
    

    
    
    
#CODE
cursor.close()
conexao.close()