# G = {1: [2, 3], 2: [3], 3:[2, 4], 4:[5, 6], 5: [4, 6], 7:[8], 8:[7]}
G = {1: [2], 2: [3, 4, 5], 3:[4], 5:[4], 6:[5], 4:[7]}
print(G)
controle = {v: 0 for v in range(1, 9)}

lista = []
def ordenacao(G, controle, no, lista):
    controle[no] = 1
    for i in G.get(no,[]):
        if controle[i] ==0:
            ordenacao(G, controle, i, lista)
    controle[no] = 2
    print(no)
    lista.append(no)

for i in G:
    if controle[i] == 0:
        # print(i)
        ordenacao(G, controle, i, lista)
print(lista)
exit()

def busca_conexao(G, controle, no):
    if controle[no] > 0:
        return
    controle[no] = 1
    for filho in G.get(no, []):
        busca_conexao(G, controle, filho)
    controle[no] = 2


def busca_conexao_conjunto(G, controle, no, conjunto):
    if controle[no] > 0:
        return
    conjunto.add(no)
    controle[no] = 1
    for filho in G.get(no, []):
        busca_conexao_conjunto(G, controle, filho, conjunto)
    controle[no] = 2

def inverte_grafo(G):
    g_novo = {}
    for i in G:
        for e in G[i]:
            if e not in g_novo:
                g_novo[e] = []
            g_novo[e].append(i)
    return g_novo

for i in range(1, 9):
    if i in G and controle[i] ==0:
        busca_conexao(G, controle, i)
print(G)
GIN = inverte_grafo(G)
print(GIN)
controle = {v: 0 for v in range(1, 9)}
l = []
for i in range(1, 9):
    if controle[i] ==0:
        s = set()
        busca_conexao_conjunto(GIN, controle, i, s)
        l.append(s)

print(l)


exit()


def busca(G, controle, no):
    print(no)
    if controle[no] == 1:
        return False

    if controle[no] == 2:
        return True
    controle[no] = 1

    for filho in G.get(no, []):
        v = busca(G, controle, filho)
        if not v:
            return v
    controle[no] = 2
    return True

for i in G:
    b = busca(G, controle, i)
    if not b:
        print('ciclo')
        print(controle)

        exit()
print(controle)
print('Aclicico')
