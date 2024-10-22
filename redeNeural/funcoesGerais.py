import pandas as pd
import json
import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input, BatchNormalization, Conv1D, MaxPooling1D, LSTM, Dense
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout
import random
import matplotlib.pyplot as plt
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.utils.version_utils import callbacks


def dividirAmostras(lista, tamanhoAmostra):
    return [lista[i:i + tamanhoAmostra] for i in range(0, len(lista), tamanhoAmostra) if
            len(lista[i:i + tamanhoAmostra]) == tamanhoAmostra]

def fragmentarAmostra(lista):
    amostra1 = []
    amostra2 = []

    #Fragmentar amostras
    for i, sublista in enumerate(lista):
        if i % 2 == 0:
            amostra1.append(sublista)
        else:
            amostra2.append(sublista)

    #Igualar tamanho das amostras
    if len(amostra1) > len(amostra2):
        amostra1.pop()
    elif len(amostra2) > len(amostra1):
        amostra2.pop()

    return amostra1, amostra2

def retornarDiretorio(pasta=""):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados', pasta)


def retornarArquivosDiretorio(pasta="", extensoes=None):
    if extensoes is None:
        extensoes = []

    caminho_diretorio = retornarDiretorio(pasta)

    return [
        os.path.join(caminho_diretorio, arquivo)
        for arquivo in os.listdir(caminho_diretorio)
        if os.path.isfile(os.path.join(caminho_diretorio, arquivo)) and
           (not extensoes or arquivo.endswith(tuple(extensoes)))
    ]

def retornarHeader():
    df = pd.read_csv(retornarDiretorio('eegSujeitos') + '/headerArquivos.csv')
    headersDict = df.set_index('Arquivo')['Headers'].apply(lambda x: x.split(', ')).to_dict()
    return headersDict

def retornarNomeArquivo(caminhoArquivo):
    if '/' not in caminhoArquivo:
        return caminhoArquivo[::-1][:caminhoArquivo[::-1].find("\\")][::-1]
    else:
        return caminhoArquivo[-caminhoArquivo[::-1].find('/'):-4]

# def criarModeloLSTM(formaEntrada, mapeamentoEmocoes):
#     modelo = Sequential()
#     modelo.add(LSTM(64, input_shape=formaEntrada, return_sequences=True))
#     modelo.add(Dropout(0.5))
#     modelo.add(LSTM(64))
#     modelo.add(Dense(len(mapeamentoEmocoes), activation='softmax'))
#     opt = Adam(learning_rate=0.0001)
#     modelo.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
#     return modelo


def criarModeloMLP(camadas, formaEntrada, mapeamentoEmocoes):
    modelo = Sequential()
    modelo.add(Input(shape=formaEntrada))
    modelo.add(Flatten())
    for camada in camadas:
        modelo.add(Dense(camada, activation='tanh'))
        # modelo.add(Dropout(0.2))
        # modelo.add(BatchNormalization())
    modelo.add(Dense(len(mapeamentoEmocoes), activation='softmax'))

    modelo.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return modelo

