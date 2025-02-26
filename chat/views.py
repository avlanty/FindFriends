from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Message

# Create your views here.
@login_required(login_url='login')
def join_room(request):
    username = request.user.username
    if request.method == 'POST':
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
        return redirect("chat_room", room_name=room, username=username)
    return render(request, "chat/join_room.html", {"room": Room.objects.all(), 
                                                   'username': username})


@login_required(login_url='login')
def chat_room(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    if request.method == 'POST':
        message = request.POST['message']
        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()
    get_messages= Message.objects.filter(room=get_room)
    context = {
        "messages": get_messages,
        "old_messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, "chat/chat_room.html", {"room_name": room_name,
                                                   "old_messages": get_messages,})