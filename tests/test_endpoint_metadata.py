from webrviz.models.endpoint_metadata import EndpointMetadata


def test_metadata_defaults_to_unknown() -> None:
    metadata = EndpointMetadata()

    assert metadata.status_codes == frozenset()
    assert metadata.content_types == frozenset()
    assert metadata.response_sizes == frozenset()
    assert metadata.technologies == frozenset()
    assert metadata.redirect_targets == frozenset()


def test_single_metadata_values_are_stored() -> None:
    metadata = EndpointMetadata.from_values(
        status_code=200,
        content_type="text/html",
        response_size=1024,
        technology="nginx",
        redirect_target="https://example.com/login",
    )

    assert metadata.status_codes == frozenset({200})
    assert metadata.content_types == frozenset({"text/html"})
    assert metadata.response_sizes == frozenset({1024})
    assert metadata.technologies == frozenset({"nginx"})
    assert metadata.redirect_targets == frozenset(
        {"https://example.com/login"}
    )


def test_none_values_remain_unknown() -> None:
    metadata = EndpointMetadata.from_values(
        status_code=200,
        content_type=None,
        response_size=None,
        technology=None,
        redirect_target=None,
    )

    assert metadata.status_codes == frozenset({200})
    assert metadata.content_types == frozenset()
    assert metadata.response_sizes == frozenset()
    assert metadata.technologies == frozenset()
    assert metadata.redirect_targets == frozenset()


def test_duplicate_values_are_merged_once() -> None:
    first = EndpointMetadata.from_values(
        status_code=200,
        technology="nginx",
    )

    second = EndpointMetadata.from_values(
        status_code=200,
        technology="nginx",
    )

    merged = first.merge(second)

    assert merged.status_codes == frozenset({200})
    assert merged.technologies == frozenset({"nginx"})


def test_conflicting_status_codes_are_preserved() -> None:
    first = EndpointMetadata.from_values(
        status_code=200,
    )

    second = EndpointMetadata.from_values(
        status_code=403,
    )

    merged = first.merge(second)

    assert merged.status_codes == frozenset({200, 403})


def test_multiple_content_types_are_preserved() -> None:
    first = EndpointMetadata.from_values(
        content_type="text/html",
    )

    second = EndpointMetadata.from_values(
        content_type="application/json",
    )

    merged = first.merge(second)

    assert merged.content_types == frozenset(
        {
            "text/html",
            "application/json",
        }
    )


def test_multiple_technologies_are_preserved() -> None:
    first = EndpointMetadata.from_values(
        technology="nginx",
    )

    second = EndpointMetadata.from_values(
        technology="React",
    )

    merged = first.merge(second)

    assert merged.technologies == frozenset(
        {
            "nginx",
            "React",
        }
    )


def test_missing_metadata_does_not_overwrite_existing_metadata() -> None:
    existing = EndpointMetadata.from_values(
        status_code=200,
        content_type="text/html",
        technology="nginx",
    )

    missing = EndpointMetadata()

    merged = existing.merge(missing)

    assert merged == existing


def test_merge_is_commutative() -> None:
    first = EndpointMetadata.from_values(
        status_code=200,
        technology="nginx",
    )

    second = EndpointMetadata.from_values(
        status_code=403,
        technology="React",
    )

    assert first.merge(second) == second.merge(first)


def test_merge_is_idempotent() -> None:
    metadata = EndpointMetadata.from_values(
        status_code=200,
        technology="nginx",
    )

    assert metadata.merge(metadata) == metadata


def test_merge_is_deterministic() -> None:
    first = EndpointMetadata.from_values(
        status_code=200,
        technology="nginx",
    )

    second = EndpointMetadata.from_values(
        status_code=403,
        technology="React",
    )

    result_one = first.merge(second)
    result_two = first.merge(second)

    assert result_one == result_two
