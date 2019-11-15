import random
import re
import hashlib
import base64
import heapq
import math
from _decimal import Decimal
from main.graficos import Janela
from sympy import solve, symbols


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        try:
            heapq.heappush(self.elements, (priority, item))
        except:
            pass
    def get(self):
        return heapq.heappop(self.elements)[1]


def aplicar(estados, no_pai, estimativa_inicial, acoes, meta, alpha=0.0001):

    # estados = problema['states']
    # acoes = problema['action']
    politica={}
    #inicializacao
    estimativa={}


    #inicializacao das primeiras estimativas

    #inicializacao com 0
    for estado in estimativa_inicial:
        estimativa[estado]=estimativa_inicial[estado]
    # grafico=Janela.Grafico (estados, 20, 20, estimativa,politica)
    contador = 0
    while True :
        contador+=1
        delta=0
        nova_estimativa = {}
        #cada iteracao e baseada em dois momentos
        for estado in estados:
            if estado == meta:
                estimativa[estado]=0
                nova_estimativa[estado]=0
                politica[estado]='move-north'
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
            delta+=minimo-estimativa[estado]

        #repassar as estimativas
        for i in nova_estimativa:
            estimativa[i]=nova_estimativa[i]
        # grafico.atualizar (estimativa, politica)
        if alpha>(delta/len(estimativa)):
            break

    proximos_expansiveis = set()
    for x in politica:
        for t in acoes[politica[x]][x]:
            if t[0] not in estados:
                proximos_expansiveis.add(t[0])
    # proximos_expansiveis = [acoes[politica[x]][x] for x in politica]
    print(contador)
    return politica, proximos_expansiveis



def calcula_heuristica(estado, meta):
    _, xe, ye = re.split('x|y',estado)
    _, xm, ym = re.split('x|y', meta)
    return abs(int(xe)-int(xm)) + abs(int(ye)-int(ym))


def make_hashable(o):
    if isinstance(o, (tuple, list)):
        return tuple((make_hashable(e) for e in o))

    if isinstance(o, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in o.items()))

    if isinstance(o, (set, frozenset)):
        return tuple(sorted(make_hashable(e) for e in o))

    return o

def _gere_hash(o):
    hasher = hashlib.sha256()
    hasher.update(repr(make_hashable(o)).encode())
    return base64.b64encode(hasher.digest()).decode()

def equivalentes(estado, meta):
    _, xe, ye = re.split('x|y', estado)
    _, xm, ym = re.split('x|y', meta)
    if int(xe) == int(xm) and int(ye) == int(ym):
        return True
    return False

def lista_vizinhos(problema, estado):
    d = []
    for action in problema['action']:
        for l in problema['action'][action][estado]:
            if l[0] != estado:
                d.append(l[0])

    return d

def lista_vizinhos_operacoes(problema, estado):
    return {action:problema['action'][action][estado] for action in problema['action']}


def atualiza_custo(problema, estado, custo_estado):

    h_e = _gere_hash(estado)
    dict = lista_vizinhos_operacoes(problema, estado)
    def retorna_valor(est):
        if estado == est:
            return 'x'
        return custo_estado[_gere_hash(est)][0]
    saida = []
    for operacao in dict:

        s = '1 + ' + ' + '.join([str(retorna_valor(x[0]))+'*'+str(round(x[1],2)) for x in dict[operacao]]) + ' - x'
        x = symbols('x')
        saida += solve(s, x)

    custo_estado[h_e][0] = min(saida)

        # estado = no_pai[h_e][0]
    # atualiza_custo(problema, no_pai[h_e][0], custo_estado, no_pai)


def retorna_proximo_expandido(conjunto):
    elem = random.sample(conjunto, 1)[0]
    conjunto.remove(elem)
    return elem

def LAO_star(problema, gerar_graficos):

    inicio = problema['initialstate']
    meta = problema['goalstate']

    heuristica_inicio = calcula_heuristica(inicio, meta)
    estimativa = {inicio:heuristica_inicio}
    nos_expandidos = set()
    politica = {inicio:None}
    nos_folhas = {inicio}
    no_pai = {}

    no_pai[inicio] = set()
    meta_plano = []
    grafico = Janela.Grafico(problema['states'], 20, 20, estimativa, problema['states'])
    while nos_folhas:
        grafico.atualizar(estimativa, politica)
        atual = retorna_proximo_expandido(nos_folhas)


        for vizinho in lista_vizinhos(problema, atual):
            no_pai[vizinho] = no_pai.get(vizinho, set())
            no_pai[vizinho].add(atual)

            if vizinho in nos_expandidos:
                continue

            nos_folhas.add(vizinho)
            if equivalentes(atual, meta):
                estimativa[vizinho] = 0
            else:
                estimativa[vizinho] = calcula_heuristica(vizinho, meta)
        nos_expandidos.add(atual)

        grafico.atualizar(estimativa, politica)
        politica, nos_folhas = aplicar(nos_expandidos, no_pai, estimativa, problema['action'], meta)
        for p in politica:
            for i in problema['action'][politica[p]][p]:
                if i[0] != p:
                    no_pai[i[0]] = no_pai.get(i[0], set())
                    no_pai[i[0]].add(p)
