from app import create_app
from app import socketio

app = create_app()

if __name__ == '__main__':
  socketio.run(app,debug=False,host='0.0.0.0',port=2002)

# gunicorn -k eventlet -w 1 --timeout 3600 wsgi:app -b 0.0.0.0:2002
# pkill -9 -f gunicorn

# To know status of process running 
# lsof -i :5002  [PORT_NUMBER]