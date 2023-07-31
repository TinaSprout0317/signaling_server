import eventlet
import socketio
import ifcfg
import json

clients = []
numClients = 0

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.on('message')
def message(sid, message):
    print('Client said: ', message)
    print('Client ID ', sid)
    sio.emit('message', message)

@sio.on('create or join')
def create_room(sid, room):
    print('Received request to create or join room ' + room)
    numClients = len(clients)
    if sid in clients:
        print('Client ' + sid + ' already in room')
    else:
        clients.append(sid)
    print('Room ' + room + ' now has ' + str(numClients) + ' client(s)')
    print('Client sid list :')
    print(clients)
    if (numClients == 0):
        sio.enter_room(sid, room)
        print('Client ID ' + str(sid) + ' created room ' + room)
        sio.emit('created', room, sid)
    elif ( numClients == 1):
        print('Client ID ' + str(sid) + ' joined room ' + room)
        sio.emit(event = 'join', room=room)
        sio.enter_room(sid, room)
        sio.emit(event = 'joined', to = sid)
    else:
        sio.emit('full', to = sid)
        
@sio.on('ipaddr')
def message_ipaddr():
    sio.emit('ipaddr', '192.168.11.5')

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.on('bye')
def bye():
    print('received bye')

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    clients.remove(sid)
    

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('192.168.11.5', 3030)), app)