#
# problema = {
# 'states': ['robot-at-x1y1', 'robot-at-x2y1', 'robot-at-x3y1', 'robot-at-x1y2', 'robot-at-x2y2', 'robot-at-x3y2', 'robot-at-x1y3', 'robot-at-x2y3', 'robot-at-x3y3'],
#
# 'action': {
# 'move-south': {'robot-at-x1y1': [('robot-at-x1y1', Decimal('1.000000'))], 'robot-at-x2y1': [('robot-at-x2y1', Decimal('1.000000'))], 'robot-at-x3y1': [('robot-at-x3y1', Decimal('1.000000'))], 'robot-at-x1y2': [('robot-at-x1y1', Decimal('0.500000')), ('robot-at-x1y2', Decimal('0.500000'))], 'robot-at-x2y2': [('robot-at-x2y1', Decimal('0.500000')), ('robot-at-x2y2', Decimal('0.500000'))], 'robot-at-x3y2': [('robot-at-x3y1', Decimal('0.500000')), ('robot-at-x3y2', Decimal('0.500000'))], 'robot-at-x1y3': [('robot-at-x1y2', Decimal('0.500000')), ('robot-at-x1y3', Decimal('0.500000'))], 'robot-at-x2y3': [('robot-at-x2y3', Decimal('1.000000'))], 'robot-at-x3y3': [('robot-at-x3y2', Decimal('0.500000')), ('robot-at-x3y3', Decimal('0.500000'))]},
#
# 'move-north': {'robot-at-x1y1': [('robot-at-x1y2', Decimal('0.500000')), ('robot-at-x1y1', Decimal('0.500000'))], 'robot-at-x2y1': [('robot-at-x2y1', Decimal('1.0000000'))], 'robot-at-x3y1': [('robot-at-x3y2', Decimal('0.500000')), ('robot-at-x3y1', Decimal('0.500000'))], 'robot-at-x1y2': [('robot-at-x1y3', Decimal('0.500000')), ('robot-at-x1y2', Decimal('0.500000'))], 'robot-at-x2y2': [('robot-at-x2y2', Decimal('1.000000'))], 'robot-at-x3y2': [('robot-at-x3y3', Decimal('0.500000')), ('robot-at-x3y2', Decimal('0.500000'))], 'robot-at-x1y3': [('robot-at-x1y3', Decimal('1.000000'))], 'robot-at-x2y3': [('robot-at-x2y3', Decimal('1.000000'))], 'robot-at-x3y3': [('robot-at-x3y3', Decimal('1.000000'))]},
#
# 'move-east': {'robot-at-x1y1': [('robot-at-x2y1', Decimal('0.500000')), ('robot-at-x1y1', Decimal('0.500000'))], 'robot-at-x2y1': [('robot-at-x3y1', Decimal('0.500000')), ('robot-at-x2y1', Decimal('0.500000'))], 'robot-at-x3y1': [('robot-at-x3y1', Decimal('1.000000'))], 'robot-at-x1y2': [('robot-at-x1y2', Decimal('1.000000'))], 'robot-at-x2y2': [('robot-at-x2y2', Decimal('1.000000'))], 'robot-at-x3y2': [('robot-at-x3y2', Decimal('1.000000'))], 'robot-at-x1y3': [('robot-at-x2y3', Decimal('0.500000')), ('robot-at-x1y3', Decimal('0.500000'))], 'robot-at-x2y3': [('robot-at-x3y3', Decimal('0.500000')), ('robot-at-x2y3', Decimal('0.500000'))], 'robot-at-x3y3': [('robot-at-x3y3', Decimal('1.000000'))]}},
# 'cost': [], 'initialstate': 'robot-at-x1y2', 'goalstate': 'robot-at-x3y3'}
#
# # aplicar(problema)
#
# LAO_star(problema, 1)