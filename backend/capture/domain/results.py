from dataclasses import dataclass


@dataclass(frozen=True)
class CaptureResult:
    single_throw_probability: float
    cumulative_probability: float
    expected_throws: float
    guaranteed: bool
    calculation_details: dict[str, int | float | str]