from collections.abc import Iterable

from webrviz.models import Application, Endpoint


class ApplicationMerger:
    """
    Builds an Application object from one or more collections of Endpoints.
    """

    def merge(self, *endpoint_groups: Iterable[Endpoint]) -> Application:
        """
        Merge multiple endpoint collections into a single Application.

        Parameters
        ----------
        *endpoint_groups:
            One or more iterables containing Endpoint objects.

        Returns
        -------
        Application
            The populated application model.
        """
        application = Application()

        for endpoints in endpoint_groups:
            for endpoint in endpoints:
                host = application.get_or_create_host(endpoint.hostname)
                host.add_endpoint(endpoint)

        return application
