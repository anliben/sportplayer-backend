from pprint import pprint
import random
from shared.player import Player
from .engine import Engine
from shared.baralho import Baralho
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms

engine = Engine()


class SocketCashGamex1:
    def __init__(self, socket):
        self.socket = socket
        self.room = self.socket['room']
        join_room(self.room)


        if self.socket['request'] == 'addPlayer':
            self.insertPlayer()

        elif self.socket['request'] == 'jogarCarta':
            self.jogarCarta()
        
        players = engine.find_player_begin(self.room)
        for i in players:
            i.update()


    def jogarCarta(self):
        manilha = self.socket['manilha']
        numero = self.socket['carta']['numero']
        naipe = self.socket['carta']['naipe']
        index = self.socket['carta']['index']

        player = engine.find_player('1')

        engine.jogarCarta(
            self.socket['room'],
            {
                'numero': numero, 'naipe': naipe,
                'index': index}, self.socket['jogador'])
                        
        #engine.countCartasJogadas(self.socket['room'], self.socket['jogador'])

        emit('jogarCarta', {
            'numero': numero,
            'naipe': naipe,
            'index': index,
            'jogador': self.socket['jogador'],
            'jogadores': [player[0], player[1]]
        }, broadcast=True)
        
        if len(player[0]['mao']) == 0 and len(player[1]['mao']) == 0:
            self.nova_rodada('1')
        try:
            ganhador = engine.verificarGanhador(
                player[0]['cartasJogadas'][-1],
                player[1]['cartasJogadas'][-1],
                manilha)
            engine.adicionarRodada('1',
                                   player[0]['cartasJogadas'][0],
                                   player[1]['cartasJogadas'][0], ganhador)

            engine.limparCartaJogada('1')

            players = engine.find_player('1')
            if player[0]['rodadas'] >= 2:
                engine.adicionarPonto('1', player[0]['username'])
                self.nova_rodada('1')
            if player[1]['rodadas'] >= 2:
                engine.adicionarPonto('1', player[1]['username'])
                self.nova_rodada('1')
            emit('rodada', {
                'jogadores': players
            }, broadcast=True)
        except:
            pass
        if player[0]['rodadas'] >= 2:
            engine.adicionarPonto('1', player[0]['username'])
            self.nova_rodada('1')
        if player[1]['rodadas'] >= 2:
            engine.adicionarPonto('1', player[1]['username'])
            self.nova_rodada('1')

    def nova_rodada(self, room):
        baralho = Baralho()
        baralho.embaralhar()
        baralho.definirVira(baralho)
        manilha = baralho.definirManilha()
        baralho.definirManilhas(manilha)
        players = engine.find_player_begin(room)
        players[0].criarMao(baralho)
        players[1].criarMao(baralho)
        players[0].rodadas = 0
        players[1].rodadas = 0
        player = engine.find_player(room)
        emit('novaMao', {
            'jogadores': [
                player[0],
                player[1]]
        }, broadcast=True)

    def insertPlayer(self):
        player = Player(self.socket)
        engine.insertPlayer(player)

        players = engine.find_player('1')

        if len(players) >= 2:
            jogador1, jogador2, vira, manilha = self.organizar_playersx1()
            print('jogador1', jogador1)
            print('jogador2', jogador2)

            emit('findPlayersx1', {
                'jogadores': [jogador1.data(), jogador2.data()],
                'vira': vira,
                'manilha': manilha,
            }, broadcast=True)

    def organizar_playersx1(self):
        baralho = Baralho()
        baralho.embaralhar()
        baralho.definirVira(baralho)
        manilha = baralho.definirManilha()
        baralho.definirManilhas(manilha)

        jogador = engine.criarMaoJogador(self.room)

        vira = baralho.retornaVira()
        manilha = baralho.retornaManilhas()
        if jogador[0].rodadas == 0 and jogador[1].rodadas == 0:
            if jogador[0].pontos == 0 and jogador[1].pontos == 0:
                jogadores = ['jogador1', 'jogador2']
                sorteado = random.choice(jogadores)
                if sorteado == 'jogador1':
                    jogador[0].primeiro = True
                    jogador[1].ultimo = True
                elif sorteado == 'jogador2':
                    jogador[1].primeiro = True
                    jogador[0].ultimo = True

        return [jogador[0], jogador[1], vira, manilha]
