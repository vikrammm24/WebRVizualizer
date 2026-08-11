from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Source:
    """
    Identifies the reconnaissance source that produced an observation.

    Source names are intentionally represented as strings rather than an
    enum so that future tools can be added without modifying the core
    data model.
    """

    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("source name must not be empty")
