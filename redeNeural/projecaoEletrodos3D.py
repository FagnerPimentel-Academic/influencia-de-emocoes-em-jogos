from funcoesGerais import retornarHeader, retornarDiretorio, retornarNomeArquivo
from mpl_toolkits.mplot3d import Axes3D
from pyparsing import lineStart
import matplotlib.pyplot as plt
import pandas as pd
import os

def contabilizarEletrodosPorSujeito(quantidadeEletrodos=46):
    eletrodosPorSujeito = {}
    cabecalhos = retornarHeader()

    for cabecalhoSujeito, eletrodos in cabecalhos.items():
        for eletrodo in eletrodos:
            if eletrodo not in ['Time', 'Event']:
                if eletrodo not in eletrodosPorSujeito:
                    eletrodosPorSujeito[eletrodo] = [1, [cabecalhoSujeito]]
                else:
                    eletrodosPorSujeito[eletrodo][0] += 1
                    eletrodosPorSujeito[eletrodo][1].append(cabecalhoSujeito)

    if quantidadeEletrodos > 0:
        principaisEletrodos = sorted(
            [(quantidade, eletrodo) for eletrodo, (quantidade, _) in eletrodosPorSujeito.items()],
            reverse=True
        )[:quantidadeEletrodos]
    else:
        principaisEletrodos = sorted(
            [(quantidade, eletrodo) for eletrodo, (quantidade, _) in eletrodosPorSujeito.items()],
            reverse=True
        )

    eletrodosComMaisDe31 = [
        eletrodosPorSujeito[eletrodo] for _, eletrodo in principaisEletrodos
    ]

    sujeitosMaisFrequentes = sorted(
        [(len(sujeitos), sujeitos) for _, sujeitos in eletrodosComMaisDe31],
        reverse=True
    )[0][1]

    diferencasSujeitos = []
    for _, sujeitos in sorted([(len(sujeitos), sujeitos) for _, sujeitos in eletrodosComMaisDe31]):
        diferenca = set(sujeitosMaisFrequentes) - set(sujeitos)
        diferencasSujeitos.extend(dif for dif in diferenca if dif not in diferencasSujeitos)

    return principaisEletrodos


def multiplasProjecoesPorPagina(individuosPorPagina=6):
    from main import arquivosPosicaoEletrodos
    eletrodosContabilizados = [l[1] for l in contabilizarEletrodosPorSujeito()]

    arquivosParaProjecao, listaAuxiliar = [], []
    for arquivo in arquivosPosicaoEletrodos:
        listaAuxiliar.append(arquivo)
        if len(listaAuxiliar) == individuosPorPagina:
            arquivosParaProjecao.append(listaAuxiliar)
            listaAuxiliar = []
    if listaAuxiliar:
        arquivosParaProjecao.append(listaAuxiliar)

    for i, arquivoParaProjecao in enumerate(arquivosParaProjecao):
        rows = 2
        cols = len(arquivosParaProjecao) // 2 if len(arquivosParaProjecao) % 2 == 0 else len(arquivosParaProjecao) // 2 + 1

        fig, axes = plt.subplots(rows, cols, figsize=(20, 10), subplot_kw={'projection': '3d'})
        axes = axes.ravel()
        for j, arquivo in enumerate(arquivoParaProjecao):
            nomeArquivo = retornarNomeArquivo(arquivo)
            posicaoEletrodos = pd.read_csv(arquivo, sep='\t')
            eletrodosEscolhidos = posicaoEletrodos[posicaoEletrodos['name'].isin(eletrodosContabilizados)]
            demaisEletrodos = posicaoEletrodos[~posicaoEletrodos['name'].isin(eletrodosContabilizados)]

            ax = axes[j]
            ax.scatter(eletrodosEscolhidos['x'], eletrodosEscolhidos['y'], eletrodosEscolhidos['z'], color='r', s=35)
            ax.scatter(demaisEletrodos['x'], demaisEletrodos['y'], demaisEletrodos['z'], color='b', s=35)
            for j, row in eletrodosEscolhidos.iterrows():
                ax.text(row['x'], row['y'], row['z'], row['name'], size=10, zorder=1)

            ax.set_xlim([posicaoEletrodos['x'].min(), posicaoEletrodos['x'].max()])
            ax.set_ylim([posicaoEletrodos['y'].min(), posicaoEletrodos['y'].max()])
            ax.set_zlim([posicaoEletrodos['z'].min(), posicaoEletrodos['z'].max()])

            ax.view_init(elev=45, azim=15)

            ax.set_title('%s' % nomeArquivo, fontsize=10)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

        plt.savefig(retornarDiretorio("projecao3D") + '/individuos%d.png' % (i+1), bbox_inches='tight')
        plt.tight_layout()
        plt.close()
        # plt.show()



def umaProjecaoPorPagina():
    from main import arquivosPosicaoEletrodos
    eletrodosContabilizados = [l[1] for l in contabilizarEletrodosPorSujeito()]
    for i, arquivo in enumerate(arquivosPosicaoEletrodos):
        nomeArquivo = retornarNomeArquivo(arquivo)
        posicaoEletrodos = pd.read_csv(arquivo, sep='\t')
        eletrodosEscolhidos = posicaoEletrodos[posicaoEletrodos['name'].isin(eletrodosContabilizados)]
        demaisEletrodos = posicaoEletrodos[~posicaoEletrodos['name'].isin(eletrodosContabilizados)]

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(eletrodosEscolhidos['x'], eletrodosEscolhidos['y'], eletrodosEscolhidos['z'], color='r', s=50)
        ax.scatter(demaisEletrodos['x'], demaisEletrodos['y'], demaisEletrodos['z'], color='b', s=50)

        for j, row in posicaoEletrodos.iterrows():
            ax.text(row['x'], row['y'], row['z'], row['name'], size=10, zorder=1)

        ax.set_xlim([posicaoEletrodos['x'].min(), posicaoEletrodos['x'].max()])
        ax.set_ylim([posicaoEletrodos['y'].min(), posicaoEletrodos['y'].max()])
        ax.set_zlim([posicaoEletrodos['z'].min(), posicaoEletrodos['z'].max()])

        ax.view_init(elev=45, azim=15)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('%s' % nomeArquivo)

        plt.savefig(retornarDiretorio("projecao3D") + '/' + nomeArquivo + '.png', bbox_inches='tight')

        plt.close()
        # plt.show()
