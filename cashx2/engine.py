from typing import Type
from shared.observador import Observador
from shared.baralho import Baralho
from shared.carta import Carta
from shared.jogo import Jogo
import random
import os

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
        p[2].criarMao(baralho)
        p[3].criarMao(baralho)
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
        for player in self.players:
            if player.username == username:
                return player.jogarCarta(carta_escolhida)

    def countCartasJogadas(self, room, jogador):
        for player in self.players:
            if player.username == jogador:
                player.countCartasJogadas()

    def organizar_jogo(self,p1,p2,p3,p4):
        jogo = Jogo()
        baralho = Baralho()
        baralho.embaralhar()
        baralho.definirVira(baralho)
        manilha = baralho.definirManilha()
        baralho.definirManilhas(manilha)

        jogador1 = jogo.criarJogador(p1['username'], baralho)
        jogador2 = jogo.criarJogador(p2['username'], baralho)
        jogador3 = jogo.criarJogador(p3['username'], baralho)
        jogador4 = jogo.criarJogador(p4['username'], baralho)
        """ 
        p1.mao = jogador1.retornarMao()
        p2.mao = jogador2.retornarMao()
        p3.mao = jogador3.retornarMao()
        p4.mao = jogador4.retornarMao() """

        return [ jogador1, jogador2, jogador3, jogador4 ]

    def verificarGanhador(self, carta1, carta2, carta3, carta4, manilha):
        #Verifica se a carta 1 e a carta 3 são manilhas
        if carta1.numero == manilha and carta3.numero == manilha: #posso tirar o .numero ???
            ganhador = carta1.verificarManilha(carta1, carta3)
            #Se a carta 1 for maior que a carta 3
            if carta1 == ganhador:
                #Verifica se a carta 2 e a carta 4 são manilhas
                if carta2.numero == manilha and carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta2, carta4)
                    if ganhador == carta2:
                        ganhador = carta1.verificarManilha(carta1, carta2)
                        return ganhador
                    else:
                        ganhador = carta1.verificarManilha(carta1, carta4)
                        return ganhador
                elif carta2.numero == manilha:
                    ganhador = carta1.verificarManilha(carta1, carta2)
                    return ganhador
                elif carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta1, carta4)
                    return ganhador
            #Se a carta 3 for maior que a carta 1
            else:
                if carta2.numero == manilha and carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta2, carta4)
                    if ganhador == carta2:
                        ganhador = carta1.verificarManilha(carta3, carta2)
                        return ganhador
                    else:
                        ganhador = carta1.verificarManilha(carta3, carta4)
                        return ganhador
                elif carta2.numero == manilha:
                    ganhador = carta1.verificarManilha(carta3, carta2)
                    return ganhador
                elif carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta3, carta4)
                    return ganhador
        #Se a carta 1 for manilha
        elif carta1.numero == manilha:
                if carta2.numero == manilha and carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta2, carta4)
                    if ganhador == carta2:
                        ganhador = carta1.verificarManilha(carta1, carta2)
                        return ganhador
                    else:
                        ganhador = carta1.verificarManilha(carta1, carta4)
                        return ganhador
                elif carta2.numero == manilha:
                    ganhador = carta1.verificarManilha(carta1, carta2)
                    return ganhador
                elif carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta1, carta4)
                    return ganhador
                else:
                    ganhador = carta1
                    return ganhador
        #Se a carta 3 são manilha
        elif carta3.numero == manilha:
                if carta2.numero == manilha and carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta2, carta4)
                    if ganhador == carta2:
                        ganhador = carta1.verificarManilha(carta3, carta2)
                        return ganhador
                    else:
                        ganhador = carta1.verificarManilha(carta3, carta4)
                        return ganhador
                elif carta2.numero == manilha:
                    ganhador = carta1.verificarManilha(carta3, carta2)
                    return ganhador
                elif carta4.numero == manilha:
                    ganhador = carta1.verificarManilha(carta3, carta4)
                    return ganhador
                else:
                    ganhador = carta3
                    return ganhador
        #Se a carta 2 ou a carta 4 são manilha
        elif carta2.numero == manilha and carta4.numero == manilha:
            ganhador = carta1.verificarManilha(carta2, carta4)
            return ganhador
        #Se a carta 2 for manilha
        elif carta2.numero == manilha:
            ganhador = carta2
            return ganhador
        #Se a carta 4 for manilha
        elif carta4.numero == manilha:
            ganhador = carta4
            return ganhador
        #Se nenhuma carta for manilha
        else:
            dupla1 = carta1.verificarCarta(carta1, carta3)
            if dupla1 == "Empate":
                dupla1 = carta1
            dupla2 = carta1.verificarCarta(carta2, carta4)
            if dupla2 == "Empate":
                dupla2 = carta2
            ganhador = carta1.verificarCarta(dupla1, dupla2)
            if ganhador == "Empate":
                return "Empate"
            else:
                return ganhador
    
    def quemJogaPrimeiro(self, jogador1, jogador2, jogador3, jogador4, carta1, carta2, carta3, carta4, ganhador): 
        if carta1 == ganhador:
            jogador1.primeiro = True
            jogador2.primeiro = False
            jogador3.primeiro = False
            jogador4.primeiro = False
        elif carta2 == ganhador:
            jogador1.primeiro = False
            jogador2.primeiro = True
            jogador3.primeiro = False
            jogador4.primeiro = False
        elif carta3 == ganhador:
            jogador1.primeiro = False
            jogador2.primeiro = False
            jogador3.primeiro = True
            jogador4.primeiro = False
        elif carta4 == ganhador:
            jogador1.primeiro = False
            jogador2.primeiro = False
            jogador3.primeiro = False
            jogador4.primeiro = True
        elif ganhador == "Empate":
            pass
    
    def adicionarPonto(self, room, carta1, carta2, carta3, carta4, ganhador):
        players = []
        for player in self.players:
            if player.room == room:
                players.append(player)
        if ganhador == "Empate":
            players[0].adicionarPonto()
            players[1].adicionarPonto()
            players[2].adicionarPonto()
            players[3].adicionarPonto()
            return "Empate"
        elif ganhador == carta1 or ganhador == carta3:
            players[0].adicionarPonto()
            players[1].adicionarPonto()
        elif ganhador == carta2 or ganhador == carta4:
            players[2].adicionarPonto()
            players[3].adicionarPonto()
        else:
            return "Erro"
    def adicionarRodada(self, room):
        for player in self.players:
            if player.room == room:
                player.adicionarRodada()
                
    def resetarRodada(self, room):
        for player in self.players:
            if player.room == room:
                player.resetarRodada()
                

    def quemIniciaRodada(self, jogador1, jogador2, jogador3, jogador4):
        if jogador1.pontos == 0 and jogador2.pontos == 0:
            if jogador1.ultimo == True:
                jogador2.ultimo = True
                jogador1.ultimo = False
                jogador1.primeiro = True
                jogador2.primeiro = False
                jogador3.primeiro = False
                jogador4.primeiro = False
            elif jogador2.ultimo == True:
                jogador3.ultimo = True
                jogador2.ultimo = False
                jogador1.primeiro = False
                jogador2.primeiro = True
                jogador3.primeiro = False
                jogador4.primeiro = False
            elif jogador3.ultimo == True:
                jogador4.ultimo = True
                jogador3.ultimo = False
                jogador1.primeiro = False
                jogador2.primeiro = False
                jogador3.primeiro = True
                jogador4.primeiro = False
            elif jogador4.ultimo == True:
                jogador1.ultimo = True
                jogador4.ultimo = False
                jogador1.primeiro = False
                jogador2.primeiro = False
                jogador3.primeiro = False
                jogador4.primeiro = True   