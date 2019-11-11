from decimal import Decimal
from os import listdir
from main import IteracaoDeValor
from main.LAO_star import LAO_star
path = '../in/'

def read_directory(dir, path=''):
    instance = {}
    for file in listdir(path + dir):
        g = {'states': [], 'action': {}, 'cost': [], 'initialstate': '', 'goalstate': ''}
        with open(path + dir + file) as f:
            tag = None
            action = None
            for line in f:
                data = str(line.strip())
                if data == '':
                    continue
                if 'Grid:' in data:
                    break
                else:
                    if not tag:
                        if 'action' in data:
                            info = data.split(' ')
                            tag = info[0]
                            action = info[1]
                        else:
                            tag = data
                    else:
                        if data == 'end{}'.format(tag):
                            tag = None
                            action = None
                        elif tag == 'action':
                            info = data.split(' ')[:3]
                            from_state = str(info[0])
                            g[tag][action] = g[tag].get(action, {})
                            g[tag][action][from_state] = g[tag][action].get(from_state, [])
                            g[tag][action][from_state].append((info[1], Decimal(info[2])))
                        elif tag == 'states':
                            g[tag] = [s.strip() for s in data.split(',')]
                        elif tag in ['initialstate', 'goalstate']:
                            g[tag] = data
                        elif tag == 'cost':
                            if '0.500' in data:
                                print('cost')
        instance[file] = g
    return instance


deterministic_instances = read_directory('DeterministicGoalState/', path)
random_instances = read_directory('RandomGoalState/', path)

''# for p in deterministic_instances:
import time
l = ['navigation_1.net', 'navigation_2.net', 'navigation_3.net', 'navigation_4.net', 'navigation_5.net',
     'navigation_6.net', 'navigation_7.net', 'navigation_8.net', 'navigation_9.net', 'navigation_10.net']
print('Problema de inicios definidos\n')
for p in l:
    print('Executando o problema {}'.format(p))
    t = time.time()
    meta_plano, contador_gerados = LAO_star(deterministic_instances[p])
    print('Executado em {} seg\n O plano tem comprimento {} e {} estados foram visitados\n'.format(time.time()-t, len(meta_plano), contador_gerados))

print('\n\nProblema de inicios aleatorios\n')
for p in l:
    print('Executando o problema {}'.format(p))
    t = time.time()
    meta_plano, contador_gerados = LAO_star(random_instances[p])
    print('Executado em {} seg\n O plano tem comprimento {} e {} estados foram visitados\n'.format(time.time()-t, len(meta_plano), contador_gerados))


exit()
deterministic_instances["navigation_1.net"]["action"]["move-south"]
IteracaoDeValor.iteracaoDeValor().aplicar(deterministic_instances["navigation_1.net"]["states"],deterministic_instances["navigation_1.net"]["action"],0.1)