from capture.domain.calculators.base import (
    BaseCaptureCalculator,
)
from capture.domain.calculators.generation_1 import (
    GenerationOneCalculator,
)
from capture.domain.calculators.generation_2 import (
    GenerationTwoCalculator,
)


_CALCULATORS: dict[int, type[BaseCaptureCalculator]] = {
    1: GenerationOneCalculator,
    2: GenerationTwoCalculator,
}


def get_capture_calculator(
    generation: int,
) -> BaseCaptureCalculator:
    calculator_class = _CALCULATORS.get(generation)

    if calculator_class is None:
        raise ValueError(
            f"Generation {generation} is not supported."
        )

    return calculator_class()