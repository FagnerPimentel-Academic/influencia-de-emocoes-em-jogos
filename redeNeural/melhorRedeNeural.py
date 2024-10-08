from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from funcoesGerais import retornarHeader, retornarArquivosDiretorio, retornarNomeArquivo, criarModelo, treinarModelo, reprocessarEegFiltrados, retornarAmostras
import pandas as pd
import numpy as np
import json
import os

def dividirAmostras(lista, tamanhoAmostra):
    return [lista[i:i + tamanhoAmostra] for i in range(0, len(lista), tamanhoAmostra) if
            len(lista[i:i + tamanhoAmostra]) == tamanhoAmostra]

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
            if emocao in []:
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
        amostras = dividirAmostras(amostras, 40)
        dadosPorEmocao[emocao] = amostras

    nomeArquivo = retornarNomeArquivo(arquivo)
    diretorio = os.path.dirname(arquivo)
    caminhoArquivoJson = os.path.join(diretorio, nomeArquivo + '.json')
    if not os.path.exists(caminhoArquivoJson):
        with open(caminhoArquivoJson, 'w', encoding='utf-8') as arquivoJson:
            json.dump(dadosPorEmocao, arquivoJson, ensure_ascii=False, indent=4)

    return dadosPorEmocao


def encontrarMelhorRedeNeural(formaEntrada):
    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['.json'])

    if len(eegFiltradosJSON) != 34:
        eegFiltradosJSON = reprocessarEegFiltrados()

    if len(eegFiltradosJSON) == 34:
        arquiteturas = gerarEstruturaCamadas()
        valoresEpocas, resultados = [1000, 5000, 10000], []

        amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes = retornarAmostras()

        import time
        for arquitetura in arquiteturas:
            for epocas in valoresEpocas:
                print("Testando arquitetura %s com %s épocas..." % (str(arquitetura), str(epocas)))
                modelo = criarModelo(arquitetura, formaEntrada, mapeamentoEmocoes)
                tempoInicioTreinamento = time.time()

                _, valorPerda, valorAcuracia = treinarModelo(modelo, epocas, amostrasTreinamento,
                                                                  emocoesTreinamento, amostrasTestes, emocoesTestes)

                tempoFimTreinamento = time.time()
                tempoTotalTreinamento = tempoFimTreinamento - tempoInicioTreinamento
                horas, resto = divmod(tempoTotalTreinamento, 3600)
                minutos, segundos = divmod(tempoTotalTreinamento, 60)
                tempoTreinamento = "{:02d}:{:02d}:{:02d}".format(int(horas), int(minutos), int(segundos))

                resultados.append({
                    'Arquitetura': arquitetura,
                    'Epocas': epocas,
                    'Perda': valorPerda,
                    'Acuracia': valorAcuracia,
                    'Treinamento': tempoTreinamento
                })

                print("Arquitetura %s com %s épocas -> Perda: %.4f, Acurácia: %.4f, Tempo de Treinamento: %s" % (str(arquitetura), str(epocas), valorPerda, valorAcuracia, tempoTreinamento))

        dataFrameResultados = pd.DataFrame(resultados)
        dataFrameResultados["Melhor Resultado"] = ""
        melhorIndice = dataFrameResultados.index[
            dataFrameResultados.apply(lambda x: (x['Perda'], -x['Acuracia']), axis=1).idxmin()]
        dataFrameResultados.at[melhorIndice, "Melhor Resultado"] = "Melhor Resultado ( - Perda, + Acurácia )"
        dataFrameResultados.to_excel("./resultadoMelhorRede.xlsx", index=False)
        print("Resultados gravados no arquivo Excel: resultadoMelhorRede.xlsx")

        melhorResultado = min(resultados, key=lambda x: (x['Perda'], -x['Acuracia']))
        return melhorResultado
    else:
        print("Erro ao tentar encontrar arquivos filtrados .json")