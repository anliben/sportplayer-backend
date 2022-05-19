from socket import socket
from flask import Flask, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from flask_cors import CORS
from kivy.storage.jsonstore import JsonStore
from cashx1.engine import Engine
from shared.player import Player
from shared.baralho import Baralho
from shared.carta import Carta
import random
from random import choice
import string
from pprint import pprint
from cashx1.entrada import SocketCashGamex1

engine = Engine()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ADSDASDASD4234X3'
cors = CORS(app, resources={r"*": {"origins": "*"}})

socket = SocketIO(app, cors_allowed_origins='*')

db = JsonStore("db.json")


def gerador_id(tamanho):
    valores = string.ascii_lowercase
    senha = ''
    for i in range(tamanho):
        senha += choice(valores)
    return senha


@socket.on('connect')
def connect(auth):
    print(auth)
    print('alguem connectados')


@socket.on('jogarCarta')
def hand(data):
    manilha = data['manilha']
    engine.jogarCarta(data['room'], {'numero': data["carta"]["numero"], 'naipe': data["carta"]["naipe"],
                                     'index': data["carta"]["index"]}, data['jogador'])

    player = engine.find_player('1')
    socket.emit('jogarCarta', {
        'numero': data["carta"]["numero"],
        'naipe': data["carta"]["naipe"],
        'index': data["carta"]["index"],
        'jogador': data['jogador'],
        'jogadores': [player[0], player[1], player[2], player[3]]
    })

    pprint(player[0])
    pprint(player[1])
    pprint(player[2])
    pprint(player[3])

    if len(player[0]['cartasJogadas']) == 1 and len(player[1]['cartasJogadas']) == 1 and len(
            player[2]['cartasJogadas']) == 1 and len(player[3]['cartasJogadas']) == 1:
        ganhador = engine.verificarGanhador(
            player[0]['cartasJogadas'][0],
            player[1]['cartasJogadas'][0],
            player[2]['cartasJogadas'][0],
            player[3]['cartasJogadas'][0], manilha)
        engine.adicionarPonto('1',
                              player[0]['cartasJogadas'][0],
                              player[1]['cartasJogadas'][0],
                              player[2]['cartasJogadas'][0],
                              player[3]['cartasJogadas'][0],
                              ganhador)
        engine.adicionarRodada('1')
        engine.limparCartaJogada('1')
        players = engine.find_player('1')
        socket.emit('rodada', {
            'jogadores': players
        })
    if len(player[0]['mao']) == 0 and len(player[1]['mao']) == 0 and len(player[2]['mao']) == 0 and len(
            player[3]['mao']) == 0:
        nova_rodada('1')


def nova_rodada(room):
    baralho = Baralho()
    baralho.embaralhar()
    baralho.definirVira(baralho)
    manilha = baralho.definirManilha()
    baralho.definirManilhas(manilha)
    players = engine.find_player_begin(room)
    players[0].criarMao(baralho)
    players[1].criarMao(baralho)
    players[2].criarMao(baralho)
    players[3].criarMao(baralho)
    player = engine.find_player(room)
    engine.resetarRodada(room)
    socket.emit('novaMao', {
        'jogadores': [
            player[0],
            player[1],
            player[2],
            player[3]]
    })


@socket.on('join_room')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('playerId', {'id': gerador_id(20)})


@socket.on('findPlayer')
def on_findPlayers(data):
    player = engine.find_player(data['room'])
    print(player)
    # emitir player na sala atual
    if player:
        emit('findPlayers', player)


@socket.on('addPlayerCashGameX1')
def on_addPlayer(data):
    SocketCashGamex1(data)


@socket.on('cartaPlayerCashGameX1')
def on_cartaPlayer(data):
    SocketCashGamex1(data)


@socket.on('insertPlayer')
def on_insertPlayer(data):
    print(data)
    room = '1'
    join_room(room)
    send('insertPlayer', to=room)
    player = Player(data)
    engine.insertPlayer(player)

    players = engine.find_player('1')

    if len(players) >= 4 and len(players) <= 4:
        players[0]['friend'] = players[1]['username']
        players[1]['friend'] = players[0]['username']

        players[2]['friend'] = players[3]['username']
        players[3]['friend'] = players[2]['username']

        players[0]['rival1'] = players[2]['username']
        players[0]['rival2'] = players[3]['username']

        players[1]['rival1'] = players[2]['username']
        players[1]['rival2'] = players[3]['username']
        players[2]['rival1'] = players[0]['username']

        players[2]['rival2'] = players[1]['username']
        players[3]['rival1'] = players[0]['username']
        players[3]['rival2'] = players[1]['username']

        jogador1, jogador2, jogador3, jogador4, vira, manilha = organizar_players('1')

        jogador1.friend = jogador2.username
        jogador2.friend = jogador1.username
        jogador3.friend = jogador4.username
        jogador4.friend = jogador3.username

        jogador1.rival1 = jogador3.username
        jogador1.rival2 = jogador4.username

        jogador2.rival1 = jogador3.username
        jogador2.rival2 = jogador4.username

        jogador3.rival1 = jogador1.username
        jogador3.rival2 = jogador2.username

        jogador4.rival1 = jogador1.username
        jogador4.rival2 = jogador2.username

        socket.emit('findPlayers', {
            'jogadores': [jogador1.data(), jogador2.data(), jogador3.data(), jogador4.data()],
            'vira': vira,
            'manilha': manilha,
        }, broadcast=True)


def organizar_players(room):
    baralho = Baralho()
    baralho.embaralhar()
    baralho.definirVira(baralho)
    manilha = baralho.definirManilha()
    baralho.definirManilhas(manilha)

    jogador = engine.criarMaoJogador(room)

    vira = baralho.retornaVira()
    manilha = baralho.retornaManilhas()
    if jogador[0].rodadas == 0 and jogador[1].rodadas == 0:
        if jogador[0].pontos == 0 and jogador[1].pontos == 0:
            jogadores = ["jogador1", "jogador2", "jogador3", "jogador4"]
            sorteado = random.choice(jogadores)
            if sorteado == "jogador1":
                jogador[0].primeiro = True
                jogador[1].ultimo = True
            elif sorteado == "jogador2":
                jogador[1].primeiro = True
                jogador[2].ultimo = True
            elif sorteado == "jogador3":
                jogador[2].primeiro = True
                jogador[3].ultimo = True
            else:
                jogador[3].primeiro = True
                jogador[0].ultimo = True

    return [jogador[0], jogador[1], jogador[2], jogador[3], vira, manilha]


if __name__ == '__main__':
    socket.run(app, host='192.168.1.102', port=3000, debug=True)

