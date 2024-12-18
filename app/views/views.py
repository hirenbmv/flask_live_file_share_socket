from flask import Blueprint,render_template,request,make_response,jsonify,redirect,flash
import logging
from threading import Lock
from collections import defaultdict
from app import socketio,db
import random,math
from app.models.models import Room
from app.events.events import *
import base64

log = logging.getLogger('File-Sharing')

lock = Lock()
chucks = defaultdict(list)

views_blueprint = Blueprint('views_blueprint', __name__)

def generate_room_number():
    # Declare a digits variable  
    # which stores all digits
    digits = "0123456789"
    ROOM_NUMBER = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(6) :
        ROOM_NUMBER += digits[math.floor(random.random() * 10)]

    return ROOM_NUMBER

@views_blueprint.route("/")
def index():
    return render_template('index.html',generate_room_number=generate_room_number)


@views_blueprint.route("/create_room")
def create_room():

    room_id = generate_room_number()

    room_exist = Room.query.filter_by(room_id = room_id).first()

    if not room_exist:
        add_room = Room(room_id = room_id)
        db.session.add(add_room)
        db.session.commit()
    else:
        log.error('Room ID already exists, Create new...')
        flash('Some error occurs, Please try again','error')
        return redirect('/')

    return redirect(f'/join_room?room_id={room_id}')

@views_blueprint.route("/join_room",methods=["GET","POST"])
def join_room():

    room_id = request.args.get('room_id',None)
    if not room_id:

        room_id = request.form.get('room_id',None)

    room_exist = Room.query.filter_by(room_id = room_id).first()

    if room_exist:
        flash('You entered in room','success')
    else:
        log.error('Room ID not exists, Create new...')
        flash('Room ID not exists, Create new.','error')
        return redirect('/')

    return render_template('join_room.html',room_id=room_id)

# Assuming 'file' is a FileStorage object received from a form
def file_to_base64(file):
    # Read the file content and encode it to Base64
    file_content = file.read()
    encoded_content = base64.b64encode(file_content).decode('utf-8')  # Convert bytes to string
    return encoded_content

@views_blueprint.route("/upload", methods=["GET","POST"])
def upload():

    # Define chunk size (5MB as per your requirement)
    CHUNK_SIZE = 5 * 1024 * 1024  # 5MB
    
    file = request.files.get("file")
    room = request.form.get('room_id',None)
    socket_id = request.form.get('socket_id',None)

    
    if not file:
        raise make_response(status=400, body="No file provided")

    dz_uuid = request.form.get("dzuuid")
    if not dz_uuid:
        # Now send the encoded file over the socket
        encoded_file = file_to_base64(file)
        # Assume this file has not been chunked
        print('Sending Full File')
        socketio.emit('receive_chunks', {'full_file': encoded_file,'filename':file.filename}, to=room,skip_sid=socket_id)
        # with open(storage_path / f"{uuid.uuid4()}_{secure_filename(file.filename)}", "wb") as f:
        #     print(f"Emitting to room: {room}")
        #     file.save(f)
        return "File Saved"


    # Chunked download
    try:
        chunk_index = int(request.form["dzchunkindex"])
        total_chunks = int(request.form["dztotalchunkcount"])
        chunkbyteoffset = int(request.form['dzchunkbyteoffset'])
    except KeyError as err:
        raise make_response(status=400, body=f"Not all required fields supplied, missing {err}")
    except ValueError:
        raise make_response(status=400, body=f"Values provided were not in expected format")


    # Read the chunk from the file without saving it
    chunk_data = file.read(CHUNK_SIZE)  # Read the chunk (directly from the file)

    # See if we have all the chunks downloaded
    with lock:
        chucks[dz_uuid].append(chunk_index)
        socketio.emit('receive_chunks', {'chunk':chunk_data,'chunkbyteoffset': chunkbyteoffset,'chunk_index':chunk_index,'filename':file.filename,'total_chunks':total_chunks}, to=room,skip_sid=socket_id)
        completed = len(chucks[dz_uuid]) == total_chunks

    # Concat all the files into the final file when all are downloaded
    if completed:
        log.info(f"{file.filename} has been uploaded")

    return jsonify({"message":f"{file.filename} process completed"})