from main.graficos import Janela
import math

class iteracaoDeValor:
    def aplicar(self, problema,alpha):

        estados = problema['states']
        acoes = problema['action']
        politica={}
        #inicializacao
        estimativa={}


        #inicializacao das primeiras estimativas

        #inicializacao com 0
        for estado in estados:
            estimativa[estado]=0;
        grafico=Janela.Grafico (estados, 20, 20, estimativa,politica)

        while True :
            delta=0
            nova_estimativa = {}
            #cada iteracao e baseada em dois momentos
            for estado in estados:
                if estado == problema['goalstate']:
                    estimativa[estado]=0
                    nova_estimativa[estado]=0
                    politica[estado]="X"
                    continue
                # sera calculada a equcao de belman para cada estado
                minimo = math.inf
                min_arg = None
                for acao in acoes:
                    somatorio=0
                    for tupla in acoes[acao][estado]: #para cada sucessor
                        sucessor=tupla[0]
                        probabilidade=tupla[1]
                        somatorio+=probabilidade*(1+estimativa[sucessor]) #equacao de belman
                        pass
                    if somatorio <minimo:
                        minimo=somatorio
                        min_arg=acao

                politica[estado]=min_arg
                nova_estimativa[estado]=minimo
                delta+=minimo-estimativa[estado];

            #repassar as estimativas

            estimativa=nova_estimativa;
            grafico.atualizar (estimativa)
            if alpha>(delta/len(estimativa)):
                break

        return politica
