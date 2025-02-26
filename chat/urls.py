from django.urls import path
from . import views

urlpatterns = [
    path("<str:room_name>/<str:username>", views.chat_room, name="chat_room"),
    path("join-room/", views.join_room, name="join_room"),
]