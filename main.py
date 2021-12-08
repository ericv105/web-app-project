from website import create_app
from flask_socketio import SocketIO, send
import json

app = create_app()
socketio = SocketIO(app)

from website.models import Upload

@socketio.on('upvote')
def handleUpvote(data):
    info = json.loads(data)
    filename = info['filename']
    images = Upload.objects(filename=filename)
    Upload.objects(filename=filename).update_one(inc__votes=1)
    image = images[0]
    image.reload()
    votes = image.votes
    print(image.votes, image.filename)
    payload = json.dumps({
        "action": "upvote",
        "filename": filename,
        "votes": votes
    })
    send(payload, broadcast=True)

@socketio.on('downvote')
def handleDownvote(data):
    info = json.loads(data)
    filename = info['filename']
    images = Upload.objects(filename=filename)
    Upload.objects(filename=filename).update_one(dec__votes=1)
    image = images[0]
    image.reload()
    votes = image.votes
    print(image.votes, image.filename)
    payload = json.dumps({
        "action": "downvote",
        "filename": filename,
        "votes": votes
    })
    send(payload, broadcast=True)

if __name__ == '__main__':
    print("===Running===")
    socketio.run(app, debug=True, host='0.0.0.0', log_output=True)