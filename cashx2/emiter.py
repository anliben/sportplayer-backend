from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms


def join_player(data, position=None):
        join_room(data.room)
        if position == None:
                emit(f'join', {'username': data.username, 'room': data.room, 'posicao':data.posicao, 'src': data.src}, broadcast=True)
                return
        emit(f'join', {'username': data.username, 'room': data.room, 'posicao':position, 'src': data.src}, broadcast=True)



def leave_player(data):
        print('saindo da sala')
        leave_room(data.room)
        emit(f'leave-{data.posicao}', {'username': data.username, 'room': data.room, 'src': data.src}, broadcast=True)
