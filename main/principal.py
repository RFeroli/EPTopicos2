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
for p in problemas_nomes:
    print('Executando o problema {}'.format(p))
    print('LAO * {}')
    t = time.time()
    LAO_star(deterministic_instances[p])
    print('Executado em {} seg\n O plano tem comprimento {} e {} estados foram visitados\n'.format(time.time() - t,
                                                                                                   len(meta_plano),
                                                                                                   contador_gerados))
    IteracaoDeValor.iteracaoDeValor().aplicar(deterministic_instances[p])
    print('Executado em {} seg\n O plano tem comprimento {} e {} estados foram visitados\n'.format(time.time()-t, len(meta_plano), contador_gerados))

print('\n\nProblemas aleatórios\n')
for p in problemas_nomes:
    print('Executando o problema {}'.format(p))
    t = time.time()
    LAO_star(random_instances[p])
    print('Executado em {} seg\n O plano tem comprimento {} e {} estados foram visitados\n'.format(time.time()-t, len(meta_plano), contador_gerados))


exit()
IteracaoDeValor.iteracaoDeValor().aplicar(deterministic_instances["navigation_1.net"]["states"],deterministic_instances["navigation_1.net"]["action"],0.1)
