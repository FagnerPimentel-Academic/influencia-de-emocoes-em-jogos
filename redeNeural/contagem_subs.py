import csv
import os

# Esse programa realiza a contagem dos subjects, excluindo os que não possuem todos os eletrodos utilizados ou nenhuma das emoções utilizadas

#diretorio atual para caminho relativo
dirname = os.path.dirname(__file__)
#lista de eletrodos utilizados no estudo
eletrodos = [ 'D10', 'D3', 'H10', 'B4', 'B9', 'H3', 'B3', 'B8', 'B12', 'B7','B11', 'B6', 'B2', 'H5', 'H15', 'A4','A10']

def contagem():
    #happy, sad, fear, angry
    contagem = [0,0,0,0]
    total_subs = 0
    
    for i in range(1, 36):
        flag = False
        
        if i != 22:
            print(f"lendo csv subject {i}")
            if i < 10:
                contagem_sub = [0,0,0,0]
                arquivo = f'{dirname}/dados/eegSujeitos/EEG_data_sub-0{i}.csv'
                with open(arquivo) as f_obj:
                    reader = csv.reader(f_obj, delimiter=',')
                    for line in reader:      #itera todas as linhas
                        #print(line)
                        if not flag:        #checa os eletrodos dos subjects no header (primeira linha)
                            flag = True
                            for valor in eletrodos:
                                if line.count(valor) == 0:
                                    print(f"subject nao tem eletrodo {valor}")
                                    flag = False
                                    break               
                        if not flag:
                            break
                        else:    
                            if 'happy' in line:     #checa se há alguma das emoções
                                #print('encontrou happy')
                                contagem_sub[0]+=1
                            if 'sad' in line:
                                #print("encontrou sad")
                                contagem_sub[1]+=1
                            if 'fear' in line:
                                #print("encontrou fear")
                                contagem_sub[2]+=1
                            if 'anger' in line:
                                #print("encontrou anger")
                                contagem_sub[3]+=1
            else:
                contagem_sub = [0,0,0,0]
                arquivo = f'{dirname}/dados/eegSujeitos/EEG_data_sub-{i}.csv'
                with open(arquivo) as f_obj:
                    reader = csv.reader(f_obj, delimiter=',')
                    for line in reader:      
                        #print(line)          
                        if not flag:
                            flag = True
                            for valor in eletrodos:
                                if line.count(valor) == 0:
                                    print(f"subject nao tem eletrodo{valor}")
                                    flag = False
                                    break               
                        if not flag:
                            break
                        else:    
                            if 'happy' in line:      
                                #print('encontrou happy')
                                contagem_sub[0]+=1
                            if 'sad' in line:
                                #print("encontrou sad")
                                contagem_sub[1]+=1
                            if 'fear' in line:
                                #print("encontrou fear")
                                contagem_sub[2]+=1
                            if 'anger' in line:
                                #print("encontrou anger")
                                contagem_sub[3]+=1
                
            for i in range(0,4):
                if contagem_sub[i] != 0: #adiciona ao total das emoções se o subject tiver uma quantidade maior que zero de dita emoção
                    contagem[i]+=1
            if contagem_sub.count(0) != 4: #adiciona ao total de subjects se este subject tiver uma das quatro emoções
                total_subs+=1
                
    print("happy, sad, fear, anger")
    print(contagem)
    print(f"total subjects: {total_subs}")


contagem()
#print(dirname)