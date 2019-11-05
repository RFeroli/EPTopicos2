from main import Roleta

class acao:
    def __init__(self,dict):
        self.func={}

        for chaveEstado in dict:
            self.func[chaveEstado]=Roleta.roleta()
            for imagem in dict[chaveEstado]:
                self.func[chaveEstado].adicionar(imagem[0],imagem[1])


    def aplicar(self,dominio):
        if(dominio not in self.func):
            #problema ponto da funcao nao definido
            return
        return self.func[dominio].sortear()

