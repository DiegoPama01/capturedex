from rest_framework import filters, generics

from .models import Pokemon
from .serializers import PokemonSerializer


class PokemonListView(generics.ListAPIView):
    serializer_class = PokemonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "slug",
        "national_dex_number",
    ]

    def get_queryset(self):
        return (
            Pokemon.objects
            .prefetch_related("generation_data")
            .filter(generation_data__generation=1)
            .distinct()
        )