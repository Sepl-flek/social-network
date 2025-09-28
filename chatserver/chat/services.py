from asgiref.sync import sync_to_async

from chat.models import Room, Message


@sync_to_async
def save_message(room_name: str, text: str, user):
    room = Room.objects.get(name=room_name)
    return Message.objects.create(room=room, text=text, author=user)
