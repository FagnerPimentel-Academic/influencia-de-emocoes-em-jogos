from projecaoEletrodos3D import multiplasProjecoesPorPagina, umaProjecaoPorPagina
from melhorRedeNeural import encontrarMelhorRedeNeural
from redeNeural import realizarTreinamento, realizarDeteccao
from funcoesGerais import retornarArquivosDiretorio, reprocessarEegFiltrados
import pandas as pd
import numpy as np
import platform
import time
import json
import sys
import os

RED = "\033[91m"
RESET = "\033[0m"
formaEntrada = (72, 17)

arquivosPosicaoEletrodos = retornarArquivosDiretorio(pasta="posicaoEletrodos")
eegSujeitos = retornarArquivosDiretorio(pasta="eegSujeitos")


def exibirErro(msg):
    print(RED + "ERRO: " + msg + RESET)

def limparTerminal():
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.system('cls')
        elif sistema in ["Linux", "Darwin"]:  # Para Linux e macOS
            if 'TERM' in os.environ:
                os.system('clear')
            else:
                print("\n" * 100)
        else:
            print("\n" * 100)
    except:
        # Se o comando falhar, simplesmente imprime várias linhas vazias
        print("\n" * 100)

def exibirMenu():
    print("\n======== Menu Principal ========")
    print("1. Projeção 3D.")
    print("2. Encontrar melhor rede neural.")
    print("3. Realizar treinamento.")
    print("4. Detectar emoção.")
    print("5. Sair.")
    print("================================")


def processar_emocoes():
    caminhoMapeamentoEmocoes = os.path.dirname(os.path.abspath(__file__)) + '/mapeamentoEmocoes.json'
    try:
        with open(caminhoMapeamentoEmocoes, 'r') as jsonEmocoes:
            dadosEmocoes = json.load(jsonEmocoes)
        if not dadosEmocoes:
            raise ValueError("O mapeamento de emoções JSON está vazio.")
        print("\nEmoções processadas com sucesso!")
        # Chama a função pontosSubject3D() se necessário
        pontosSubject3D()
    except Exception as e:
        print("Erro ao processar emoções: " + str(e))


def exibir_configuracoes():
    # Exemplo fictício de configuração de rede neural
    print("\nConfigurações da Rede Neural:")
    print("Arquitetura: 40 camadas, 224 unidades por camada")
    print("Épocas: 50")
    print("Acurácia estimada: 92%")

