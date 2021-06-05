# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources
from requests import __version__ as requests_version

import google.auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore

from google.cloud.compute_v1.types import compute

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-compute",).version,
        grpc_version=None,
        rest_version=requests_version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = google.auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None


class NetworksTransport(abc.ABC):
    """Abstract transport class for Networks."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/compute",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    DEFAULT_HOST: str = "compute.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): This method is in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-auth is increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.add_peering: gapic_v1.method.wrap_method(
                self.add_peering, default_timeout=None, client_info=client_info,
            ),
            self.delete: gapic_v1.method.wrap_method(
                self.delete, default_timeout=None, client_info=client_info,
            ),
            self.get: gapic_v1.method.wrap_method(
                self.get, default_timeout=None, client_info=client_info,
            ),
            self.get_effective_firewalls: gapic_v1.method.wrap_method(
                self.get_effective_firewalls,
                default_timeout=None,
                client_info=client_info,
            ),
            self.insert: gapic_v1.method.wrap_method(
                self.insert, default_timeout=None, client_info=client_info,
            ),
            self.list: gapic_v1.method.wrap_method(
                self.list, default_timeout=None, client_info=client_info,
            ),
            self.list_peering_routes: gapic_v1.method.wrap_method(
                self.list_peering_routes, default_timeout=None, client_info=client_info,
            ),
            self.patch: gapic_v1.method.wrap_method(
                self.patch, default_timeout=None, client_info=client_info,
            ),
            self.remove_peering: gapic_v1.method.wrap_method(
                self.remove_peering, default_timeout=None, client_info=client_info,
            ),
            self.switch_to_custom_mode: gapic_v1.method.wrap_method(
                self.switch_to_custom_mode,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_peering: gapic_v1.method.wrap_method(
                self.update_peering, default_timeout=None, client_info=client_info,
            ),
        }

    @property
    def add_peering(
        self,
    ) -> Callable[
        [compute.AddPeeringNetworkRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete(
        self,
    ) -> Callable[
        [compute.DeleteNetworkRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetNetworkRequest], Union[compute.Network, Awaitable[compute.Network]]
    ]:
        raise NotImplementedError()

    @property
    def get_effective_firewalls(
        self,
    ) -> Callable[
        [compute.GetEffectiveFirewallsNetworkRequest],
        Union[
            compute.NetworksGetEffectiveFirewallsResponse,
            Awaitable[compute.NetworksGetEffectiveFirewallsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def insert(
        self,
    ) -> Callable[
        [compute.InsertNetworkRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListNetworksRequest],
        Union[compute.NetworkList, Awaitable[compute.NetworkList]],
    ]:
        raise NotImplementedError()

    @property
    def list_peering_routes(
        self,
    ) -> Callable[
        [compute.ListPeeringRoutesNetworksRequest],
        Union[
            compute.ExchangedPeeringRoutesList,
            Awaitable[compute.ExchangedPeeringRoutesList],
        ],
    ]:
        raise NotImplementedError()

    @property
    def patch(
        self,
    ) -> Callable[
        [compute.PatchNetworkRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def remove_peering(
        self,
    ) -> Callable[
        [compute.RemovePeeringNetworkRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def switch_to_custom_mode(
        self,
    ) -> Callable[
        [compute.SwitchToCustomModeNetworkRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_peering(
        self,
    ) -> Callable[
        [compute.UpdatePeeringNetworkRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("NetworksTransport",)