def criarModeloCNNLSTM(formaEntrada, mapeamentoEmocoes):
    modelo = Sequential()
    modelo.add(Conv1D(64, 3, activation='tanh', input_shape=formaEntrada))
    modelo.add(MaxPooling1D(pool_size=2))
    modelo.add(LSTM(128))
    modelo.add(Dense(len(mapeamentoEmocoes), activation='softmax'))

    modelo.compile(optimizer='adam',
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    return modelo

def criarModeloLSTM(formaEntrada, mapeamentoEmocoes):
    modelo = Sequential()
    modelo.add(LSTM(128, input_shape=formaEntrada))
    modelo.add(Dense(len(mapeamentoEmocoes), activation='softmax'))

    modelo.compile(optimizer='adam',
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    return modelo


def gerarEstruturaCamadas(numMax=100, decrementarNum=5, porcentCamadaUm=0.8, porcentCamadaDois=0.2):
    arquiteturas = []
    for neuronios in range(numMax, decrementarNum - 1, -decrementarNum):
        numb1 = neuronios
        numb2 = int(numb1 * porcentCamadaUm)
        numb3 = int(numb1 * porcentCamadaDois)
        arquiteturas.append([numb1, numb2, numb3])
    return arquiteturas

def plotarHistory(history):
    # Resumo da perda
    plt.figure(figsize=(12, 6))

    # Perda
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.title('Loss durante o treinamento')
    plt.xlabel('Épocas')
    plt.ylabel('Perda')
    plt.legend()

    # Acurácia
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.title('Acurácia durante o treinamento')
    plt.xlabel('Épocas')
    plt.ylabel('Acurácia')
    plt.legend()

    plt.show()

def treinarModelo(modelo, epocas, amostras, emocoes, amostrasTeste, emocoesTeste):
    # earlyStopping = EarlyStopping(monitor='val_loss', patience=3000, restore_best_weights=True)
    # callbacks = [earlyStopping]
    history = modelo.fit(amostras, emocoes, epochs=epocas, batch_size=32,
                                 validation_data=(amostrasTeste, emocoesTeste), verbose=1,
                         )
    # plotarHistory(history)
    melhor_val_loss = max(history.history['val_loss'])
    indice_melhor_epoca = history.history['val_loss'].index(melhor_val_loss)
    print('Melhor val_loss: %s na época %s' % (str(melhor_val_loss), str(indice_melhor_epoca + 1)))
    val_loss, val_acc = modelo.evaluate(amostrasTeste, emocoesTeste, verbose=1)
    return history, val_loss, val_acc


def converterEmocaoParaID(y, mapeamentoEmocoes):
    for index, emocao in enumerate(y):
        try:
            y[index] = mapeamentoEmocoes[emocao]
        except Exception as e:
            print("Erro no mapeamento de emoções: %s - %s" % (emocao, str(e)))
            raise

def processarEmocoes(arquivo):
    dados = pd.read_csv(arquivo)
    dadosPorEmocao = {}

    emocaoAtual = None
    grupoAtual = []
    # ignorarLinhas = ['InitialInstructions', 'prebase_instruct', 'prebase', 'exit', 'FeelingItInstructionsButton',
    #                  'InstructionsForEnding', 'ImaginationSuggestions', 'enter', 'postbase_instruct', 'ExitThankYou',
    #                  'postbase', 'FeelingItInstructionsNoButton']

    tempoAnterior = None
    intervaloMinimo = 1.0

    for _, linha in dados.iterrows():
        tempoAtual = linha['tempo']
        if tempoAnterior is None or (tempoAtual - tempoAnterior) >= intervaloMinimo:
            emocao = linha['emotion']
            # if emocao in ignorarLinhas:
            #     continue
            if emocao in ['press']:
                continue
            else:
                caracteristicas = linha.drop(labels=['tempo', 'emotion']).tolist()

                if emocao == emocaoAtual:
                    grupoAtual.append(caracteristicas)
                else:
                    if emocaoAtual is not None:
                        if emocaoAtual not in dadosPorEmocao:
                            dadosPorEmocao[emocaoAtual] = []
                        dadosPorEmocao[emocaoAtual].append(grupoAtual)

                    emocaoAtual = emocao
                    grupoAtual = [caracteristicas]
            tempoAnterior = tempoAtual

    if emocaoAtual is not None:
        if emocaoAtual not in dadosPorEmocao:
            dadosPorEmocao[emocaoAtual] = []
        dadosPorEmocao[emocaoAtual].append(grupoAtual)

    for emocao in dadosPorEmocao.keys():
        amostras = dadosPorEmocao[emocao][0]
        amostra1, amostra2 = fragmentarAmostra(amostras)
        # amostras = dividirAmostras(amostras, 40)
        dadosPorEmocao[emocao] = {'fragmentacao1': amostra1,
                                  'fragmentacao2': amostra2}

    nomeArquivo = retornarNomeArquivo(arquivo)
    diretorio = retornarDiretorio(pasta='eegFiltrados')
    for i in range(1,3):
        jsonGravar = {}
        for emocao in dadosPorEmocao.keys():
            jsonGravar[emocao] = dadosPorEmocao[emocao]['fragmentacao%d' % i]
        caminhoArquivoJson = os.path.join(diretorio, nomeArquivo[:-4] + 'frag%d' % i + '.json')
        if not os.path.exists(caminhoArquivoJson):
            with open(caminhoArquivoJson, 'w', encoding='utf-8') as arquivoJson:
                json.dump(jsonGravar, arquivoJson, ensure_ascii=False, indent=4)

    return dadosPorEmocao

def reprocessarEegFiltrados():
    eegFiltradosCSV = retornarArquivosDiretorio(pasta='eegSujeitos', extensoes=['eeg_filtrados.csv'])
    eegFiltradosCSV.sort()
    for arquivo in eegFiltradosCSV[:28]:
        processarEmocoes(arquivo)
    for arquivo in eegFiltradosCSV[28:]:
        processarEmocoes(arquivo)
    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtrados.json'])
    return eegFiltradosJSON

def retornarMapeamentoEmocoes():

    caminhoMapeamentoEmocoes = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['.json'])

    with open(caminhoMapeamentoEmocoes[0], 'r', encoding='utf-8') as arquivo:
        mapeamentoEmocoes = json.load(arquivo)
    return mapeamentoEmocoes

def retornarAmostras(formaEntrada=(40, 17), tipoAmostra="específica", emocao=False):
    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtrados.json'])
    eegFiltradosJSON20 = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['20.json'])

    mapeamentoEmocoes = retornarMapeamentoEmocoes()

    amostrasTreinamento, emocoesTreinamento = [], []
    amostrasTestes, emocoesTestes = [], []

    if tipoAmostra == 'específica':
        tentativasAmostraEspecifica = 0
        while tentativasAmostraEspecifica < 100:
            eegEscolhido = random.randint(0, 33)
            with open(eegFiltradosJSON20[eegEscolhido], 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                if emocao in dadosEmocao and [amostra for amostra in dadosEmocao[emocao] if len(amostra[0]) == 17]:
                    dadosEmocaoEscolhida = dadosEmocao[emocao]
                    return random.choice(dadosEmocaoEscolhida)
                else:
                    tentativasAmostraEspecifica +=1
        raise ValueError("Não encontrou amostra específica.")
    elif tipoAmostra == 'porSujeito':
        eegFiltradosJSON80 = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['80.json'])
        for filtrado in eegFiltradosJSON80:
            with open(filtrado, 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao, amostras in dadosEmocao.items():
                    for amostra in amostras:
                        try:
                            amostrasTreinamento.append(np.array(amostra, dtype=np.float64).reshape(formaEntrada[0], formaEntrada[1]))
                            emocoesTreinamento.append(mapeamentoEmocoes[emocao])
                        except Exception as e:
                            pass
        for filtrado in eegFiltradosJSON20:
            with open(filtrado, 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao, amostras in dadosEmocao.items():
                    for amostra in amostras:
                        try:
                            amostrasTestes.append(np.array(amostra, dtype=np.float64).reshape(formaEntrada[0], formaEntrada[1]))
                            emocoesTestes.append(mapeamentoEmocoes[emocao])
                        except Exception as e:
                            pass
        # dict80 = {}
        # dict20 = {}
        # for emocao in dadosEmocao.keys():
        #     qtdAmostrasTreinamento = int(len(dadosEmocao[emocao]) * 0.8)
        #     for amostra in dadosEmocao[emocao]:
        #         if qtdAmostrasTreinamento > 0:
        #             if emocao in dict80.keys():
        #                 amostraEmocoes = dict80.get(emocao)
        #                 amostraEmocoes.append(amostra)
        #             else:
        #                 dict80[emocao] = [amostra]
        #             qtdAmostrasTreinamento -= 1
        #         else:
        #             if emocao in dict20.keys():
        #                 amostraEmocoes = dict20.get(emocao)
        #                 amostraEmocoes.append(amostra)
        #             else:
        #                 dict20[emocao] = [amostra]
        # nomeArquivo = retornarNomeArquivo(eegFiltradosJSON[i])
        # nomeArquivo80, nomeArquivo20 = nomeArquivo[:-5] + '_80', nomeArquivo[:-5] + '_20'
        # diretorio = os.path.dirname(eegFiltradosJSON[i])
        # caminhoArquivoJson80 = os.path.join(diretorio, nomeArquivo80 + '.json')
        # caminhoArquivoJson20 = os.path.join(diretorio, nomeArquivo20 + '.json')
        # if not os.path.exists(caminhoArquivoJson80):
        #     with open(caminhoArquivoJson80, 'w', encoding='utf-8') as arquivoJson:
        #         json.dump(dict80, arquivoJson, ensure_ascii=False, indent=4)
        # if not os.path.exists(caminhoArquivoJson20):
        #     with open(caminhoArquivoJson20, 'w', encoding='utf-8') as arquivoJson:
        #         json.dump(dict20, arquivoJson, ensure_ascii=False, indent=4)
    elif tipoAmostra == 'ondaFragmentada':
        eegFrag1JSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtradosfrag1.json'])
        eegFrag2JSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtradosfrag2.json'])
        tempoEmocao1, tempoEmocao2 = [], []
        for filtrado in eegFrag1JSON:
            with open(filtrado, 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                tempoEmocaoPorSubject = []
                for emocao in dadosEmocao.keys():
                    tempoEmocaoPorSubject.append([emocao, len(dadosEmocao[emocao])])
                tempoEmocao1.append(tempoEmocaoPorSubject)
        for filtrado in eegFrag2JSON:
            with open(filtrado, 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                tempoEmocaoPorSubject = []
                for emocao in dadosEmocao.keys():
                    tempoEmocaoPorSubject.append([emocao, len(dadosEmocao[emocao])])
                tempoEmocao2.append(tempoEmocaoPorSubject)

        from collections import defaultdict
        import numpy as np

        duracoes_por_emocao = defaultdict(list)
        # Agrupar durações por emoção
        for sessao in tempoEmocao1:
            for emocao, duracao in sessao:
                duracoes_por_emocao[emocao].append(duracao)

        # Calcular estatísticas
        estatisticas = {}
        for emocao, duracoes in duracoes_por_emocao.items():
            media = np.mean(duracoes)
            mediana = np.median(duracoes)
            desvio_padrao = np.std(duracoes)
            duracao_min = np.min(duracoes)
            duracao_max = np.max(duracoes)

            estatisticas[emocao] = {
                'media': media,
                'mediana': mediana,
                'desvio_padrao': desvio_padrao,
                'minimo': duracao_min,
                'maximo': duracao_max
            }

        # Exibir as estatísticas
        for emocao, stats in estatisticas.items():
            print(f"Emoção: {emocao}")
            print(f"  Média: {stats['media']}")
            print(f"  Mediana: {stats['mediana']}")
            print(f"  Desvio Padrão: {stats['desvio_padrao']}")
            print(f"  Mínimo: {stats['minimo']}")
            print(f"  Máximo: {stats['maximo']}")
            print()

        tamanhoAmostra = 72

        for filtrado in eegFrag1JSON:
            with open(filtrado, 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao in dadosEmocao.keys():
                    amostras = dividirAmostras(dadosEmocao[emocao], tamanhoAmostra)
                    for amostra in amostras:
                        if len(amostra[0]) == 17:
                            amostrasTreinamento.append(np.array(amostra, dtype=np.float64).reshape(formaEntrada[0], formaEntrada[1]))
                            emocoesTreinamento.append(mapeamentoEmocoes[emocao])
        for filtrado in eegFrag2JSON:
            with open(filtrado, 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao in dadosEmocao.keys():
                    amostras = dividirAmostras(dadosEmocao[emocao], tamanhoAmostra)
                    for amostra in amostras:
                        if len(amostra[0]) == 17:
                            amostrasTestes.append(np.array(amostra, dtype=np.float64).reshape(formaEntrada[0], formaEntrada[1]))
                            emocoesTestes.append(mapeamentoEmocoes[emocao])
    else:
        for i in range(28, 34):
            with open(eegFiltradosJSON[i], 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao, amostras in dadosEmocao.items():
                    for amostra in amostras:
                        try:
                            amostrasTestes.append(np.array(amostra, dtype=np.float64).reshape(formaEntrada[0], formaEntrada[1]))
                            emocoesTestes.append(mapeamentoEmocoes[emocao])
                        except Exception as e:
                            pass

        for i in range(0, 28):
            with open(eegFiltradosJSON[i], 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao, amostras in dadosEmocao.items():
                    for amostra in amostras:
                        try:
                            amostrasTreinamento.append(np.array(amostra, dtype=np.float64).reshape(formaEntrada[0], formaEntrada[1]))
                            emocoesTreinamento.append(mapeamentoEmocoes[emocao])
                        except Exception as e:
                            pass

    amostrasTreinamento = np.array(amostrasTreinamento, dtype=np.float64)
    emocoesTreinamento = np.array(emocoesTreinamento, dtype=np.int32)
    amostrasTestes = np.array(amostrasTestes, dtype=np.float64)
    emocoesTestes = np.array(emocoesTestes, dtype=np.int32)

    return amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes
