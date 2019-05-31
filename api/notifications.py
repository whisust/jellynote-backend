from models.jellynote import Song
from persist import users, notifications


def format_message(song_title, instruments):
    return "A new Song matching " + ', '.join([i.value for i in instruments]) + " was published: " + song_title


def generate_notifications(song: Song):
    user_list = users.list_by_instruments(song.instruments)
    set_instruments = set(song.instruments)
    notification_values = []
    for user in user_list:
        instruments = set(user.instrument).intersection(set_instruments)
        msg = format_message(song.title, instruments)
        notification_values.append((song.id, user.id, msg))

    notifications.insert(notification_values)
