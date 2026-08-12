from django.contrib import admin

from .models import Pokemon, PokemonGenerationData


class PokemonGenerationDataInline(admin.TabularInline):
    model = PokemonGenerationData
    extra = 0


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = (
        "national_dex_number",
        "name",
        "slug",
    )
    search_fields = (
        "name",
        "slug",
    )
    ordering = ("national_dex_number",)
    prepopulated_fields = {
        "slug": ("name",),
    }
    inlines = [PokemonGenerationDataInline]


@admin.register(PokemonGenerationData)
class PokemonGenerationDataAdmin(admin.ModelAdmin):
    list_display = (
        "pokemon",
        "generation",
        "version_group",
        "catch_rate",
    )
    list_filter = (
        "generation",
        "version_group",
    )
    search_fields = (
        "pokemon__name",
        "pokemon__slug",
    )
    autocomplete_fields = ("pokemon",)