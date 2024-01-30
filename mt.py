import sys 
import json

class MaquinaTuring:

    D = ">"
    E = "<"

    def __init__(self):
        self.estadoinicial = "" #config[7]
        self.Inicio = "" #config[4]
        self.Branco = "" #config[5]
        self.fitas = [] 
        self.alfabeto = [] #config[2]
        self.simbolos = [] #config[3]
        self.estadosfinais = [] #config[8]
        self.estados = {} #config[1]
        self.numTrilhas = 0
        #transicoes config[6]

#carrega as configs do json pra maquina
    def constructorMT(self, config):
        self.numTrilhas = config[0]
        for i in range(self.numTrilhas):
            self.fitas.append([])

        for estado in config[1]:
            self.estados.update({estado: []})
        
        for simbolo in config[2]:
            self.alfabeto.append(simbolo)
        
        for entrada in config[3]:
            self.simbolos.append(entrada)

        self.Inicio = config[4]

        self.Branco = config[5]

        for transicao in config[6]:
            self.estados[transicao[0]].append(transicao[1:])

        self.estadoinicial = config[7]

        self.estadosfinais = config[8]
    

#pra maquina de turing com multiplas trilhas, devemos definir qual das trilhas vai andar
#transicao maq turing simples para maq turing multiplas: d(e,a) = [e', b, d] -> troca a por b e vai pra direita
#em uma multipla: d(e,a,"","",""...) = [e', b, "","",...,d] -> muda na trilha 1 e deixa as outras inalteradas

#valida o reconhecimento da palavra
    def valida(self, palavra):
        valido = True
        estadosfinais = self.estadosfinais
        atual = self.estadoinicial
        cabecote = 1 #setando o cabecote
        estados = self.estados
        fita = self.fitas
        fita[0] = self.Inicio + palavra #coloca a palavra na fita principal
        numTrilhas = self.numTrilhas

        for i in range(1, numTrilhas):
            fita[i] = "_"

        while valido:
            
            valido = False # hold
            estado = estados[atual]

            for transicao in estado:          
                for i in range(numTrilhas):
                    while len(fita[i]) <= cabecote + 1: # passa pela fita e adiciona os valores em branco
                        fita[i] += self.Branco

                #conferir outros valores da transicao
                check = True 
                for i in range(numTrilhas):                 
                    if transicao[i] != fita[i][cabecote]: 
                        check = False

                if check == True and transicao[numTrilhas] in estados: # se o estado for definido
                    for i in range(numTrilhas): #substitui a trilha pela proxima
                        fita[i] = fita[i].replace(fita[i][:cabecote+1], fita[i][:cabecote] + transicao[numTrilhas + 1 + i], 1) # escreve na fita
                    atual = transicao[numTrilhas] # muda de estado
                    if transicao[-1] == self.D:
                        cabecote += 1 #move cabecote p direita
                    elif transicao[-1] == self.E:
                        cabecote -= 1 #move cabecote p esquerda
                    valido = True
                    break
                else:
                    valido = False   

       #se acabar no estado final a MT deu certo - em teoria
        if atual in estadosfinais: 
            return True
        
        return False

#abrindo o json e configurando a maquina
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print('Usar: [python3] {} [MT] [Word]'.format(sys.argv[0]))
        sys.exit(1)
    
    mt = MaquinaTuring()

    with open(sys.argv[1], encoding='utf-8') as mt_json: # abre arquivo json
        config = (json.load(mt_json))

    mt.constructorMT(config['mt']) # construi a maquina
    palavra = sys.argv[2]

    if mt.valida(palavra): # roda a maquina
        print('Sim')
    else:
        print('Não')