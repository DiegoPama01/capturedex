"use client";

import Image from "next/image";
import * as React from "react";
import { RiArrowUpDownLine } from "@remixicon/react";

import { buttonVariants } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import type { BallType } from "@/features/capture-calculator/types/capture";

export type PokeballOption = {
  value: BallType;
  label: string;
  sprite: string;
};

type PokeballComboboxProps = {
  options: PokeballOption[];
  value: BallType;
  onValueChange: (value: BallType) => void;
};

export function PokeballCombobox({
  options,
  value,
  onValueChange,
}: PokeballComboboxProps) {
  const [open, setOpen] = React.useState(false);
  const listId = React.useId();

  const selectedOption = options.find((option) => option.value === value);

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
        {selectedOption ? (
          <span className="flex min-w-0 flex-1 items-center gap-2 overflow-hidden">
            <PokeballSwatch option={selectedOption} />
            <span className="truncate">{selectedOption.label}</span>
          </span>
        ) : (
          <span className="truncate">Selecciona una Pokeball</span>
        )}

        <RiArrowUpDownLine className="ml-2 size-4 shrink-0 opacity-50" />
      </PopoverTrigger>

      <PopoverContent className="w-[--radix-popover-trigger-width] p-0" align="start">
        <Command>
          <CommandList id={listId}>
            <CommandEmpty>No se encontro ninguna Pokeball.</CommandEmpty>

            <CommandGroup>
              {options.map((option) => (
                <CommandItem
                  key={option.value}
                  value={[option.label, option.value].join(" ")}
                  onSelect={() => {
                    onValueChange(option.value);
                    setOpen(false);
                  }}
                >
                  <PokeballSwatch option={option} />
                  <span className="flex-1">{option.label}</span>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}

function PokeballSwatch({ option }: { option: PokeballOption }) {
  return (
    <Image
      src={option.sprite}
      alt=""
      width={28}
      height={28}
      className="size-7 shrink-0 object-contain pixelated"
    />
  );
}
