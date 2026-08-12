from rest_framework import filters, generics
from rest_framework.pagination import PageNumberPagination

from .models import Pokemon
from .serializers import PokemonSerializer


class GenerationOnePokemonPagination(PageNumberPagination):
    page_size = 151
    max_page_size = 151


class PokemonListView(generics.ListAPIView):
    serializer_class = PokemonSerializer
    pagination_class = GenerationOnePokemonPagination
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