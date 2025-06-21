import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import create_app, db
from server.models import Episode, Guest, Appearance
import csv

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    csv_path = os.path.join(os.path.dirname(__file__), 'seed.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Seed file not found at {csv_path}")

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        episodes = {}
        guests = {}

        for row in reader:
            if row['Show'] and not episodes.get(row['Show']):
                episode = Episode(date=row['Show'], number=len(episodes) + 1)
                db.session.add(episode)
                episodes[row['Show']] = episode

            if row['Raw_Guest_List'] and not guests.get(row['Raw_Guest_List']):
                guest = Guest(name=row['Raw_Guest_List'], occupation=row['GoogleKnowlege_Occupation'])
                db.session.add(guest)
                guests[row['Raw_Guest_List']] = guest

        db.session.commit()

        csvfile.seek(0)
        next(reader)
        for row in reader:
            if row['Raw_Guest_List'] and row['Show']:
                guest = guests.get(row['Raw_Guest_List'])
                episode = episodes.get(row['Show'])
                if guest and episode and not Appearance.query.filter_by(guest_id=guest.id, episode_id=episode.id).first():
                    appearance = Appearance(rating=3, episode_id=episode.id, guest_id=guest.id)
                    db.session.add(appearance)

        db.session.commit()