def main():
    limparTerminal()
    while True:
        exibirMenu()
        opcaoMenu = input("Escolha uma opção: ")

        if opcaoMenu == '1':
            while True:
                limparTerminal()
                print("\n======== Projeção 3D ========")
                print("1. Projetar um indivíduo por página.")
                print("2. Projetar múltiplos individuos por página.")
                print("3. Voltar.")
                print("================================")
                opcaoProjecao = input("Escolha uma opção: ")
                if opcaoProjecao == '1':
                    print("Salvando arquivos...")
                    umaProjecaoPorPagina()
                    print("Arquivos salvos na pasta de 'projeção3D'.")
                    time.sleep(4)
                    limparTerminal()
                    break
                elif opcaoProjecao == '2':
                    print("Salvando arquivos...")
                    multiplasProjecoesPorPagina(individuosPorPagina=6)
                    print("Arquivos salvos na pasta de 'projeção3D'.")
                    time.sleep(4)
                    limparTerminal()
                    break
                elif opcaoProjecao == '3':
                    limparTerminal()
                    break
                else:
                    print("Opção inválida, tente novamente.")
        elif opcaoMenu == '2':
            while True:
                limparTerminal()
                print("\n======== Encontrar melhor rede neural ========")
                print("Essa opção costuma demorar um bom tempo, tem certeza que deseja continuar?")
                print("1. Sim.")
                print("2. Não.")
                print("================================")
                opcaoEncontrarMelhorRede = input("Escolha uma opção: ")
                if opcaoEncontrarMelhorRede == '1':
                    print("Iniciando busca...")
                    encontrarMelhorRedeNeural(formaEntrada)
                    print("Arquivo de resultado salvo na pasta de 'treinamentos'.")
                    time.sleep(4)
                    limparTerminal()
                    break
                elif opcaoEncontrarMelhorRede == '2':
                    limparTerminal()
                    break
                else:
                    print("Opção inválida, tente novamente.")
        elif opcaoMenu == '3':
            while True:
                limparTerminal()
                print("\n======== Realizar treinamento ========")
                print("1. Utilizar a melhor rede encontrada.")
                print("2. Realizar treinamento inserindo parâmetros manualmente.")
                print("================================")
                opcaoRealizarTreinamento = input("Escolha uma opção: ")
                if opcaoRealizarTreinamento not in ['1', '2']:
                    print("Opção inválida, tente novamente.")
                else:
                    while True:
                        limparTerminal()
                        print("\n======== Tipo de treinamento ========")
                        print("1. Por sujeito (80% da onda treinar / 20% onda teste).")
                        print("2. Onda fragmentada (Onda separada, 1 tick para treinamento, 1 tick para testes).")
                        print("================================")
                        opcaoTipoTreinamento = input("Escolha uma opção: ")
                        tipoTreinamento = 'porSujeito' if opcaoTipoTreinamento == '1' else 'ondaFragmentada' if opcaoTipoTreinamento == '2' else 'opcaoErrada'
                        if opcaoTipoTreinamento not in ['1', '2']:
                            print("Opção inválida, tente novamente.")
                        elif opcaoRealizarTreinamento == '1':
                            print("Iniciando treinamento...")
                            try:
                                realizarTreinamento(formaEntrada, melhorRedeNeural=True, tipoTreinamento=tipoTreinamento)
                                print("Modelo salvo na pasta de 'treinamentos'.")
                                time.sleep(4)
                                break
                            except Exception as e:
                                print("Erro ao tentar treinar modelo. %s" % e.args[0])
                                time.sleep(4)
                                limparTerminal()
                                break
                        elif opcaoRealizarTreinamento == '2':
                            print("\n======== Realizar treinamento ========")
                            print("Necessário fornecer as informações abaixo nessa ordem:")
                            print("1. Quantidade de épocas para o treinamento. (Informação numérica)*")
                            print("2. Quantidade de neurônios na 1º camada.    (Informação numérica)*")
                            print("3. Quantidade de neurônios na 2º camada.    (Informação numérica)*")
                            print("4. Quantidade de neurônios na 3º camada.    (Informação numérica)*")
                            print("================================")
                            epocas = input("Insira a quantidade de eṕocas: ")
                            primeiraCamada = input("Insira a quantiade de neurônios (1º camada): ")
                            segundaCamada = input("Insira a quantiade de neurônios (2º camada): ")
                            terceiraCamada = input("Insira a quantiade de neurônios (3º camada): ")
                            try:
                                realizarTreinamento(formaEntrada, dadosManuais={'epocas': epocas,
                                                                  'neuronios': [primeiraCamada, segundaCamada, terceiraCamada]},
                                                    nomeModelo='modeloManualTreinado.keras', tipoTreinamento=tipoTreinamento)
                                print("Modelo salvo na pasta de 'treinamentos'.")
                                time.sleep(4)
                                break
                            except Exception as e:
                                print("Erro ao tentar treinar modelo manualmente. %s" % e.args[0])
                                time.sleep(4)
                                limparTerminal()
                                break
                    break
        elif opcaoMenu == '4':
            while True:
                limparTerminal()
                print("\n======== Detectar emoção ========")
                print("Emoções disponíveis:")
                print("1. Raiva.")
                print("2. Felicidade.")
                print("3. Tristeza.")
                print("4. Medo.")
                print("5. Voltar.")
                print("================================")
                opcaoDetectarEmocao = input("Escolha uma emoção: ")
                if opcaoDetectarEmocao == '5':
                    limparTerminal()
                    break
                elif opcaoDetectarEmocao not in ['1', '2', '3', '4']:
                    print("Opção inválida, tente novamente.")
                else:
                    try:
                        realizarDeteccao(int(opcaoDetectarEmocao)-1)
                        time.sleep(2)
                        limparTerminal()
                    except Exception as e:
                        print("Erro ao realizar detecção de emoção %s" % e.args[0])
                        time.sleep(4)
        elif opcaoMenu == '5':
            limparTerminal()
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == '__main__':
    main()
