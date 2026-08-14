"use client";

import Image from "next/image";
import * as React from "react";
import { RiArrowUpDownLine } from "@remixicon/react";

import { buttonVariants } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import type {
  Pokemon,
} from "@/features/capture-calculator/types/capture";
import { cn } from "@/lib/utils";

type PokemonComboboxProps = {
  pokemon: Pokemon[];
  value?: number;
  selectedPokemon?: Pokemon;
  isLoading: boolean;
  isLoadingMore: boolean;
  hasMore: boolean;
  onSearchChange: (value: string) => void;
  onReachEnd: () => Promise<void> | void;
  onValueChange: (pokemonId: number) => void;
};

export function PokemonCombobox({
  pokemon,
  value,
  selectedPokemon,
  isLoading,
  isLoadingMore,
  hasMore,
  onSearchChange,
  onReachEnd,
  onValueChange,
}: PokemonComboboxProps) {
  const [open, setOpen] = React.useState(false);
  const listId = React.useId();
  const scrollRef = React.useRef<HTMLDivElement | null>(null);

  const handleScroll = React.useCallback(() => {
    const element = scrollRef.current;

    if (!element || !hasMore || isLoadingMore) {
      return;
    }

    const distanceToBottom =
      element.scrollHeight - element.scrollTop - element.clientHeight;

    if (distanceToBottom < 24) {
      void onReachEnd();
    }
  }, [hasMore, isLoadingMore, onReachEnd]);

  const selectedPokemonOption =
    pokemon.find((item) => item.id === value) ?? selectedPokemon;

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger
        type="button"
        role="combobox"
        aria-controls={listId}
        aria-expanded={open}
        className={cn(
          buttonVariants({ variant: "outline" }),
          "h-10 w-full min-w-0 justify-between px-3 text-sm",
        )}
      >
        {selectedPokemonOption ? (
          <span className="flex min-w-0 flex-1 items-center gap-2 overflow-hidden">
            <PokemonSprite pokemon={selectedPokemonOption} />

            <span className="truncate">
              #{String(selectedPokemonOption.national_dex_number).padStart(3, "0")}{" "}
              {selectedPokemonOption.name}
            </span>
          </span>
        ) : (
          <span className="truncate">Selecciona un Pokémon</span>
        )}

        <RiArrowUpDownLine className="ml-2 size-4 shrink-0 opacity-50" />
      </PopoverTrigger>

      <PopoverContent
        className="w-[--radix-popover-trigger-width] p-0"
        align="start"
      >
        <Command>
          <CommandInput
            placeholder="Buscar Pokémon..."
            onValueChange={onSearchChange}
          />

          <div
            ref={scrollRef}
            onScroll={handleScroll}
            className="max-h-72 overflow-y-auto"
          >
            <CommandList id={listId} className="max-h-none overflow-visible">
              <CommandEmpty>
                {isLoading
                  ? "Cargando Pokémon..."
                  : "No se encontró ningún Pokémon."}
              </CommandEmpty>

              <CommandGroup>
                {pokemon.map((item) => (
                  <CommandItem
                    key={item.id}
                    data-checked={value === item.id}
                    value={[
                      item.name,
                      item.slug,
                      item.national_dex_number,
                    ].join(" ")}
                    onSelect={() => {
                      onValueChange(item.id);
                      setOpen(false);
                    }}
                  >
                    <PokemonSprite pokemon={item} />

                    <span className="flex-1">
                      #{String(item.national_dex_number).padStart(3, "0")}{" "}
                      {item.name}
                    </span>
                  </CommandItem>
                ))}
              </CommandGroup>

              {isLoadingMore ? (
                <div className="px-2 py-3 text-center text-xs text-muted-foreground">
                  Cargando más Pokémon...
                </div>
              ) : null}
            </CommandList>
          </div>
        </Command>
      </PopoverContent>
    </Popover>
  );
}

function PokemonSprite({ pokemon }: { pokemon: Pokemon }) {
  const sprite = pokemon.generation_data[0]?.sprite_url;

  if (!sprite) {
    return <span className="size-8 shrink-0" />;
  }

  return (
    <Image
      src={sprite}
      alt=""
      width={32}
      height={32}
      className="size-8 shrink-0 object-contain pixelated"
    />
  );
}
