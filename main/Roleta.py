import  random
class roleta:

    class item:
        def __init__(self,valor,probabilidade):
            self.valor=valor
            self.probabilidade=probabilidade

    def __init__(self):
        self.soma=0
        self.itens=[]


    def adicionar(self,valor,probabilidade):
        self.soma+=probabilidade
        self.itens.append(self.item(valor,probabilidade))

    def sortear(self):
        agulha= random.uniform(0, 1)*self.soma;
        parcial=0
        for item in self.itens:
            parcial += item.probabilidade
            if(agulha<=parcial):
                return item.valor





r=roleta()

r.adicionar("batata",10)
r.adicionar("pate",10)
r.adicionar("biscoito",10)
r.adicionar("pure",10)

batata=0
pate=0
biscoito=0

qtd=10
for i in range(qtd):
    s=r.sortear()
    if s =="batata":
        batata+=1
    if s =="pate":
        pate+=1
    if s =="biscoito":
        biscoito+=1


print("batata",(batata/qtd)*100,"%")
print("pate",(pate/qtd)*100,"%")
print("biscoito",(biscoito/qtd)*100,"%")


