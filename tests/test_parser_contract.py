from collections.abc import Iterable

import pytest

from webrviz.models.normalized_observation import NormalizedObservation
from webrviz.parsers.normalized_base import Parser


class DummyParser(Parser):
    def parse(self) -> Iterable[NormalizedObservation]:
        return []


def test_parser_can_be_implemented() -> None:
    parser = DummyParser()

    assert list(parser.parse()) == []


def test_parser_is_abstract() -> None:
    with pytest.raises(TypeError):
        Parser()
