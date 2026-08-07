from __future__ import annotations

from collections.abc import Iterable

from webrviz.models.application import Application
from webrviz.models.endpoint import Endpoint
from webrviz.utils.domains import get_parent_domain


class ApplicationBuilder:
    """
    Builds an Application from a collection of Endpoints.

    Responsibilities
    ----------------
    - Remove duplicate endpoints
    - Group endpoints by hostname
    - Build the host hierarchy
    - Sort hosts
    - Sort endpoints
    """

    @staticmethod
    def build(endpoints: Iterable[Endpoint]) -> Application:
        """
        Build and return an Application.
        """

        application = Application()

        #
        # Remove duplicates.
        #
        unique_endpoints = sorted(
            set(endpoints),
            key=lambda endpoint: endpoint.full_url,
        )

        #
        # PASS 1
        #
        # Create every host and attach endpoints.
        #
        for endpoint in unique_endpoints:
            host = application.get_or_create_host(endpoint.hostname)
            host.add_endpoint(endpoint)

        #
        # PASS 2
        #
        # Build host hierarchy.
        #
        for host in application.all_hosts():

            parent_hostname = get_parent_domain(host.hostname)

            if parent_hostname is None:
                continue

            parent = application.hosts.get(parent_hostname)

            if parent is None:
                continue

            parent.add_child(host)

        #
        # PASS 3
        #
        # Sort endpoints and child hosts.
        #
        for host in application.all_hosts():
            host.sort_endpoints()
            host.sort_children()

        #
        # PASS 4
        #
        # Sort application hosts.
        #
        application.hosts = dict(
            sorted(
                application.hosts.items(),
                key=lambda item: item[0],
            )
        )

        return application
