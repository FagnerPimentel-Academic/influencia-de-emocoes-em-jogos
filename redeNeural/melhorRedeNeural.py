from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
# criarModeloMLP
from funcoesGerais import retornarArquivosDiretorio, treinarModelo, reprocessarEegFiltrados, \
    retornarAmostras, gerarEstruturaCamadas, retornarMapeamentoEmocoes
import pandas as pd

def encontrarMelhorRedeNeural(formaEntrada):
    eegFiltradosJSON = retornarArquivosDiretorio(pasta='eegFiltrados', extensoes=['filtrados.json'])

    if len(eegFiltradosJSON) != 34:
        eegFiltradosJSON = reprocessarEegFiltrados()

    if len(eegFiltradosJSON) == 34:
        arquiteturas = gerarEstruturaCamadas()
        valoresEpocas, resultados = [1000, 5000, 10000], []
        modelosTreinamento = ['modeloMLP', 'modelo', 'modelo']
        mapeamentoEmocoes = retornarMapeamentoEmocoes()

        amostrasTreinamento, emocoesTreinamento, amostrasTestes, emocoesTestes = retornarAmostras()

        import time
        for arquitetura in arquiteturas:
            for epocas in valoresEpocas:
                print("Testando arquitetura %s com %s épocas..." % (str(arquitetura), str(epocas)))
                modelo = criarModeloMLP(arquitetura, formaEntrada, mapeamentoEmocoes)
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