from main.graficos import Janela


class iteracaoDeValor:
    def aplicar(self,estados,acoes,alpha):


        politica={}
        #inicializacao
        estimativa={}
        nova_estimativa={}

        #inicializacao das primeiras estimativas

        #inicializacao com 0
        for estado in estados:
            estimativa[estado]=0;
        grafico=Janela.Grafico (estados, 20, 20, estimativa,politica)

        while True :
            #cada iteracao e baseada em dois momentos
            for estado in estados:
                if estado == 'robot-at-x10y10':
                    estimativa[estado]=0
                    nova_estimativa[estado]=0
                    politica[estado]="X"
                    continue
                # sera calculada a equcao de belman para cada estado
                minimo = 100000000
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

            #repassar as estimativas
            for estado in estados:
                estimativa[estado]=nova_estimativa[estado]

            grafico.atualizar()
