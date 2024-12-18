from app import socketio
from flask_socketio import emit,join_room,rooms,leave_room,send
from flask import request,flash

@socketio.on("join_room")
def join(data):
    room = data.get('room_id')
    if room:
        join_room(room)
        emit("status", {"message": f" Has Joined Room","socket_id":request.sid},to=room)

@socketio.on("leave_room")
def leave(data):
    room = data.get('room_id')
    if room:
        leave_room(room)
        emit("status", {"message": f" Has left room","socket_id":request.sid},to=room)

@socketio.on("progress_bar")
def progress_bar(data):
    room = data.get('room_id')
    emit('progress_bar_status', {'data':data}, to=room)

@socketio.on("file_complete")
def status(data):
    room = data.get('room_id')
    filename = data.get('filename')
    emit('file_complete', {'data':data}, to=room)
    emit("status", {"message": f" Has Shared a {filename} file","socket_id":request.sid},to=room)