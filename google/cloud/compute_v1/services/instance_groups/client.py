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
from collections import OrderedDict
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.compute_v1.services.instance_groups import pagers
from google.cloud.compute_v1.types import compute
from .transports.base import InstanceGroupsTransport, DEFAULT_CLIENT_INFO
from .transports.rest import InstanceGroupsRestTransport


class InstanceGroupsClientMeta(type):
    """Metaclass for the InstanceGroups client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[InstanceGroupsTransport]]
    _transport_registry["rest"] = InstanceGroupsRestTransport

    def get_transport_class(cls, label: str = None,) -> Type[InstanceGroupsTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class InstanceGroupsClient(metaclass=InstanceGroupsClientMeta):
    """The InstanceGroups API."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "compute.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            InstanceGroupsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            InstanceGroupsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> InstanceGroupsTransport:
        """Returns the transport used by the client instance.

        Returns:
            InstanceGroupsTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, InstanceGroupsTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the instance groups client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, InstanceGroupsTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, InstanceGroupsTransport):
            # transport is a InstanceGroupsTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def add_instances_unary(
        self,
        request: Union[compute.AddInstancesInstanceGroupRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_add_instances_request_resource: compute.InstanceGroupsAddInstancesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Adds a list of instances to the specified instance
        group. All of the instances in the instance group must
        be in the same network/subnetwork. Read Adding instances
        for more information.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_add_instances():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.AddInstancesInstanceGroupRequest(
                    instance_group="instance_group_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.add_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.AddInstancesInstanceGroupRequest, dict]):
                The request object. A request message for
                InstanceGroups.AddInstances. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group where
                you are adding instances.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_add_instances_request_resource (google.cloud.compute_v1.types.InstanceGroupsAddInstancesRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_add_instances_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                [Global](/compute/docs/reference/rest/v1/globalOperations)
                \*
                [Regional](/compute/docs/reference/rest/v1/regionOperations)
                \*
                [Zonal](/compute/docs/reference/rest/v1/zoneOperations)
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the globalOperations
                resource. - For regional operations, use the
                regionOperations resource. - For zonal operations, use
                the zonalOperations resource. For more information, read
                Global, Regional, and Zonal Resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_add_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddInstancesInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddInstancesInstanceGroupRequest):
            request = compute.AddInstancesInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_add_instances_request_resource is not None:
                request.instance_groups_add_instances_request_resource = (
                    instance_groups_add_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_instances]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def aggregated_list(
        self,
        request: Union[compute.AggregatedListInstanceGroupsRequest, dict] = None,
        *,
        project: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.AggregatedListPager:
        r"""Retrieves the list of instance groups and sorts them
        by zone.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_aggregated_list():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.AggregatedListInstanceGroupsRequest(
                    project="project_value",
                )

                # Make the request
                page_result = client.aggregated_list(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.AggregatedListInstanceGroupsRequest, dict]):
                The request object. A request message for
                InstanceGroups.AggregatedList. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instance_groups.pagers.AggregatedListPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AggregatedListInstanceGroupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AggregatedListInstanceGroupsRequest):
            request = compute.AggregatedListInstanceGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.aggregated_list]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.AggregatedListPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_unary(
        self,
        request: Union[compute.DeleteInstanceGroupRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes the specified instance group. The instances
        in the group are not deleted. Note that instance group
        must not belong to a backend service. Read Deleting an
        instance group for more information.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_delete():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.DeleteInstanceGroupRequest(
                    instance_group="instance_group_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.delete(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteInstanceGroupRequest, dict]):
                The request object. A request message for
                InstanceGroups.Delete. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group to
                delete.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                [Global](/compute/docs/reference/rest/v1/globalOperations)
                \*
                [Regional](/compute/docs/reference/rest/v1/regionOperations)
                \*
                [Zonal](/compute/docs/reference/rest/v1/zoneOperations)
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the globalOperations
                resource. - For regional operations, use the
                regionOperations resource. - For zonal operations, use
                the zonalOperations resource. For more information, read
                Global, Regional, and Zonal Resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteInstanceGroupRequest):
            request = compute.DeleteInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get(
        self,
        request: Union[compute.GetInstanceGroupRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.InstanceGroup:
        r"""Returns the specified zonal instance group. Get a
        list of available zonal instance groups by making a
        list() request. For managed instance groups, use the
        instanceGroupManagers or regionInstanceGroupManagers
        methods instead.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_get():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.GetInstanceGroupRequest(
                    instance_group="instance_group_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.get(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.GetInstanceGroupRequest, dict]):
                The request object. A request message for
                InstanceGroups.Get. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group.
                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.InstanceGroup:
                Represents an Instance Group
                resource. Instance Groups can be used to
                configure a target for load balancing.
                Instance groups can either be managed or
                unmanaged. To create managed instance
                groups, use the instanceGroupManager or
                regionInstanceGroupManager resource
                instead. Use zonal unmanaged instance
                groups if you need to apply load
                balancing to groups of heterogeneous
                instances or if you need to manage the
                instances yourself. You cannot create
                regional unmanaged instance groups. For
                more information, read Instance groups.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetInstanceGroupRequest):
            request = compute.GetInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def insert_unary(
        self,
        request: Union[compute.InsertInstanceGroupRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group_resource: compute.InstanceGroup = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates an instance group in the specified project
        using the parameters that are included in the request.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_insert():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.InsertInstanceGroupRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.insert(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.InsertInstanceGroupRequest, dict]):
                The request object. A request message for
                InstanceGroups.Insert. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where you want
                to create the instance group.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_resource (google.cloud.compute_v1.types.InstanceGroup):
                The body resource for this request
                This corresponds to the ``instance_group_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                [Global](/compute/docs/reference/rest/v1/globalOperations)
                \*
                [Regional](/compute/docs/reference/rest/v1/regionOperations)
                \*
                [Zonal](/compute/docs/reference/rest/v1/zoneOperations)
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the globalOperations
                resource. - For regional operations, use the
                regionOperations resource. - For zonal operations, use
                the zonalOperations resource. For more information, read
                Global, Regional, and Zonal Resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_group_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.InsertInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.InsertInstanceGroupRequest):
            request = compute.InsertInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group_resource is not None:
                request.instance_group_resource = instance_group_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list(
        self,
        request: Union[compute.ListInstanceGroupsRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPager:
        r"""Retrieves the list of zonal instance group resources
        contained within the specified zone. For managed
        instance groups, use the instanceGroupManagers or
        regionInstanceGroupManagers methods instead.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_list():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.ListInstanceGroupsRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                page_result = client.list(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ListInstanceGroupsRequest, dict]):
                The request object. A request message for
                InstanceGroups.List. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instance_groups.pagers.ListPager:
                A list of InstanceGroup resources.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ListInstanceGroupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListInstanceGroupsRequest):
            request = compute.ListInstanceGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_instances(
        self,
        request: Union[compute.ListInstancesInstanceGroupsRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_list_instances_request_resource: compute.InstanceGroupsListInstancesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesPager:
        r"""Lists the instances in the specified instance group.
        The orderBy query parameter is not supported.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_list_instances():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.ListInstancesInstanceGroupsRequest(
                    instance_group="instance_group_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                page_result = client.list_instances(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ListInstancesInstanceGroupsRequest, dict]):
                The request object. A request message for
                InstanceGroups.ListInstances. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group from
                which you want to generate a list of
                included instances.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_list_instances_request_resource (google.cloud.compute_v1.types.InstanceGroupsListInstancesRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_list_instances_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instance_groups.pagers.ListInstancesPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_list_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ListInstancesInstanceGroupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListInstancesInstanceGroupsRequest):
            request = compute.ListInstancesInstanceGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_list_instances_request_resource is not None:
                request.instance_groups_list_instances_request_resource = (
                    instance_groups_list_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_instances]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInstancesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def remove_instances_unary(
        self,
        request: Union[compute.RemoveInstancesInstanceGroupRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_remove_instances_request_resource: compute.InstanceGroupsRemoveInstancesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Removes one or more instances from the specified
        instance group, but does not delete those instances. If
        the group is part of a backend service that has enabled
        connection draining, it can take up to 60 seconds after
        the connection draining duration before the VM instance
        is removed or deleted.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_remove_instances():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.RemoveInstancesInstanceGroupRequest(
                    instance_group="instance_group_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.remove_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.RemoveInstancesInstanceGroupRequest, dict]):
                The request object. A request message for
                InstanceGroups.RemoveInstances. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group where
                the specified instances will be removed.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_remove_instances_request_resource (google.cloud.compute_v1.types.InstanceGroupsRemoveInstancesRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_remove_instances_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                [Global](/compute/docs/reference/rest/v1/globalOperations)
                \*
                [Regional](/compute/docs/reference/rest/v1/regionOperations)
                \*
                [Zonal](/compute/docs/reference/rest/v1/zoneOperations)
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the globalOperations
                resource. - For regional operations, use the
                regionOperations resource. - For zonal operations, use
                the zonalOperations resource. For more information, read
                Global, Regional, and Zonal Resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_remove_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.RemoveInstancesInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.RemoveInstancesInstanceGroupRequest):
            request = compute.RemoveInstancesInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_remove_instances_request_resource is not None:
                request.instance_groups_remove_instances_request_resource = (
                    instance_groups_remove_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_instances]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def set_named_ports_unary(
        self,
        request: Union[compute.SetNamedPortsInstanceGroupRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_set_named_ports_request_resource: compute.InstanceGroupsSetNamedPortsRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets the named ports for the specified instance
        group.


        .. code-block:: python

            from google.cloud import compute_v1

            def sample_set_named_ports():
                # Create a client
                client = compute_v1.InstanceGroupsClient()

                # Initialize request argument(s)
                request = compute_v1.SetNamedPortsInstanceGroupRequest(
                    instance_group="instance_group_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.set_named_ports(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetNamedPortsInstanceGroupRequest, dict]):
                The request object. A request message for
                InstanceGroups.SetNamedPorts. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group where
                the named ports are updated.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_set_named_ports_request_resource (google.cloud.compute_v1.types.InstanceGroupsSetNamedPortsRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_set_named_ports_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                [Global](/compute/docs/reference/rest/v1/globalOperations)
                \*
                [Regional](/compute/docs/reference/rest/v1/regionOperations)
                \*
                [Zonal](/compute/docs/reference/rest/v1/zoneOperations)
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the globalOperations
                resource. - For regional operations, use the
                regionOperations resource. - For zonal operations, use
                the zonalOperations resource. For more information, read
                Global, Regional, and Zonal Resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_set_named_ports_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetNamedPortsInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetNamedPortsInstanceGroupRequest):
            request = compute.SetNamedPortsInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_set_named_ports_request_resource is not None:
                request.instance_groups_set_named_ports_request_resource = (
                    instance_groups_set_named_ports_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_named_ports]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-compute",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("InstanceGroupsClient",)
