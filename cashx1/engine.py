from pprint import pprint
from typing import Type
from shared.observador import Observador
from shared.jogo import Jogo
from shared.baralho import Baralho
from shared.carta import Carta

class Engine:

    def __init__(self):
        self.players = []

    def insertPlayer(self, player: Type[Observador]):
        self.players.append(player)

    def criarMaoJogador(self, room):
        baralho = Baralho()
        baralho.embaralhar()
        baralho.definirVira(baralho)
        manilha = baralho.definirManilha()
        baralho.definirManilhas(manilha)
        p = []
        for player in self.players:
            if player.room == room:
                p.append(player)
        p[0].criarMao(baralho)
        p[1].criarMao(baralho)
        return p
    
    def limparCartaJogada(self, room):
        for player in self.players:
            if player.room == room:
                player.limparCartasJogadas()

    def resetarMao(self, room):
        for player in self.players:
            if player.room == room:
                player.resetarMao()
    
    def join_room(self):
        for player in self.players:
            if player.posicao == 'bottom':
                player.join('top')
            else:
                player.join()

    def leave_room(self):
        for player in self.players:
            player.leave()
    
    def update_player(self):
        for player in self.players:
            return player.data()

    def find_player(self, room):
        arr_player = []
        for player in self.players:
            if player.room == room:
                arr_player.append(player.data())
        return arr_player

    def find_One_Player(self, username):
        for player in self.players:
            if player.username == username:
                return player
    
    def find_player_begin(self, room):
        arr_player = []
        for player in self.players:
            if player.room == room:
                arr_player.append(player)
        return arr_player

    def jogarCarta(self, room, carta_escolhida, username):
        print("carta escolhida: ", carta_escolhida)
        for player in self.players:
            if player.username == username:
                return player.jogarCarta(carta_escolhida)

    def countCartasJogadas(self, room, jogador):
        for player in self.players:
            if player.username == jogador:
                player.countCartasJogadas()

    def organizar_jogo(self,p1,p2):
        jogo = Jogo()
        baralho = Baralho()
        baralho.embaralhar()
        baralho.definirVira(baralho)
        manilha = baralho.definirManilha()
        baralho.definirManilhas(manilha)

        jogador1 = jogo.criarJogador(p1['username'], baralho)
        jogador2 = jogo.criarJogador(p2['username'], baralho)

        return [ jogador1, jogador2 ]

    def verificarGanhador(self, carta1, carta2, manilha):
        carta1 = Carta(carta1['numero'], carta1['naipe'])
        carta2 = Carta(carta2['numero'], carta2['naipe'])
        if carta1.retornarNumero() == manilha and carta2.retornarNumero() == manilha: #posso tirar o .numero ???
            ganhador = carta1.verificarManilha(carta1, carta2)
            return ganhador
        else:
            ganhador = carta1.verificarCarta(carta1, carta2)
            return ganhador
    
    def quemJogaPrimeiro(self, jogador1, jogador2, carta1, carta2, ganhador): 
        if carta1 == ganhador:
            jogador1.primeiro = True
            jogador2.primeiro = False
        elif carta2 == ganhador:
            jogador1.primeiro = False
            jogador2.primeiro = True
        elif ganhador == "Empate":
            pass
    
    def adicionarPonto(self, room, username, score: int) -> None:
        for player in self.players:
            if player.room == room and player.username == username:
                player.adicionarPonto(score)

    def adicionarRodada(self, room, carta1,carta2, ganhador):
        carta1 = Carta(carta1['numero'], carta1['naipe'])
        carta2 = Carta(carta2['numero'], carta2['naipe'])
        players = []
        for player in self.players:
            if player.room == room:
                players.append(player)
        pprint(players)
        if ganhador.retornarNumero() == carta1.retornarNumero() and ganhador.retornarNaipe() == carta1.retornarNaipe():
            players[0].adicionarRodada()
            print("jogador 1 ganhou")
        elif ganhador.retornarNumero() == carta2.retornarNumero() and ganhador.retornarNaipe() == carta2.retornarNaipe():
            players[1].adicionarRodada()
            print("jogador 2 ganhou")
        else:
            players[1].adicionarRodada()
            players[0].adicionarRodada()
            print("empate")

    def resetarRodada(self, room):
        for player in self.players:
            if player.room == room:
                player.resetarRodada()
                

    def quemIniciaRodada(self, jogador1, jogador2):
        if jogador1.pontos == 0 and jogador2.pontos == 0:
            if jogador1.ultimo == True:
                jogador2.ultimo = True
                jogador1.ultimo = False
                jogador1.primeiro = True
                jogador2.primeiro = False
            elif jogador2.ultimo == True:
                jogador2.ultimo = False
                jogador1.primeiro = False
                jogador2.primeiro = True