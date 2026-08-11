from collections.abc import Iterable

from webrviz.models.endpoint_metadata import EndpointMetadata


def merge_metadata(
    metadata: Iterable[EndpointMetadata],
) -> EndpointMetadata:
    """
    Merge endpoint metadata deterministically.

    Empty input produces empty metadata.
    """

    result = EndpointMetadata()

    for item in metadata:
        result = result.merge(item)

    return result
