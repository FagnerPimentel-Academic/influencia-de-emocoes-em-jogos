import pandas as pd
import json
import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input
import random

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
    return caminhoArquivo[-caminhoArquivo[::-1].find('/'):-4]

def criarModelo(camadas, formaEntrada, mapeamentoEmocoes):
    modelo = Sequential()
    modelo.add(Input(shape=formaEntrada))
    modelo.add(Flatten())
    for camada in camadas:
        modelo.add(Dense(camada, activation='tanh'))
    modelo.add(Dense(len(mapeamentoEmocoes), activation='softmax'))

    modelo.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return modelo

def gerarEstruturaCamadas(numMax=100, decrementarNum=5, porcentCamadaUm=0.8, porcentCamadaDois=0.2):
    arquiteturas = []
    for neuronios in range(numMax, decrementarNum - 1, -decrementarNum):
        numb1 = neuronios
        numb2 = int(numb1 * porcentCamadaUm)
        numb3 = int(numb1 * porcentCamadaDois)
        arquiteturas.append([numb1, numb2, numb3])
    return arquiteturas

def treinarModelo(modelo, epocas, amostras, emocoes, amostrasTeste, emocoesTeste):
    history = modelo.fit(amostras, emocoes, epochs=epocas, batch_size=32,
                                 validation_data=(amostrasTeste, emocoesTeste), verbose=1)

    val_loss, val_acc = modelo.evaluate(amostrasTeste, emocoesTeste, verbose=1)
    return history, val_loss, val_acc


def converterEmocaoParaID(y, mapeamentoEmocoes):
    for index, emocao in enumerate(y):
        try:
            y[index] = mapeamentoEmocoes[emocao]
        except Exception as e:
            print("Erro no mapeamento de emoções: %s - %s" % (emocao, str(e)))
            raise

def reprocessarEegFiltrados():
    eegFiltradosCSV = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['.csv'])
    eegFiltradosCSV.sort()
    for arquivo in eegFiltradosCSV[:28]:
        processarEmocoes(arquivo)
    for arquivo in eegFiltradosCSV[28:]:
        processarEmocoes(arquivo)
    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['.json'])
    return eegFiltradosJSON

def retornarMapeamentoEmocoes():
    caminhoMapeamentoEmocoes = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['.json'])

    with open(caminhoMapeamentoEmocoes[0], 'r', encoding='utf-8') as arquivo:
        mapeamentoEmocoes = json.load(arquivo)
    return mapeamentoEmocoes

def retornarAmostras(retornarAmostraEspecifica=False):
    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['.json'])

    mapeamentoEmocoes = retornarMapeamentoEmocoes()

    amostrasTreinamento, emocoesTreinamento = [], []
    amostrasTestes, emocoesTestes = [], []

    if retornarAmostraEspecifica:
        tentativasAmostraEspecifica = 0
        while tentativasAmostraEspecifica < 10:
            eegEscolhido = random.randint(28, 33)
            with open(eegFiltradosJSON[eegEscolhido], 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                if retornarAmostraEspecifica in dadosEmocao:
                    dadosEmocaoEscolhida = dadosEmocao[retornarAmostraEspecifica]
                    return random.choice(dadosEmocaoEscolhida)
                else:
                    tentativasAmostraEspecifica +=1
        raise ValueError("Não encontrou amostra específica.")
    else:
        for i in range(28, 34):
            with open(eegFiltradosJSON[i], 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao, amostras in dadosEmocao.items():
                    for amostra in amostras:
                        try:
                            amostrasTestes.append(np.array(amostra, dtype=np.float32).reshape(40, 17))
                            emocoesTestes.append(mapeamentoEmocoes[emocao])
                        except Exception as e:
                            pass

        for i in range(0, 28):
            with open(eegFiltradosJSON[i], 'r', encoding='utf-8') as arquivo:
                dadosEmocao = json.load(arquivo)
                for emocao, amostras in dadosEmocao.items():
                    for amostra in amostras:
                        try:
                            amostrasTreinamento.append(np.array(amostra, dtype=np.float32).reshape(40, 17))
                            emocoesTreinamento.append(mapeamentoEmocoes[emocao])
                        except Exception as e:
                            pass

        amostrasTreinamento = np.array(amostrasTreinamento, dtype=np.float32)
        emocoesTreinamento = np.array(emocoesTreinamento, dtype=np.int32)
        amostrasTestes = np.array(amostrasTestes, dtype=np.float32)
        emocoesTestes = np.array(emocoesTestes, dtype=np.int32)

        return amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes
