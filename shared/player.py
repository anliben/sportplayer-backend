from .observador import Observador
from  kivy.storage.jsonstore import JsonStore
from .carta import Carta

db = JsonStore("db.json")

class Player(Observador):

    def __init__(self, data):
        self.username = data['username']
        self.room = data['room']
        self.src = data['src']
        self.posicao = ''
        self.friend = ''
        self.rival1 = ''
        self.rival2 = ''
        self.id = ''
        self.mao = []
        self.pontos = 0
        self.rodadas = 0
        self.primeiro = False
        self.ultimo = False
        self.countCartas = 0
        self.cartasJogadas = []
    
    def criarMao(self, baralho):
        for i in range(3):
            self.mao.append(baralho.retirarCarta())
        return self

    def jogarCarta(self, carta_escolhida):
        for i in self.mao:
            if i.retornarNumero() == carta_escolhida['numero'] and i.retornarNaipe() == carta_escolhida['naipe']:
                self.cartasJogadas.append(carta_escolhida)
                self.countCartas += 1
                self.mao.pop(self.mao.index(i))
                return True

    def limparCartasJogadas(self):
        self.cartasJogadas.clear()
       
    
    def countCartasJogadas(self):
        self.countCartas += 1

    def mostrarMao(self):
        for carta in self.mao:
            carta.printarCarta()
    
    def retornarMao(self):
        hands = []
        count = 0
        for carta in self.mao:
            hands.append({
               'numero': carta.retornarNumero(),
               'naipe': carta.retornarNaipe(),
               'index': count
            })
            count += 1
        return hands
    
    def adicionarPonto(self):
        print('adicionando ponto')
        self.pontos += 3
        #self.cartasJogadas = []
    
    def adicionarRodada(self):
        self.rodadas += 1
        print('adicionando rodada para ', self.username)

    def resetarRodada(self):
        self.rodadas = 0
    
    def resetar(self):
        self.pontos = 0
        self.mao = []

    def resetarMao(self):
        self.mao = []

    def update(self):
        print(f'-------------- {self.username} -------------------------------')
        print(
            'username: {}, posicao: {}, room: {}, src: {}, mao: {}, pontos: {}, rodadas: {}, primeiro: {}, ultimo: {}, friend: {}, rival1: {}, rival2: {}, id: {}, countCartas: {}, cartasJogadas: {}'.format(
                self.username,
                self.posicao,
                self.room,
                self.src,
                self.mao,
                self.pontos,
                self.rodadas,
                self.primeiro,
                self.ultimo,
                self.friend,
                self.rival1,
                self.rival2,
                self.id,
                self.countCartas,
                self.cartasJogadas
            )
        )
        print('-------------------------------------------------------')

    def subscribe(self):
        print('Opa, estou online')

    def unsubscribe(self):
        print('Opa, estou online')

    def join(self, position=None):
        self.update_db('insert')

    def leave(self):
        self.update_db('delete')
    
    def update_db(self, query):
        if query == 'insert':
            db.put(self.username, username=self.username, position=self.posicao, src=self.src, room=self.room)    
            return
        if db.exists(self.username):
            db.delete(self.username)
    
    def data(self):
        return {
            'username': self.username,
            'posicao': self.posicao,
            'room': self.room,
            'src': self.src,
            'mao': self.retornarMao(),
            'pontos': self.pontos,
            'rodadas': self.rodadas,
            'primeiro': self.primeiro,
            'ultimo': self.ultimo,
            'friend': self.friend,
            'rival1': self.rival1,
            'rival2': self.rival2,
            'id': self.id,
            'countCartas': self.countCartas,
            'cartasJogadas': self.cartasJogadas
        }
