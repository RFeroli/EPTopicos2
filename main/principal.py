from main import IteracaoDeValor
from main.LAO_star import LAO_star
from main.parser import read_directory
import time

# Leitura dos problemas
path = '../in/'
deterministic_instances = read_directory('DeterministicGoalState/', path)
random_instances = read_directory('RandomGoalState/', path)

problemas_nomes = [ 'navigation_1.net', 'navigation_2.net', 'navigation_3.net', 'navigation_4.net', 'navigation_5.net',
                    'navigation_6.net', 'navigation_7.net', 'navigation_8.net', 'navigation_9.net', 'navigation_10.net']

def extrair_politica_total(name,politica):
    with open(name+".txt","w") as f:
        for estado in politica:
            f.write(estado+":"+politica[estado]+"\n")

def extrair_politica_parcial(name,politica,problema):

    acoes=problema['action']
    with open (name + ".txt", "w") as f:
        s=problema['initialstate']
        meta=problema['goalstate']
        while s!=meta :

            f.write(s+":"+politica[s]+"\n")

            sucessores=acoes[politica[s]][s]
            if sucessores[0][0]==s:
                sucessor=sucessores[1][0]
            else:
                sucessor=sucessores[0][0]
            s=sucessor

def extrair_resultados(nome,politica,problema):
    extrair_politica_parcial(nome+"politica_parcial",politica,problema)
    extrair_politica_total(nome+"politica_total",politica)




print('Problemas determinísticos\n')
gerar_graficos = False
for p in problemas_nomes:
    print('\nExecutando o problema {}'.format(p))
    t = time.time()
    lao=LAO_star(deterministic_instances[p], gerar_graficos)
    print('LAO * Executado em {} seg\n'.format(time.time() - t))
    extrair_resultados(p+"_lao_",lao,deterministic_instances[p])
    t = time.time()
    iteracao=IteracaoDeValor.iteracaoDeValor().aplicar(problema=deterministic_instances[p], alpha=0.001, gerar_graficos=gerar_graficos)

    print('Iteracao de Valor Executado em {} seg'.format(time.time()-t))
    extrair_resultados (p + "_iteracao_de_valor_", iteracao, deterministic_instances[p])


print('\n\nProblemas aleatórios\n')
for p in problemas_nomes:
    print ('\nExecutando o problema {}'.format (p))
    t = time.time ()
    lao = LAO_star (deterministic_instances[p], gerar_graficos)
    print ('LAO * Executado em {} seg\n'.format (time.time () - t))
    extrair_resultados (p + "_lao", lao, deterministic_instances[p])
    t = time.time ()
    iteracao = IteracaoDeValor.iteracaoDeValor ().aplicar (problema=deterministic_instances[p], alpha=0.001,
                                                           gerar_graficos=gerar_graficos)

    print ('Iteracao de Valor Executado em {} seg'.format (time.time () - t))
    extrair_resultados (p + "_iteracao_de_valor", iteracao, deterministic_instances[p])



