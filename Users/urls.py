from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index),
    path("", views.home, name="Home"),
    path("forum/", views.forum, name="Forum"),
    path("discussion/<int:myid>/", views.discussion, name="Discussions"),
    path("register/", views.UserRegister, name="Register"),
    path("login/", views.UserLogin, name="Login"),
    path("logout/", views.UserLogout, name="Logout"),
    path("myprofile/", views.myprofile, name="Myprofile"),
    path("news/", views.news, name="News"),
    path("home/", views.home, name="Home"),
    path("events/", views.events, name="Events"),
    path("events/archives/", views.archives, name="Archives"),
    path("events/calendar/", views.calendar, name="Calendar"),
    path("contact/", views.contact, name="Contact"),
    path("members/", views.members, name="Members"),
    path("members/map", views.map, name="Map"),
]