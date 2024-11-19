# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.models import load_model
import random

import numpy as np
import pandas as pd
# import ast
# criarModeloMLP, criarModeloCNNLSTM, criarModeloLSTM
from funcoesGerais import retornarArquivosDiretorio, reprocessarEegFiltrados, retornarAmostras, retornarDiretorio, retornarMapeamentoEmocoes, treinarModelo,rotinaModeloRandomForest, carregarModelo
# import os

def realizarDeteccao(emocao):
    """Acurácias para cada combinação de emoções:
        Emoções: ('angry', 'happy'), Acurácia: 60.00%
        Emoções: ('angry', 'sad'), Acurácia: 22.22%
        Emoções: ('angry', 'fear'), Acurácia: 80.00%
        Emoções: ('happy', 'sad'), Acurácia: 77.78%
        Emoções: ('happy', 'fear'), Acurácia: 80.00%
        Emoções: ('sad', 'fear'), Acurácia: 88.89%"""
    modeloAngryFear = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['model_angry_fear.pkl'])
    modeloHappySad = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['model_happy_sad.pkl'])
    modeloAngryFear = carregarModelo(modeloAngryFear[0])
    modeloHappySad = carregarModelo(modeloHappySad[0])
    if emocao in ['angry', 'fear']:
        dadosTesteAngryFear = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['dadosTesteangry_fear.csv'])
        labelTesteAngryFear = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['labelTesteangry_fear.csv'])
        dadosTeste = pd.read_csv(dadosTesteAngryFear[0])
        labelTeste = pd.read_csv(labelTesteAngryFear[0])
        indices = labelTeste[labelTeste['label'] == emocao].index.tolist()
        indice_aleatorio = random.choice(indices)
        amostraSelecionada = dadosTeste.iloc[indice_aleatorio].to_frame().T
        deteccao_angry_fear = modeloAngryFear.predict_proba(amostraSelecionada)
        deteccao = {classe: round(prob,2) for classe, prob in zip(modeloAngryFear.classes_, deteccao_angry_fear[0])}
        return deteccao
    elif emocao in ['happy', 'sad']:
        dadosTesteHappySad = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['dadosTestehappy_sad.csv'])
        labelTesteHappySad = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['labelTestehappy_sad.csv'])
        dadosTeste = pd.read_csv(dadosTesteHappySad[0])
        labelTeste = pd.read_csv(labelTesteHappySad[0])
        indices = labelTeste[labelTeste['label'] == emocao].index.tolist()
        indice_aleatorio = random.choice(indices)
        amostraSelecionada = dadosTeste.iloc[indice_aleatorio].to_frame().T
        deteccao_happy_sad = modeloHappySad.predict_proba(amostraSelecionada)
        deteccao = {classe: round(prob,2) for classe, prob in zip(modeloHappySad.classes_, deteccao_happy_sad[0])}
        return deteccao


    # mapeamentoEmocoes = retornarMapeamentoEmocoes()
    # emocaoEscolhida = [emocao for emocao, valor in mapeamentoEmocoes.items() if valor == opcaoEmocaoEscolhida][0]

    # eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtrados.json'])

    # if len(eegFiltradosJSON) != 34:
    #     eegFiltradosJSON = reprocessarEegFiltrados()

    # if len(eegFiltradosJSON) == 34:
    #     amostra = retornarAmostras(tipoAmostra='específica', emocao=emocaoEscolhida)
    #     amostra = np.expand_dims(amostra, axis=0)
    #     predicoes = modeloCarregado.predict(np.array(amostra, dtype=np.float64))
    #     resultadoDeteccao = np.argmax(predicoes, axis=-1)
    #     emocaoDetectada = [emocao for emocao, valor in mapeamentoEmocoes.items() if valor == resultadoDeteccao[0]][0]
    #     print("Emoção: %s" % emocaoDetectada)
    # else:
    #     print("Erro ao tentar encontrar arquivos filtrados .json")
    # return

def realizarTreinamento(formaEntrada=False, melhorRedeNeural=False, dadosManuais={}, tipoTreinamento='porSujeito', nomeModelo='modeloMLP.keras'):
    # if melhorRedeNeural:
    #     resultadoMelhorRede = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['.xlsx'])
    #     df = pd.read_excel(resultadoMelhorRede[0])
    #     linhaMelhorResultado = df[df.iloc[:, 5] == "Melhor Resultado ( - Perda, + Acurácia )"]
    #     camadas = ast.literal_eval(linhaMelhorResultado.iloc[0, 0])
    #     epocas = int(linhaMelhorResultado.iloc[0, 1])
    # else:
    #     camadas = [int(neuronio) for neuronio in dadosManuais['neuronios']]
    #     epocas = int(dadosManuais['epocas'])
    #
    # eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtrados.json'])
    #
    # if len(eegFiltradosJSON) != 34:
    #     eegFiltradosJSON = reprocessarEegFiltrados()
    #
    # if len(eegFiltradosJSON) == 34:
    # amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes = retornarAmostras(formaEntrada = formaEntrada, tipoAmostra=tipoTreinamento)
    # else:
    #     print("Erro ao tentar encontrar arquivos filtrados .json")
    #     return

    # mapeamentoEmocoes = retornarMapeamentoEmocoes()

    # modeloMLP = criarModeloMLP(camadas=camadas, formaEntrada=formaEntrada, mapeamentoEmocoes=mapeamentoEmocoes)
    # modeloCNNLSTM = criarModeloCNNLSTM(formaEntrada=formaEntrada, mapeamentoEmocoes=mapeamentoEmocoes)
    # modeloLSTM = criarModeloLSTM(formaEntrada=formaEntrada, mapeamentoEmocoes=mapeamentoEmocoes)
    arvoreDecisao = rotinaModeloRandomForest()

    # _, valorPerda, valorAcuracia = treinarModelo(modeloMLP, epocas, amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes)

    # _, valorPerda, valorAcuracia = treinarModelo(modeloCNNLSTM, epocas, amostrasTreinamento, emocoesTreinamento,
    #                                              amostrasTestes, emocoesTestes)
    #
    # _, valorPerda, valorAcuracia = treinarModelo(modeloLSTM, epocas, amostrasTreinamento, emocoesTreinamento,
    #                                              amostrasTestes, emocoesTestes)

    # diretorioTreinamentos = retornarDiretorio(pasta='treinamentos')
    #
    # modelo.save(os.path.join(diretorioTreinamentos, nomeModelo))