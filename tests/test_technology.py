import pytest

from webrviz.models.technology import Technology


def test_technology_stores_name() -> None:
    technology = Technology("nginx")

    assert technology.name == "nginx"


def test_technology_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="technology name"):
        Technology("")


def test_same_technologies_are_equal() -> None:
    first = Technology("nginx")
    second = Technology("nginx")

    assert first == second


def test_different_technologies_are_not_equal() -> None:
    first = Technology("nginx")
    second = Technology("Apache")

    assert first != second


def test_technology_is_immutable() -> None:
    technology = Technology("nginx")

    with pytest.raises(AttributeError):
        technology.name = "Apache"
