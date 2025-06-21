import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request
from server import create_app
from server.models import db, Episode, Guest, Appearance

app = create_app()

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return {'episodes': [episode.to_dict() for episode in episodes]}

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = db.session.get(Episode, id)
    if episode:
        return episode.to_dict()
    return {'error': 'Episode not found'}, 404

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return {'guests': [guest.to_dict() for guest in guests]}

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        Appearance.validate_rating(data['rating'])
        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(appearance)
        db.session.commit()
        return appearance.to_dict(), 201
    except ValueError as e:
        return {'errors': [str(e)]}, 400
    except Exception:
        db.session.rollback()
        return {'errors': ['validation errors']}, 400

@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = db.session.get(Episode, id)
    if episode:
        db.session.delete(episode)
        db.session.commit()
        return {}, 204
    return {'error': 'Episode not found'}, 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)