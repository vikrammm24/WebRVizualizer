from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Technology:
    """
    Represents a technology associated with an endpoint or host.

    Technology detection is outside the responsibility of this model.
    """

    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("technology name must not be empty")
