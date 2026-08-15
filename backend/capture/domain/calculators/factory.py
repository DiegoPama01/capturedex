from capture.domain.calculators.base import (
    BaseCaptureCalculator,
)
from capture.domain.calculators.generation_1 import (
    GenerationOneCalculator,
)
from capture.domain.calculators.generation_2 import (
    GenerationTwoCalculator,
)
from capture.domain.calculators.generation_3 import (
    GenerationThreeCalculator,
)
from capture.domain.calculators.generation_4 import GenerationFourCalculator
from capture.domain.calculators.generation_5 import GenerationFiveCalculator
from capture.domain.calculators.generation_6 import GenerationSixCalculator


_CALCULATORS: dict[int, type[BaseCaptureCalculator]] = {
    1: GenerationOneCalculator,
    2: GenerationTwoCalculator,
    3: GenerationThreeCalculator,
    4: GenerationFourCalculator,
    5: GenerationFiveCalculator,
    6: GenerationSixCalculator,
}


def get_capture_calculator(
    generation: int,
) -> BaseCaptureCalculator:
    calculator_class = _CALCULATORS.get(generation)

    if calculator_class is None:
        raise ValueError(f"Generation {generation} is not supported.")

    return calculator_class()
