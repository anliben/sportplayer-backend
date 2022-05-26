from .carta import Carta
import random

class Baralho():
    """Modulo de Baralho para organizar o baralho
    FUNCS:
        - crirarBaralho()
        - embaralhar()
        - definirVira()
        - definirManilha()
        - definirManilhas()
        - retirarCarta()
        - resetarBaralho()
        - retornaVira()
        - retornaManilhas()
        - retornarBaralho()
    """

    def __init__(self):
        self.vira = []
        self.manilhas = []
        self.cartas = []
        self.criarBaralho()

    def criarBaralho(self):
        """Criação do baralho

        NOTE: for i in ["paus", "copas", "espadas", "ouros"]:
            for n in range(1, 14):
                if n < 8 or n > 10:
                    self.cartas.append(Carta(n, i))
        """        
        for i in ["paus", "copas", "espadas", "ouros"]:
            for n in range(1, 14):
                if n < 8 or n > 10:
                    self.cartas.append(Carta(n, i))
    
    def embaralhar(self):
        """Embaralhar as cartas

        NOTE: random.shuffle(self.cartas)
        """        
        random.shuffle(self.cartas)
    
    def definirVira(self, baralho):
        """Definir a vira

        NOTE: para definir a vira precisa de um baralho

        Args:
            baralho (Baralho): Retira uma carta do baralho e coloca na vira
        """        
        self.vira.append(baralho.retirarCarta())

    def definirManilha(self):
        """Definir a Manilha do jogo

        Returns:
            numero: devolve o numero da manilha
        """        
        for v in self.vira:
            if v.retornarNumero() == 7:
                return 11
            elif v.retornarNumero() == 13:
                return 1
            else:
                return v.numero + 1

    def definirManilhas(self, manilha):
        """Definir as manilhas

        Args:
            manilhas (number): devolve o numero de todas as manilhas
        """        
        for m in self.cartas:
            x = m.retornarNumero()
            if x == manilha:
                self.manilhas.append(m)

    def retirarCarta(self):
        """Retirna uma carta do baralho

        Returns:
            Carta: retorna a carta retirada
        """        
        return self.cartas.pop()
    
    def resetarBaralho(self):
        """Reseta o baralho
        NOTE:
            self.cartas = []
            self.manilhas = []
            self.cartas = []
        """        
        self.vira = []
        self.manilhas = []
        self.cartas = []

    def retornaVira(self):
        """Retorna a vira
        
        NOTE: Para cada carta em self.vira, retorna a carta

        Returns:
            Carta: Retorna uma carta que será considerada a vira
        """        
        vira = []
        for v in self.vira:
            vira.append(v.retornarCarta())
        return vira

    def retornaManilhas(self):
        """Retornar as manilhas

        NOTE:
            Para cada carta em self.manilhas, adiciona manilha em manilhas e retorna a Manilhas

        Returns:
            Menilhas: Manilhas do jogo
        """        
        manilhas = []
        for m in self.manilhas:
            manilhas.append(m.retornarCarta())
        return manilhas

    def retornarBaralho(self):
        """Retornar o baralho

        NOTE:
            Para cada carta em self.cartas, e retorna a carta
        """        
        for c in self.cartas:
            c.retornarCarta()
