from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^hellspawns/', HellspawnListView.as_view()),
    url(r'^scenes/', SceneListView.as_view()),
    url(r'^clues/', ClueListView.as_view()),
]
