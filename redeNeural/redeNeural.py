from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import ast
from funcoesGerais import criarModeloMLP, criarModeloCNNLSTM, criarModeloLSTM, retornarArquivosDiretorio, reprocessarEegFiltrados, retornarAmostras, retornarDiretorio, retornarMapeamentoEmocoes, treinarModelo
import os

def realizarDeteccao(opcaoEmocaoEscolhida):
    modeloTreinadoCaminho = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['modeloMLP.keras'])
    modeloCarregado = load_model(modeloTreinadoCaminho[0])
    mapeamentoEmocoes = retornarMapeamentoEmocoes()
    emocaoEscolhida = [emocao for emocao, valor in mapeamentoEmocoes.items() if valor == opcaoEmocaoEscolhida][0]

    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtrados.json'])

    if len(eegFiltradosJSON) != 34:
        eegFiltradosJSON = reprocessarEegFiltrados()

    if len(eegFiltradosJSON) == 34:
        amostra = retornarAmostras(tipoAmostra='específica', emocao=emocaoEscolhida)
        amostra = np.expand_dims(amostra, axis=0)
        predicoes = modeloCarregado.predict(np.array(amostra, dtype=np.float64))
        resultadoDeteccao = np.argmax(predicoes, axis=-1)
        emocaoDetectada = [emocao for emocao, valor in mapeamentoEmocoes.items() if valor == resultadoDeteccao[0]][0]
        print("Emoção: %s" % emocaoDetectada)
    else:
        print("Erro ao tentar encontrar arquivos filtrados .json")
    return

def realizarTreinamento(formaEntrada, melhorRedeNeural=False, dadosManuais={}, tipoTreinamento='porSujeito', nomeModelo='modeloMLP.keras'):
    if melhorRedeNeural:
        resultadoMelhorRede = retornarArquivosDiretorio(pasta='treinamentos', extensoes=['.xlsx'])
        df = pd.read_excel(resultadoMelhorRede[0])
        linhaMelhorResultado = df[df.iloc[:, 5] == "Melhor Resultado ( - Perda, + Acurácia )"]
        camadas = ast.literal_eval(linhaMelhorResultado.iloc[0, 0])
        epocas = int(linhaMelhorResultado.iloc[0, 1])
    else:
        camadas = [int(neuronio) for neuronio in dadosManuais['neuronios']]
        epocas = int(dadosManuais['epocas'])

    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtrados.json'])

    if len(eegFiltradosJSON) != 34:
        eegFiltradosJSON = reprocessarEegFiltrados()

    if len(eegFiltradosJSON) == 34:
        amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes = retornarAmostras(formaEntrada = formaEntrada, tipoAmostra=tipoTreinamento)
    else:
        print("Erro ao tentar encontrar arquivos filtrados .json")
        return

    mapeamentoEmocoes = retornarMapeamentoEmocoes()

    modeloMLP = criarModeloMLP(camadas=camadas, formaEntrada=formaEntrada, mapeamentoEmocoes=mapeamentoEmocoes)
    modeloCNNLSTM = criarModeloCNNLSTM(formaEntrada=formaEntrada, mapeamentoEmocoes=mapeamentoEmocoes)
    modeloLSTM = criarModeloLSTM(formaEntrada=formaEntrada, mapeamentoEmocoes=mapeamentoEmocoes)

    # _, valorPerda, valorAcuracia = treinarModelo(modeloMLP, epocas, amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes)

    _, valorPerda, valorAcuracia = treinarModelo(modeloCNNLSTM, epocas, amostrasTreinamento, emocoesTreinamento,
                                                 amostrasTestes, emocoesTestes)

    _, valorPerda, valorAcuracia = treinarModelo(modeloLSTM, epocas, amostrasTreinamento, emocoesTreinamento,
                                                 amostrasTestes, emocoesTestes)

    diretorioTreinamentos = retornarDiretorio(pasta='treinamentos')

    modelo.save(os.path.join(diretorioTreinamentos, nomeModelo))