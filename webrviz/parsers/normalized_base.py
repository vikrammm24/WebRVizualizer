from abc import ABC, abstractmethod
from collections.abc import Iterable

from webrviz.models.normalized_observation import NormalizedObservation


class Parser(ABC):
    """
    Phase 2 parser interface.

    Parsers implementing this interface convert raw reconnaissance
    input into normalized observations.

    This interface is intentionally separate from the Phase 1
    BaseParser so existing parser behavior remains unchanged.
    """

    @abstractmethod
    def parse(self) -> Iterable[NormalizedObservation]:
        """
        Parse input and produce normalized observations.
        """
        raise NotImplementedError
