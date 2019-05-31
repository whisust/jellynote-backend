from datetime import datetime
from threading import Thread

from models.jellynote import Song
from persist import users, notifications


def format_message(song_title, instruments):
    return "A new Song matching " + ', '.join([i.value for i in instruments]) + " was published: " + song_title


def generate_notifications(song: Song):
    print("Starting notification generation for " + str(song))
    t0 = datetime.now()
    user_list = users.list_by_instruments(song.instruments)
    set_instruments = set(song.instruments)
    notification_values = []
    for user in user_list:
        instruments = set(user.instruments).intersection(set_instruments)
        msg = format_message(song.title, instruments)
        notification_values.append((song.id, user.id, msg))
    notifications.insert(notification_values)
    t1 = datetime.now()
    print("Done generating " + str(len(notification_values)) + " notifications for " + str(song))
    print("Elapsed: " + str((t1 - t0).total_seconds()))


def async_notification_generation(song: Song):
    t = Thread(target=generate_notifications, args=(song,))
    t.start()
