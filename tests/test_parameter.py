import pytest

from webrviz.models.parameter import Parameter, ParameterLocation


def test_parameter_stores_name_and_location() -> None:
    parameter = Parameter(
        name="id",
        location=ParameterLocation.QUERY,
    )

    assert parameter.name == "id"
    assert parameter.location == ParameterLocation.QUERY


def test_parameter_locations_are_defined() -> None:
    assert ParameterLocation.QUERY.value == "query"
    assert ParameterLocation.PATH.value == "path"
    assert ParameterLocation.HEADER.value == "header"
    assert ParameterLocation.COOKIE.value == "cookie"
    assert ParameterLocation.BODY.value == "body"


def test_parameter_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="parameter name"):
        Parameter(
            name="",
            location=ParameterLocation.QUERY,
        )


def test_parameter_is_immutable() -> None:
    parameter = Parameter(
        name="id",
        location=ParameterLocation.QUERY,
    )

    with pytest.raises(AttributeError):
        parameter.name = "user_id"


def test_same_parameters_are_equal() -> None:
    first = Parameter(
        name="id",
        location=ParameterLocation.QUERY,
    )

    second = Parameter(
        name="id",
        location=ParameterLocation.QUERY,
    )

    assert first == second


def test_parameter_location_is_part_of_identity() -> None:
    query_parameter = Parameter(
        name="id",
        location=ParameterLocation.QUERY,
    )

    header_parameter = Parameter(
        name="id",
        location=ParameterLocation.HEADER,
    )

    assert query_parameter != header_parameter
