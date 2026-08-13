from rest_framework import filters, generics
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch

from .models import Pokemon, PokemonGenerationData
from .query_serializers import PokemonListQuerySerializer
from .serializers import PokemonSerializer


class GenerationOnePokemonPagination(PageNumberPagination):
    page_size = 151
    max_page_size = 151

    def get_page_size(self, request):
        generation = request.query_params.get("generation", "1")

        if generation == "2":
            return 100

        return self.page_size


class PokemonListView(generics.ListAPIView):
    serializer_class = PokemonSerializer
    pagination_class = GenerationOnePokemonPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "slug",
        "national_dex_number",
    ]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        query_serializer = PokemonListQuerySerializer(
            data=request.query_params,
        )
        query_serializer.is_valid(raise_exception=True)
        self.validated_query_params = query_serializer.validated_data

    def get_queryset(self):
        generation = self.validated_query_params["generation"]
        version_group = self.validated_query_params.get("version_group")

        filters_by_generation: dict[str, object] = {}
        filters_by_generation["generation_data__generation"] = generation

        if version_group is not None:
            filters_by_generation["generation_data__version_group"] = version_group

        generation_data_queryset = PokemonGenerationData.objects.filter(
            generation=generation,
        ).order_by("generation", "id")

        if version_group is not None:
            generation_data_queryset = generation_data_queryset.filter(
                version_group=version_group,
            )

        return (
            Pokemon.objects.prefetch_related(
                Prefetch(
                    "generation_data",
                    queryset=generation_data_queryset,
                    to_attr="filtered_generation_data",
                )
            )
            .filter(**filters_by_generation)
            .distinct()
        )
