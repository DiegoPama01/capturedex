"use client";

import { RiArrowDownSLine } from "@remixicon/react";
import * as React from "react";

import { cn } from "@/lib/utils";

type AccordionContextValue = {
  value?: string;
  setValue: (value?: string) => void;
  collapsible: boolean;
};

const AccordionContext = React.createContext<AccordionContextValue | null>(null);
const AccordionItemContext = React.createContext<string | null>(null);

function Accordion({
  type,
  value,
  collapsible = false,
  className,
  children,
}: {
  type: "single";
  value?: string;
  collapsible?: boolean;
  className?: string;
  children: React.ReactNode;
}) {
  const [internalValue, setInternalValue] = React.useState<string | undefined>(value);
  const currentValue = value ?? internalValue;

  const contextValue = React.useMemo<AccordionContextValue>(
    () => ({
      value: currentValue,
      collapsible,
      setValue: (nextValue) => {
        if (type !== "single") {
          return;
        }

        if (value !== undefined) {
          return;
        }

        setInternalValue(nextValue);
      },
    }),
    [collapsible, currentValue, type, value],
  );

  return (
    <AccordionContext.Provider value={contextValue}>
      <div className={className}>{children}</div>
    </AccordionContext.Provider>
  );
}

function AccordionItem({
  value,
  className,
  children,
}: {
  value: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <AccordionItemContext.Provider value={value}>
      <div className={cn("border-b", className)}>{children}</div>
    </AccordionItemContext.Provider>
  );
}

function AccordionTrigger({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  const accordion = React.useContext(AccordionContext);
  const itemValue = React.useContext(AccordionItemContext);

  if (!accordion || !itemValue) {
    throw new Error("AccordionTrigger must be used inside AccordionItem.");
  }

  const isOpen = accordion.value === itemValue;

  return (
    <button
      type="button"
      data-state={isOpen ? "open" : "closed"}
      className={cn(
        "flex w-full items-center justify-between gap-4 py-3 text-left text-sm font-medium transition-all hover:underline",
        className,
      )}
      onClick={() => {
        if (isOpen && accordion.collapsible) {
          accordion.setValue(undefined);
          return;
        }

        accordion.setValue(itemValue);
      }}
    >
      <span>{children}</span>
      <RiArrowDownSLine
        className={cn(
          "size-4 shrink-0 transition-transform duration-200",
          isOpen && "rotate-180",
        )}
      />
    </button>
  );
}

function AccordionContent({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  const accordion = React.useContext(AccordionContext);
  const itemValue = React.useContext(AccordionItemContext);

  if (!accordion || !itemValue) {
    throw new Error("AccordionContent must be used inside AccordionItem.");
  }

  if (accordion.value !== itemValue) {
    return null;
  }

  return <div className={cn("pb-4", className)}>{children}</div>;
}

export { Accordion, AccordionContent, AccordionItem, AccordionTrigger };
