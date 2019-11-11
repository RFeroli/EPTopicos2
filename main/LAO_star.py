import re
import hashlib
import base64
import heapq
import math
from _decimal import Decimal

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
                d.append([l[0], action])

    return d

def lista_vizinhos_operacoes(problema, estado):
    return {action:problema['action'][action][estado] for action in problema['action']}


def atualiza_custo(problema, estado, custo_estado, no_pai):

    while True:
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
        if no_pai[h_e] is None:
            return
        return
        # estado = no_pai[h_e][0]
    # atualiza_custo(problema, no_pai[h_e][0], custo_estado, no_pai)



def LAO_star(problema):

    fila_prioridade = PriorityQueue()
    inicio = problema['initialstate']
    meta = problema['goalstate']
    fila_prioridade.put(inicio, 0)
    nos_expandidos = set()
    no_pai = {}

    hsi = _gere_hash(inicio)
    contador_gerados = 1
    no_pai[hsi] = None
    custo_estado = {}
    custo_estado[hsi] = [calcula_heuristica(inicio, meta),inicio]
    meta_plano = []

    while not fila_prioridade.empty():
        atual = fila_prioridade.get()
        hatual = _gere_hash(atual)
        if hatual in nos_expandidos:
            continue

        nos_expandidos.add(hatual)
        if equivalentes(atual, meta):
            hsi = _gere_hash(atual)
            while no_pai[hsi] is not None:
                meta_plano.insert(0, no_pai[hsi])
                hsi = _gere_hash(no_pai[hsi][0])
            break


        for vizinho_op in lista_vizinhos(problema, atual):
            vizinho = vizinho_op[0]
            operacao = vizinho_op[1]
            vizinho_h= _gere_hash(vizinho)
            novo_custo = calcula_heuristica(vizinho, meta)

            if vizinho_h not in nos_expandidos:
                custo_estado[vizinho_h] = [novo_custo, vizinho]
                contador_gerados += 1
                no_pai[vizinho_h] = [atual, operacao]
                fila_prioridade.put(vizinho, novo_custo)

        atualiza_custo(problema, atual, custo_estado, no_pai)
    # Esses dicionarios sao usados para extrair a solucao
    # return came_from, custo_neste_momento, nos_expandidos
    return meta_plano, contador_gerados



# problema = {
# 'states': ['robot-at-x1y1', 'robot-at-x2y1', 'robot-at-x3y1', 'robot-at-x1y2', 'robot-at-x2y2', 'robot-at-x3y2', 'robot-at-x1y3', 'robot-at-x2y3', 'robot-at-x3y3'],
#
# 'action': {
# 'move-south': {'robot-at-x1y1': [('robot-at-x1y1', Decimal('1.000000'))], 'robot-at-x2y1': [('robot-at-x2y1', Decimal('1.000000'))], 'robot-at-x3y1': [('robot-at-x3y1', Decimal('1.000000'))], 'robot-at-x1y2': [('robot-at-x1y1', Decimal('0.500000')), ('robot-at-x1y2', Decimal('0.500000'))], 'robot-at-x2y2': [('robot-at-x2y1', Decimal('0.500000')), ('robot-at-x2y2', Decimal('0.500000'))], 'robot-at-x3y2': [('robot-at-x3y1', Decimal('0.500000')), ('robot-at-x3y2', Decimal('0.500000'))], 'robot-at-x1y3': [('robot-at-x1y2', Decimal('0.500000')), ('robot-at-x1y3', Decimal('0.500000'))], 'robot-at-x2y3': [('robot-at-x2y3', Decimal('1.000000'))], 'robot-at-x3y3': [('robot-at-x3y2', Decimal('0.500000')), ('robot-at-x3y3', Decimal('0.500000'))]},
#
# 'move-north': {'robot-at-x1y1': [('robot-at-x1y2', Decimal('0.500000')), ('robot-at-x1y1', Decimal('0.500000'))], 'robot-at-x2y1': [('robot-at-x2y1', Decimal('1.0000000'))], 'robot-at-x3y1': [('robot-at-x3y2', Decimal('0.500000')), ('robot-at-x3y1', Decimal('0.500000'))], 'robot-at-x1y2': [('robot-at-x1y3', Decimal('0.500000')), ('robot-at-x1y2', Decimal('0.500000'))], 'robot-at-x2y2': [('robot-at-x2y2', Decimal('1.000000'))], 'robot-at-x3y2': [('robot-at-x3y3', Decimal('0.500000')), ('robot-at-x3y2', Decimal('0.500000'))], 'robot-at-x1y3': [('robot-at-x1y3', Decimal('1.000000'))], 'robot-at-x2y3': [('robot-at-x2y3', Decimal('1.000000'))], 'robot-at-x3y3': [('robot-at-x3y3', Decimal('1.000000'))]},
#
# 'move-east': {'robot-at-x1y1': [('robot-at-x2y1', Decimal('0.500000')), ('robot-at-x1y1', Decimal('0.500000'))], 'robot-at-x2y1': [('robot-at-x3y1', Decimal('0.500000')), ('robot-at-x2y1', Decimal('0.500000'))], 'robot-at-x3y1': [('robot-at-x3y1', Decimal('1.000000'))], 'robot-at-x1y2': [('robot-at-x1y2', Decimal('1.000000'))], 'robot-at-x2y2': [('robot-at-x2y2', Decimal('1.000000'))], 'robot-at-x3y2': [('robot-at-x3y2', Decimal('1.000000'))], 'robot-at-x1y3': [('robot-at-x2y3', Decimal('0.500000')), ('robot-at-x1y3', Decimal('0.500000'))], 'robot-at-x2y3': [('robot-at-x3y3', Decimal('0.500000')), ('robot-at-x2y3', Decimal('0.500000'))], 'robot-at-x3y3': [('robot-at-x3y3', Decimal('1.000000'))]}}, 'cost': [], 'initialstate': 'robot-at-x1y2', 'goalstate': 'robot-at-x3y3'}
#
#
# LAO_star(problema)