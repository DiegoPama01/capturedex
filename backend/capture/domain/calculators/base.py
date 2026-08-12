from abc import ABC, abstractmethod

from capture.domain.inputs import CaptureInput
from capture.domain.results import CaptureResult


class BaseCaptureCalculator(ABC):
    generation: int

    @abstractmethod
    def calculate(
        self,
        capture_input: CaptureInput,
    ) -> CaptureResult:
        """Calculate the capture probability."""
        raise NotImplementedError