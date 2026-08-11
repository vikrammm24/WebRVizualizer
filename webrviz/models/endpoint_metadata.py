from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class EndpointMetadata:
    """
    Metadata associated with an endpoint.

    Metadata is represented using set-like collections so information
    from multiple reconnaissance sources can be merged without
    destructive overwrites.

    Empty collections represent unknown/unavailable metadata.
    """

    status_codes: frozenset[int] = field(default_factory=frozenset)
    content_types: frozenset[str] = field(default_factory=frozenset)
    response_sizes: frozenset[int] = field(default_factory=frozenset)
    technologies: frozenset[str] = field(default_factory=frozenset)
    redirect_targets: frozenset[str] = field(default_factory=frozenset)

    def merge(self, other: "EndpointMetadata") -> "EndpointMetadata":
        """
        Merge two metadata objects deterministically.

        Scalar conflicts are preserved as multiple observed values
        rather than allowing one value to overwrite another.
        """

        return EndpointMetadata(
            status_codes=self.status_codes | other.status_codes,
            content_types=self.content_types | other.content_types,
            response_sizes=self.response_sizes | other.response_sizes,
            technologies=self.technologies | other.technologies,
            redirect_targets=self.redirect_targets | other.redirect_targets,
        )

    @classmethod
    def from_values(
        cls,
        *,
        status_code: int | None = None,
        content_type: str | None = None,
        response_size: int | None = None,
        technology: str | None = None,
        redirect_target: str | None = None,
    ) -> "EndpointMetadata":
        """
        Create metadata from a single observation.

        None values represent unknown information and are not inserted
        into the metadata collections.
        """

        return cls(
            status_codes=(
                frozenset({status_code})
                if status_code is not None
                else frozenset()
            ),
            content_types=(
                frozenset({content_type})
                if content_type is not None
                else frozenset()
            ),
            response_sizes=(
                frozenset({response_size})
                if response_size is not None
                else frozenset()
            ),
            technologies=(
                frozenset({technology})
                if technology is not None
                else frozenset()
            ),
            redirect_targets=(
                frozenset({redirect_target})
                if redirect_target is not None
                else frozenset()
            ),
        )
