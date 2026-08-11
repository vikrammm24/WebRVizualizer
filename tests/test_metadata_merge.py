from webrviz.models.endpoint_metadata import EndpointMetadata
from webrviz.services.metadata_merge import merge_metadata


def test_merge_metadata_with_empty_input() -> None:
    result = merge_metadata([])

    assert result == EndpointMetadata()


def test_merge_metadata_combines_values() -> None:
    result = merge_metadata(
        [
            EndpointMetadata.from_values(
                status_code=200,
                technology="nginx",
            ),
            EndpointMetadata.from_values(
                status_code=403,
                technology="React",
            ),
        ]
    )

    assert result.status_codes == frozenset({200, 403})
    assert result.technologies == frozenset({"nginx", "React"})


def test_merge_metadata_preserves_missing_values() -> None:
    result = merge_metadata(
        [
            EndpointMetadata.from_values(
                status_code=200,
            ),
            EndpointMetadata(),
        ]
    )

    assert result.status_codes == frozenset({200})
    assert result.content_types == frozenset()


def test_merge_metadata_is_order_independent() -> None:
    first = EndpointMetadata.from_values(
        status_code=200,
        technology="nginx",
    )

    second = EndpointMetadata.from_values(
        status_code=403,
        technology="React",
    )

    result_one = merge_metadata([first, second])
    result_two = merge_metadata([second, first])

    assert result_one == result_two
