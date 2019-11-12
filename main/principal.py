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


print('Problemas determinísticos\n')
gerar_graficos = False
for p in problemas_nomes:
    print('\nExecutando o problema {}'.format(p))
    t = time.time()
    LAO_star(deterministic_instances[p], gerar_graficos)
    print('LAO * Executado em {} seg\n'.format(time.time() - t))
    t = time.time()
    IteracaoDeValor.iteracaoDeValor().aplicar(problema=deterministic_instances[p], alpha=1, gerar_graficos=gerar_graficos)
    print('Iteracao de Valor Executado em {} seg'.format(time.time()-t))

print('\n\nProblemas aleatórios\n')
for p in problemas_nomes:
    print('Executando o problema {}'.format(p))
    t = time.time()
    LAO_star(random_instances[p], gerar_graficos)
    print('LAO * Executado em {} seg\n'.format(time.time() - t))
    t = time.time()
    IteracaoDeValor.iteracaoDeValor().aplicar(problema=random_instances[p], alpha=1, gerar_graficos=gerar_graficos)
    print('Iteracao de Valor Executado em {} seg\n'.format(time.time()-t))
