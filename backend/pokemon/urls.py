from django.urls import path

from .views import PokemonListView


app_name = "pokemon"

urlpatterns = [
    path("", PokemonListView.as_view(), name="list"),
]