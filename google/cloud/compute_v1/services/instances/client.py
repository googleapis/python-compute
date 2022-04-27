# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import functools
import os
import re
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import extended_operation
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

from google.api_core import extended_operation  # type: ignore
from google.cloud.compute_v1.services.instances import pagers
from google.cloud.compute_v1.types import compute
from .transports.base import InstancesTransport, DEFAULT_CLIENT_INFO
from .transports.rest import InstancesRestTransport


class InstancesClientMeta(type):
    """Metaclass for the Instances client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[InstancesTransport]]
    _transport_registry["rest"] = InstancesRestTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[InstancesTransport]:
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


class InstancesClient(metaclass=InstancesClientMeta):
    """The Instances API."""

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
            InstancesClient: The constructed client.
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
            InstancesClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> InstancesTransport:
        """Returns the transport used by the client instance.

        Returns:
            InstancesTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
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
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
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
        transport: Union[str, InstancesTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the instances client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, InstancesTransport]): The
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
        if isinstance(transport, InstancesTransport):
            # transport is a InstancesTransport instance.
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

    def add_access_config_unary(
        self,
        request: Union[compute.AddAccessConfigInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        network_interface: str = None,
        access_config_resource: compute.AccessConfig = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Adds an access config to an instance's network
        interface.

        Args:
            request (Union[google.cloud.compute_v1.types.AddAccessConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.AddAccessConfig. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface to
                add to this instance.

                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_config_resource (google.cloud.compute_v1.types.AccessConfig):
                The body resource for this request
                This corresponds to the ``access_config_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, network_interface, access_config_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddAccessConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddAccessConfigInstanceRequest):
            request = compute.AddAccessConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if network_interface is not None:
                request.network_interface = network_interface
            if access_config_resource is not None:
                request.access_config_resource = access_config_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_access_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def add_access_config(
        self,
        request: Union[compute.AddAccessConfigInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        network_interface: str = None,
        access_config_resource: compute.AccessConfig = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Adds an access config to an instance's network
        interface.

        Args:
            request (Union[google.cloud.compute_v1.types.AddAccessConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.AddAccessConfig. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface to
                add to this instance.

                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_config_resource (google.cloud.compute_v1.types.AccessConfig):
                The body resource for this request
                This corresponds to the ``access_config_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, network_interface, access_config_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddAccessConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddAccessConfigInstanceRequest):
            request = compute.AddAccessConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if network_interface is not None:
                request.network_interface = network_interface
            if access_config_resource is not None:
                request.access_config_resource = access_config_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_access_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def add_resource_policies_unary(
        self,
        request: Union[compute.AddResourcePoliciesInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_add_resource_policies_request_resource: compute.InstancesAddResourcePoliciesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Adds existing resource policies to an instance. You
        can only add one policy right now which will be applied
        to this instance for scheduling live migrations.

        Args:
            request (Union[google.cloud.compute_v1.types.AddResourcePoliciesInstanceRequest, dict]):
                The request object. A request message for
                Instances.AddResourcePolicies. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_add_resource_policies_request_resource (google.cloud.compute_v1.types.InstancesAddResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``instances_add_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_add_resource_policies_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddResourcePoliciesInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddResourcePoliciesInstanceRequest):
            request = compute.AddResourcePoliciesInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_add_resource_policies_request_resource is not None:
                request.instances_add_resource_policies_request_resource = (
                    instances_add_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def add_resource_policies(
        self,
        request: Union[compute.AddResourcePoliciesInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_add_resource_policies_request_resource: compute.InstancesAddResourcePoliciesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Adds existing resource policies to an instance. You
        can only add one policy right now which will be applied
        to this instance for scheduling live migrations.

        Args:
            request (Union[google.cloud.compute_v1.types.AddResourcePoliciesInstanceRequest, dict]):
                The request object. A request message for
                Instances.AddResourcePolicies. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_add_resource_policies_request_resource (google.cloud.compute_v1.types.InstancesAddResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``instances_add_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_add_resource_policies_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddResourcePoliciesInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddResourcePoliciesInstanceRequest):
            request = compute.AddResourcePoliciesInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_add_resource_policies_request_resource is not None:
                request.instances_add_resource_policies_request_resource = (
                    instances_add_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def aggregated_list(
        self,
        request: Union[compute.AggregatedListInstancesRequest, dict] = None,
        *,
        project: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.AggregatedListPager:
        r"""Retrieves an aggregated list of all of the instances
        in your project across all regions and zones. The
        performance of this method degrades when a filter is
        specified on a project that has a very large number of
        instances.

        Args:
            request (Union[google.cloud.compute_v1.types.AggregatedListInstancesRequest, dict]):
                The request object. A request message for
                Instances.AggregatedList. See the method description for
                details.
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
            google.cloud.compute_v1.services.instances.pagers.AggregatedListPager:
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
        # in a compute.AggregatedListInstancesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AggregatedListInstancesRequest):
            request = compute.AggregatedListInstancesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.aggregated_list]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", request.project),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.AggregatedListPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def attach_disk_unary(
        self,
        request: Union[compute.AttachDiskInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        attached_disk_resource: compute.AttachedDisk = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Attaches an existing Disk resource to an instance.
        You must first create the disk before you can attach it.
        It is not possible to create and attach a disk at the
        same time. For more information, read Adding a
        persistent disk to your instance.

        Args:
            request (Union[google.cloud.compute_v1.types.AttachDiskInstanceRequest, dict]):
                The request object. A request message for
                Instances.AttachDisk. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attached_disk_resource (google.cloud.compute_v1.types.AttachedDisk):
                The body resource for this request
                This corresponds to the ``attached_disk_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, attached_disk_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AttachDiskInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AttachDiskInstanceRequest):
            request = compute.AttachDiskInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if attached_disk_resource is not None:
                request.attached_disk_resource = attached_disk_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.attach_disk]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def attach_disk(
        self,
        request: Union[compute.AttachDiskInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        attached_disk_resource: compute.AttachedDisk = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Attaches an existing Disk resource to an instance.
        You must first create the disk before you can attach it.
        It is not possible to create and attach a disk at the
        same time. For more information, read Adding a
        persistent disk to your instance.

        Args:
            request (Union[google.cloud.compute_v1.types.AttachDiskInstanceRequest, dict]):
                The request object. A request message for
                Instances.AttachDisk. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attached_disk_resource (google.cloud.compute_v1.types.AttachedDisk):
                The body resource for this request
                This corresponds to the ``attached_disk_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, attached_disk_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AttachDiskInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AttachDiskInstanceRequest):
            request = compute.AttachDiskInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if attached_disk_resource is not None:
                request.attached_disk_resource = attached_disk_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.attach_disk]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def bulk_insert_unary(
        self,
        request: Union[compute.BulkInsertInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        bulk_insert_instance_resource_resource: compute.BulkInsertInstanceResource = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates multiple instances. Count specifies the
        number of instances to create.

        Args:
            request (Union[google.cloud.compute_v1.types.BulkInsertInstanceRequest, dict]):
                The request object. A request message for
                Instances.BulkInsert. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            bulk_insert_instance_resource_resource (google.cloud.compute_v1.types.BulkInsertInstanceResource):
                The body resource for this request
                This corresponds to the ``bulk_insert_instance_resource_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, bulk_insert_instance_resource_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.BulkInsertInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.BulkInsertInstanceRequest):
            request = compute.BulkInsertInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if bulk_insert_instance_resource_resource is not None:
                request.bulk_insert_instance_resource_resource = (
                    bulk_insert_instance_resource_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.bulk_insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def bulk_insert(
        self,
        request: Union[compute.BulkInsertInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        bulk_insert_instance_resource_resource: compute.BulkInsertInstanceResource = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Creates multiple instances. Count specifies the
        number of instances to create.

        Args:
            request (Union[google.cloud.compute_v1.types.BulkInsertInstanceRequest, dict]):
                The request object. A request message for
                Instances.BulkInsert. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            bulk_insert_instance_resource_resource (google.cloud.compute_v1.types.BulkInsertInstanceResource):
                The body resource for this request
                This corresponds to the ``bulk_insert_instance_resource_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, bulk_insert_instance_resource_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.BulkInsertInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.BulkInsertInstanceRequest):
            request = compute.BulkInsertInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if bulk_insert_instance_resource_resource is not None:
                request.bulk_insert_instance_resource_resource = (
                    bulk_insert_instance_resource_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.bulk_insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def delete_unary(
        self,
        request: Union[compute.DeleteInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes the specified Instance resource. For more
        information, see Deleting an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteInstanceRequest, dict]):
                The request object. A request message for
                Instances.Delete. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                delete.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteInstanceRequest):
            request = compute.DeleteInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete(
        self,
        request: Union[compute.DeleteInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Deletes the specified Instance resource. For more
        information, see Deleting an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteInstanceRequest, dict]):
                The request object. A request message for
                Instances.Delete. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                delete.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteInstanceRequest):
            request = compute.DeleteInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def delete_access_config_unary(
        self,
        request: Union[compute.DeleteAccessConfigInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        access_config: str = None,
        network_interface: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes an access config from an instance's network
        interface.

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteAccessConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.DeleteAccessConfig. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_config (str):
                The name of the access config to
                delete.

                This corresponds to the ``access_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface.
                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, access_config, network_interface]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteAccessConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteAccessConfigInstanceRequest):
            request = compute.DeleteAccessConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if access_config is not None:
                request.access_config = access_config
            if network_interface is not None:
                request.network_interface = network_interface

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_access_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_access_config(
        self,
        request: Union[compute.DeleteAccessConfigInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        access_config: str = None,
        network_interface: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Deletes an access config from an instance's network
        interface.

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteAccessConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.DeleteAccessConfig. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_config (str):
                The name of the access config to
                delete.

                This corresponds to the ``access_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface.
                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, access_config, network_interface]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteAccessConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteAccessConfigInstanceRequest):
            request = compute.DeleteAccessConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if access_config is not None:
                request.access_config = access_config
            if network_interface is not None:
                request.network_interface = network_interface

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_access_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def detach_disk_unary(
        self,
        request: Union[compute.DetachDiskInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        device_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Detaches a disk from an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.DetachDiskInstanceRequest, dict]):
                The request object. A request message for
                Instances.DetachDisk. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device_name (str):
                The device name of the disk to
                detach. Make a get() request on the
                instance to view currently attached
                disks and device names.

                This corresponds to the ``device_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, device_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DetachDiskInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DetachDiskInstanceRequest):
            request = compute.DetachDiskInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if device_name is not None:
                request.device_name = device_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.detach_disk]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def detach_disk(
        self,
        request: Union[compute.DetachDiskInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        device_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Detaches a disk from an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.DetachDiskInstanceRequest, dict]):
                The request object. A request message for
                Instances.DetachDisk. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device_name (str):
                The device name of the disk to
                detach. Make a get() request on the
                instance to view currently attached
                disks and device names.

                This corresponds to the ``device_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, device_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DetachDiskInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DetachDiskInstanceRequest):
            request = compute.DetachDiskInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if device_name is not None:
                request.device_name = device_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.detach_disk]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def get(
        self,
        request: Union[compute.GetInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Instance:
        r"""Returns the specified Instance resource. Gets a list
        of available instances by making a list() request.

        Args:
            request (Union[google.cloud.compute_v1.types.GetInstanceRequest, dict]):
                The request object. A request message for Instances.Get.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                return.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Instance:
                Represents an Instance resource. An
                instance is a virtual machine that is
                hosted on Google Cloud Platform. For
                more information, read Virtual Machine
                Instances.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetInstanceRequest):
            request = compute.GetInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_effective_firewalls(
        self,
        request: Union[compute.GetEffectiveFirewallsInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        network_interface: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.InstancesGetEffectiveFirewallsResponse:
        r"""Returns effective firewalls applied to an interface
        of the instance.

        Args:
            request (Union[google.cloud.compute_v1.types.GetEffectiveFirewallsInstanceRequest, dict]):
                The request object. A request message for
                Instances.GetEffectiveFirewalls. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface to
                get the effective firewalls.

                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.InstancesGetEffectiveFirewallsResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, network_interface])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetEffectiveFirewallsInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetEffectiveFirewallsInstanceRequest):
            request = compute.GetEffectiveFirewallsInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if network_interface is not None:
                request.network_interface = network_interface

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_effective_firewalls]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_guest_attributes(
        self,
        request: Union[compute.GetGuestAttributesInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.GuestAttributes:
        r"""Returns the specified guest attributes entry.

        Args:
            request (Union[google.cloud.compute_v1.types.GetGuestAttributesInstanceRequest, dict]):
                The request object. A request message for
                Instances.GetGuestAttributes. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.GuestAttributes:
                A guest attributes entry.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetGuestAttributesInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetGuestAttributesInstanceRequest):
            request = compute.GetGuestAttributesInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_guest_attributes]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: Union[compute.GetIamPolicyInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Gets the access control policy for a resource. May be
        empty if no such policy or resource exists.

        Args:
            request (Union[google.cloud.compute_v1.types.GetIamPolicyInstanceRequest, dict]):
                The request object. A request message for
                Instances.GetIamPolicy. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                Policy is a collection of bindings. A binding binds one
                or more members, or principals, to a single role.
                Principals can be user accounts, service accounts,
                Google groups, and domains (such as G Suite). A role is
                a named list of permissions; each role can be an IAM
                predefined role or a user-created custom role. For some
                types of Google Cloud resources, a binding can also
                specify a condition, which is a logical expression that
                allows access to a resource only if the expression
                evaluates to true. A condition can add constraints based
                on attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the [IAM
                documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).
                **JSON example:** { "bindings": [ { "role":
                "roles/resourcemanager.organizationAdmin", "members": [
                "user:mike@example.com", "group:admins@example.com",
                "domain:google.com",
                "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                ] }, { "role":
                "roles/resourcemanager.organizationViewer", "members": [
                "user:eve@example.com" ], "condition": { "title":
                "expirable access", "description": "Does not grant
                access after Sep 2020", "expression": "request.time <
                timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag":
                "BwWWja0YfJA=", "version": 3 } **YAML example:**
                bindings: - members: - user:\ mike@example.com -
                group:\ admins@example.com - domain:google.com -
                serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:\ eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA=
                version: 3 For a description of IAM and its features,
                see the [IAM
                documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetIamPolicyInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetIamPolicyInstanceRequest):
            request = compute.GetIamPolicyInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_screenshot(
        self,
        request: Union[compute.GetScreenshotInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Screenshot:
        r"""Returns the screenshot from the specified instance.

        Args:
            request (Union[google.cloud.compute_v1.types.GetScreenshotInstanceRequest, dict]):
                The request object. A request message for
                Instances.GetScreenshot. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Screenshot:
                An instance's screenshot.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetScreenshotInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetScreenshotInstanceRequest):
            request = compute.GetScreenshotInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_screenshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_serial_port_output(
        self,
        request: Union[compute.GetSerialPortOutputInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SerialPortOutput:
        r"""Returns the last 1 MB of serial port output from the
        specified instance.

        Args:
            request (Union[google.cloud.compute_v1.types.GetSerialPortOutputInstanceRequest, dict]):
                The request object. A request message for
                Instances.GetSerialPortOutput. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance for this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.SerialPortOutput:
                An instance serial console output.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetSerialPortOutputInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetSerialPortOutputInstanceRequest):
            request = compute.GetSerialPortOutputInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_serial_port_output]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_shielded_instance_identity(
        self,
        request: Union[compute.GetShieldedInstanceIdentityInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.ShieldedInstanceIdentity:
        r"""Returns the Shielded Instance Identity of an instance

        Args:
            request (Union[google.cloud.compute_v1.types.GetShieldedInstanceIdentityInstanceRequest, dict]):
                The request object. A request message for
                Instances.GetShieldedInstanceIdentity. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name or id of the instance scoping
                this request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.ShieldedInstanceIdentity:
                A Shielded Instance Identity.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetShieldedInstanceIdentityInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetShieldedInstanceIdentityInstanceRequest):
            request = compute.GetShieldedInstanceIdentityInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_shielded_instance_identity
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def insert_unary(
        self,
        request: Union[compute.InsertInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_resource: compute.Instance = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates an instance resource in the specified project
        using the data included in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.InsertInstanceRequest, dict]):
                The request object. A request message for
                Instances.Insert. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_resource (google.cloud.compute_v1.types.Instance):
                The body resource for this request
                This corresponds to the ``instance_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.InsertInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.InsertInstanceRequest):
            request = compute.InsertInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_resource is not None:
                request.instance_resource = instance_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def insert(
        self,
        request: Union[compute.InsertInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance_resource: compute.Instance = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Creates an instance resource in the specified project
        using the data included in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.InsertInstanceRequest, dict]):
                The request object. A request message for
                Instances.Insert. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_resource (google.cloud.compute_v1.types.Instance):
                The body resource for this request
                This corresponds to the ``instance_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.InsertInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.InsertInstanceRequest):
            request = compute.InsertInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_resource is not None:
                request.instance_resource = instance_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def list(
        self,
        request: Union[compute.ListInstancesRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPager:
        r"""Retrieves the list of instances contained within the
        specified zone.

        Args:
            request (Union[google.cloud.compute_v1.types.ListInstancesRequest, dict]):
                The request object. A request message for
                Instances.List. See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instances.pagers.ListPager:
                Contains a list of instances.
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
        # in a compute.ListInstancesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListInstancesRequest):
            request = compute.ListInstancesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_referrers(
        self,
        request: Union[compute.ListReferrersInstancesRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReferrersPager:
        r"""Retrieves a list of resources that refer to the VM
        instance specified in the request. For example, if the
        VM instance is part of a managed or unmanaged instance
        group, the referrers list includes the instance group.
        For more information, read Viewing referrers to VM
        instances.

        Args:
            request (Union[google.cloud.compute_v1.types.ListReferrersInstancesRequest, dict]):
                The request object. A request message for
                Instances.ListReferrers. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the target instance scoping
                this request, or '-' if the request
                should span over all instances in the
                container.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instances.pagers.ListReferrersPager:
                Contains a list of instance
                referrers.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ListReferrersInstancesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListReferrersInstancesRequest):
            request = compute.ListReferrersInstancesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_referrers]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListReferrersPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def remove_resource_policies_unary(
        self,
        request: Union[compute.RemoveResourcePoliciesInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_remove_resource_policies_request_resource: compute.InstancesRemoveResourcePoliciesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Removes resource policies from an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.RemoveResourcePoliciesInstanceRequest, dict]):
                The request object. A request message for
                Instances.RemoveResourcePolicies. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_remove_resource_policies_request_resource (google.cloud.compute_v1.types.InstancesRemoveResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``instances_remove_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance,
                instances_remove_resource_policies_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.RemoveResourcePoliciesInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.RemoveResourcePoliciesInstanceRequest):
            request = compute.RemoveResourcePoliciesInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_remove_resource_policies_request_resource is not None:
                request.instances_remove_resource_policies_request_resource = (
                    instances_remove_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def remove_resource_policies(
        self,
        request: Union[compute.RemoveResourcePoliciesInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_remove_resource_policies_request_resource: compute.InstancesRemoveResourcePoliciesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Removes resource policies from an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.RemoveResourcePoliciesInstanceRequest, dict]):
                The request object. A request message for
                Instances.RemoveResourcePolicies. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_remove_resource_policies_request_resource (google.cloud.compute_v1.types.InstancesRemoveResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``instances_remove_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance,
                instances_remove_resource_policies_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.RemoveResourcePoliciesInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.RemoveResourcePoliciesInstanceRequest):
            request = compute.RemoveResourcePoliciesInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_remove_resource_policies_request_resource is not None:
                request.instances_remove_resource_policies_request_resource = (
                    instances_remove_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def reset_unary(
        self,
        request: Union[compute.ResetInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Performs a reset on the instance. This is a hard
        reset. The VM does not do a graceful shutdown. For more
        information, see Resetting an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.ResetInstanceRequest, dict]):
                The request object. A request message for
                Instances.Reset. See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ResetInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ResetInstanceRequest):
            request = compute.ResetInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def reset(
        self,
        request: Union[compute.ResetInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Performs a reset on the instance. This is a hard
        reset. The VM does not do a graceful shutdown. For more
        information, see Resetting an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.ResetInstanceRequest, dict]):
                The request object. A request message for
                Instances.Reset. See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ResetInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ResetInstanceRequest):
            request = compute.ResetInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def resume_unary(
        self,
        request: Union[compute.ResumeInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Resumes an instance that was suspended using the
        instances().suspend method.

        Args:
            request (Union[google.cloud.compute_v1.types.ResumeInstanceRequest, dict]):
                The request object. A request message for
                Instances.Resume. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                resume.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ResumeInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ResumeInstanceRequest):
            request = compute.ResumeInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resume]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def resume(
        self,
        request: Union[compute.ResumeInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Resumes an instance that was suspended using the
        instances().suspend method.

        Args:
            request (Union[google.cloud.compute_v1.types.ResumeInstanceRequest, dict]):
                The request object. A request message for
                Instances.Resume. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                resume.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ResumeInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ResumeInstanceRequest):
            request = compute.ResumeInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resume]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def send_diagnostic_interrupt(
        self,
        request: Union[compute.SendDiagnosticInterruptInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SendDiagnosticInterruptInstanceResponse:
        r"""Sends diagnostic interrupt to the instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SendDiagnosticInterruptInstanceRequest, dict]):
                The request object. A request message for
                Instances.SendDiagnosticInterrupt. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.SendDiagnosticInterruptInstanceResponse:
                A response message for
                Instances.SendDiagnosticInterrupt. See
                the method description for details.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SendDiagnosticInterruptInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SendDiagnosticInterruptInstanceRequest):
            request = compute.SendDiagnosticInterruptInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.send_diagnostic_interrupt
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_deletion_protection_unary(
        self,
        request: Union[compute.SetDeletionProtectionInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets deletion protection on the instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SetDeletionProtectionInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetDeletionProtection. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetDeletionProtectionInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetDeletionProtectionInstanceRequest):
            request = compute.SetDeletionProtectionInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_deletion_protection]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_deletion_protection(
        self,
        request: Union[compute.SetDeletionProtectionInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets deletion protection on the instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SetDeletionProtectionInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetDeletionProtection. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetDeletionProtectionInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetDeletionProtectionInstanceRequest):
            request = compute.SetDeletionProtectionInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_deletion_protection]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_disk_auto_delete_unary(
        self,
        request: Union[compute.SetDiskAutoDeleteInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        auto_delete: bool = None,
        device_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets the auto-delete flag for a disk attached to an
        instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SetDiskAutoDeleteInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetDiskAutoDelete. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            auto_delete (bool):
                Whether to auto-delete the disk when
                the instance is deleted.

                This corresponds to the ``auto_delete`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device_name (str):
                The device name of the disk to
                modify. Make a get() request on the
                instance to view currently attached
                disks and device names.

                This corresponds to the ``device_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, auto_delete, device_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetDiskAutoDeleteInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetDiskAutoDeleteInstanceRequest):
            request = compute.SetDiskAutoDeleteInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if auto_delete is not None:
                request.auto_delete = auto_delete
            if device_name is not None:
                request.device_name = device_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_disk_auto_delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_disk_auto_delete(
        self,
        request: Union[compute.SetDiskAutoDeleteInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        auto_delete: bool = None,
        device_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets the auto-delete flag for a disk attached to an
        instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SetDiskAutoDeleteInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetDiskAutoDelete. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            auto_delete (bool):
                Whether to auto-delete the disk when
                the instance is deleted.

                This corresponds to the ``auto_delete`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device_name (str):
                The device name of the disk to
                modify. Make a get() request on the
                instance to view currently attached
                disks and device names.

                This corresponds to the ``device_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, auto_delete, device_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetDiskAutoDeleteInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetDiskAutoDeleteInstanceRequest):
            request = compute.SetDiskAutoDeleteInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if auto_delete is not None:
                request.auto_delete = auto_delete
            if device_name is not None:
                request.device_name = device_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_disk_auto_delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: Union[compute.SetIamPolicyInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        resource: str = None,
        zone_set_policy_request_resource: compute.ZoneSetPolicyRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Sets the access control policy on the specified
        resource. Replaces any existing policy.

        Args:
            request (Union[google.cloud.compute_v1.types.SetIamPolicyInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetIamPolicy. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone_set_policy_request_resource (google.cloud.compute_v1.types.ZoneSetPolicyRequest):
                The body resource for this request
                This corresponds to the ``zone_set_policy_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                Policy is a collection of bindings. A binding binds one
                or more members, or principals, to a single role.
                Principals can be user accounts, service accounts,
                Google groups, and domains (such as G Suite). A role is
                a named list of permissions; each role can be an IAM
                predefined role or a user-created custom role. For some
                types of Google Cloud resources, a binding can also
                specify a condition, which is a logical expression that
                allows access to a resource only if the expression
                evaluates to true. A condition can add constraints based
                on attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the [IAM
                documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).
                **JSON example:** { "bindings": [ { "role":
                "roles/resourcemanager.organizationAdmin", "members": [
                "user:mike@example.com", "group:admins@example.com",
                "domain:google.com",
                "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                ] }, { "role":
                "roles/resourcemanager.organizationViewer", "members": [
                "user:eve@example.com" ], "condition": { "title":
                "expirable access", "description": "Does not grant
                access after Sep 2020", "expression": "request.time <
                timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag":
                "BwWWja0YfJA=", "version": 3 } **YAML example:**
                bindings: - members: - user:\ mike@example.com -
                group:\ admins@example.com - domain:google.com -
                serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:\ eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA=
                version: 3 For a description of IAM and its features,
                see the [IAM
                documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, resource, zone_set_policy_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetIamPolicyInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetIamPolicyInstanceRequest):
            request = compute.SetIamPolicyInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource
            if zone_set_policy_request_resource is not None:
                request.zone_set_policy_request_resource = (
                    zone_set_policy_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_labels_unary(
        self,
        request: Union[compute.SetLabelsInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_labels_request_resource: compute.InstancesSetLabelsRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets labels on an instance. To learn more about
        labels, read the Labeling Resources documentation.

        Args:
            request (Union[google.cloud.compute_v1.types.SetLabelsInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetLabels. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_labels_request_resource (google.cloud.compute_v1.types.InstancesSetLabelsRequest):
                The body resource for this request
                This corresponds to the ``instances_set_labels_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_labels_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetLabelsInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetLabelsInstanceRequest):
            request = compute.SetLabelsInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_labels_request_resource is not None:
                request.instances_set_labels_request_resource = (
                    instances_set_labels_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_labels]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_labels(
        self,
        request: Union[compute.SetLabelsInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_labels_request_resource: compute.InstancesSetLabelsRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets labels on an instance. To learn more about
        labels, read the Labeling Resources documentation.

        Args:
            request (Union[google.cloud.compute_v1.types.SetLabelsInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetLabels. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_labels_request_resource (google.cloud.compute_v1.types.InstancesSetLabelsRequest):
                The body resource for this request
                This corresponds to the ``instances_set_labels_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_labels_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetLabelsInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetLabelsInstanceRequest):
            request = compute.SetLabelsInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_labels_request_resource is not None:
                request.instances_set_labels_request_resource = (
                    instances_set_labels_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_labels]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_machine_resources_unary(
        self,
        request: Union[compute.SetMachineResourcesInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_machine_resources_request_resource: compute.InstancesSetMachineResourcesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Changes the number and/or type of accelerator for a
        stopped instance to the values specified in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMachineResourcesInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMachineResources. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_machine_resources_request_resource (google.cloud.compute_v1.types.InstancesSetMachineResourcesRequest):
                The body resource for this request
                This corresponds to the ``instances_set_machine_resources_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_machine_resources_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMachineResourcesInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMachineResourcesInstanceRequest):
            request = compute.SetMachineResourcesInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_machine_resources_request_resource is not None:
                request.instances_set_machine_resources_request_resource = (
                    instances_set_machine_resources_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_machine_resources]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_machine_resources(
        self,
        request: Union[compute.SetMachineResourcesInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_machine_resources_request_resource: compute.InstancesSetMachineResourcesRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Changes the number and/or type of accelerator for a
        stopped instance to the values specified in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMachineResourcesInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMachineResources. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_machine_resources_request_resource (google.cloud.compute_v1.types.InstancesSetMachineResourcesRequest):
                The body resource for this request
                This corresponds to the ``instances_set_machine_resources_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_machine_resources_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMachineResourcesInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMachineResourcesInstanceRequest):
            request = compute.SetMachineResourcesInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_machine_resources_request_resource is not None:
                request.instances_set_machine_resources_request_resource = (
                    instances_set_machine_resources_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_machine_resources]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_machine_type_unary(
        self,
        request: Union[compute.SetMachineTypeInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_machine_type_request_resource: compute.InstancesSetMachineTypeRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Changes the machine type for a stopped instance to
        the machine type specified in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMachineTypeInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMachineType. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_machine_type_request_resource (google.cloud.compute_v1.types.InstancesSetMachineTypeRequest):
                The body resource for this request
                This corresponds to the ``instances_set_machine_type_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_machine_type_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMachineTypeInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMachineTypeInstanceRequest):
            request = compute.SetMachineTypeInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_machine_type_request_resource is not None:
                request.instances_set_machine_type_request_resource = (
                    instances_set_machine_type_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_machine_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_machine_type(
        self,
        request: Union[compute.SetMachineTypeInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_machine_type_request_resource: compute.InstancesSetMachineTypeRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Changes the machine type for a stopped instance to
        the machine type specified in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMachineTypeInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMachineType. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_machine_type_request_resource (google.cloud.compute_v1.types.InstancesSetMachineTypeRequest):
                The body resource for this request
                This corresponds to the ``instances_set_machine_type_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_machine_type_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMachineTypeInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMachineTypeInstanceRequest):
            request = compute.SetMachineTypeInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_machine_type_request_resource is not None:
                request.instances_set_machine_type_request_resource = (
                    instances_set_machine_type_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_machine_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_metadata_unary(
        self,
        request: Union[compute.SetMetadataInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        metadata_resource: compute.Metadata = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets metadata for the specified instance to the data
        included in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMetadataInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMetadata. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_resource (google.cloud.compute_v1.types.Metadata):
                The body resource for this request
                This corresponds to the ``metadata_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, metadata_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMetadataInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMetadataInstanceRequest):
            request = compute.SetMetadataInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if metadata_resource is not None:
                request.metadata_resource = metadata_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_metadata]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_metadata(
        self,
        request: Union[compute.SetMetadataInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        metadata_resource: compute.Metadata = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets metadata for the specified instance to the data
        included in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMetadataInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMetadata. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_resource (google.cloud.compute_v1.types.Metadata):
                The body resource for this request
                This corresponds to the ``metadata_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, metadata_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMetadataInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMetadataInstanceRequest):
            request = compute.SetMetadataInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if metadata_resource is not None:
                request.metadata_resource = metadata_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_metadata]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_min_cpu_platform_unary(
        self,
        request: Union[compute.SetMinCpuPlatformInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_min_cpu_platform_request_resource: compute.InstancesSetMinCpuPlatformRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Changes the minimum CPU platform that this instance
        should use. This method can only be called on a stopped
        instance. For more information, read Specifying a
        Minimum CPU Platform.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMinCpuPlatformInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMinCpuPlatform. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_min_cpu_platform_request_resource (google.cloud.compute_v1.types.InstancesSetMinCpuPlatformRequest):
                The body resource for this request
                This corresponds to the ``instances_set_min_cpu_platform_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_min_cpu_platform_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMinCpuPlatformInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMinCpuPlatformInstanceRequest):
            request = compute.SetMinCpuPlatformInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_min_cpu_platform_request_resource is not None:
                request.instances_set_min_cpu_platform_request_resource = (
                    instances_set_min_cpu_platform_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_min_cpu_platform]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_min_cpu_platform(
        self,
        request: Union[compute.SetMinCpuPlatformInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_min_cpu_platform_request_resource: compute.InstancesSetMinCpuPlatformRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Changes the minimum CPU platform that this instance
        should use. This method can only be called on a stopped
        instance. For more information, read Specifying a
        Minimum CPU Platform.

        Args:
            request (Union[google.cloud.compute_v1.types.SetMinCpuPlatformInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetMinCpuPlatform. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_min_cpu_platform_request_resource (google.cloud.compute_v1.types.InstancesSetMinCpuPlatformRequest):
                The body resource for this request
                This corresponds to the ``instances_set_min_cpu_platform_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_min_cpu_platform_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetMinCpuPlatformInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetMinCpuPlatformInstanceRequest):
            request = compute.SetMinCpuPlatformInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_min_cpu_platform_request_resource is not None:
                request.instances_set_min_cpu_platform_request_resource = (
                    instances_set_min_cpu_platform_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_min_cpu_platform]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_scheduling_unary(
        self,
        request: Union[compute.SetSchedulingInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        scheduling_resource: compute.Scheduling = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets an instance's scheduling options. You can only call this
        method on a stopped instance, that is, a VM instance that is in
        a ``TERMINATED`` state. See Instance Life Cycle for more
        information on the possible instance states. For more
        information about setting scheduling options for a VM, see Set
        VM availability policies.

        Args:
            request (Union[google.cloud.compute_v1.types.SetSchedulingInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetScheduling. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            scheduling_resource (google.cloud.compute_v1.types.Scheduling):
                The body resource for this request
                This corresponds to the ``scheduling_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, scheduling_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetSchedulingInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetSchedulingInstanceRequest):
            request = compute.SetSchedulingInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if scheduling_resource is not None:
                request.scheduling_resource = scheduling_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_scheduling]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_scheduling(
        self,
        request: Union[compute.SetSchedulingInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        scheduling_resource: compute.Scheduling = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets an instance's scheduling options. You can only call this
        method on a stopped instance, that is, a VM instance that is in
        a ``TERMINATED`` state. See Instance Life Cycle for more
        information on the possible instance states. For more
        information about setting scheduling options for a VM, see Set
        VM availability policies.

        Args:
            request (Union[google.cloud.compute_v1.types.SetSchedulingInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetScheduling. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            scheduling_resource (google.cloud.compute_v1.types.Scheduling):
                The body resource for this request
                This corresponds to the ``scheduling_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, scheduling_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetSchedulingInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetSchedulingInstanceRequest):
            request = compute.SetSchedulingInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if scheduling_resource is not None:
                request.scheduling_resource = scheduling_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_scheduling]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_service_account_unary(
        self,
        request: Union[compute.SetServiceAccountInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_service_account_request_resource: compute.InstancesSetServiceAccountRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets the service account on the instance. For more
        information, read Changing the service account and
        access scopes for an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SetServiceAccountInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetServiceAccount. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                start.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_service_account_request_resource (google.cloud.compute_v1.types.InstancesSetServiceAccountRequest):
                The body resource for this request
                This corresponds to the ``instances_set_service_account_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_service_account_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetServiceAccountInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetServiceAccountInstanceRequest):
            request = compute.SetServiceAccountInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_service_account_request_resource is not None:
                request.instances_set_service_account_request_resource = (
                    instances_set_service_account_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_service_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_service_account(
        self,
        request: Union[compute.SetServiceAccountInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_set_service_account_request_resource: compute.InstancesSetServiceAccountRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets the service account on the instance. For more
        information, read Changing the service account and
        access scopes for an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SetServiceAccountInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetServiceAccount. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                start.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_set_service_account_request_resource (google.cloud.compute_v1.types.InstancesSetServiceAccountRequest):
                The body resource for this request
                This corresponds to the ``instances_set_service_account_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, instances_set_service_account_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetServiceAccountInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetServiceAccountInstanceRequest):
            request = compute.SetServiceAccountInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_set_service_account_request_resource is not None:
                request.instances_set_service_account_request_resource = (
                    instances_set_service_account_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_service_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_shielded_instance_integrity_policy_unary(
        self,
        request: Union[
            compute.SetShieldedInstanceIntegrityPolicyInstanceRequest, dict
        ] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        shielded_instance_integrity_policy_resource: compute.ShieldedInstanceIntegrityPolicy = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets the Shielded Instance integrity policy for an
        instance. You can only use this method on a running
        instance. This method supports PATCH semantics and uses
        the JSON merge patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.SetShieldedInstanceIntegrityPolicyInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetShieldedInstanceIntegrityPolicy. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name or id of the instance scoping
                this request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            shielded_instance_integrity_policy_resource (google.cloud.compute_v1.types.ShieldedInstanceIntegrityPolicy):
                The body resource for this request
                This corresponds to the ``shielded_instance_integrity_policy_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, shielded_instance_integrity_policy_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetShieldedInstanceIntegrityPolicyInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, compute.SetShieldedInstanceIntegrityPolicyInstanceRequest
        ):
            request = compute.SetShieldedInstanceIntegrityPolicyInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if shielded_instance_integrity_policy_resource is not None:
                request.shielded_instance_integrity_policy_resource = (
                    shielded_instance_integrity_policy_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.set_shielded_instance_integrity_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_shielded_instance_integrity_policy(
        self,
        request: Union[
            compute.SetShieldedInstanceIntegrityPolicyInstanceRequest, dict
        ] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        shielded_instance_integrity_policy_resource: compute.ShieldedInstanceIntegrityPolicy = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets the Shielded Instance integrity policy for an
        instance. You can only use this method on a running
        instance. This method supports PATCH semantics and uses
        the JSON merge patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.SetShieldedInstanceIntegrityPolicyInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetShieldedInstanceIntegrityPolicy. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name or id of the instance scoping
                this request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            shielded_instance_integrity_policy_resource (google.cloud.compute_v1.types.ShieldedInstanceIntegrityPolicy):
                The body resource for this request
                This corresponds to the ``shielded_instance_integrity_policy_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, shielded_instance_integrity_policy_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetShieldedInstanceIntegrityPolicyInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, compute.SetShieldedInstanceIntegrityPolicyInstanceRequest
        ):
            request = compute.SetShieldedInstanceIntegrityPolicyInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if shielded_instance_integrity_policy_resource is not None:
                request.shielded_instance_integrity_policy_resource = (
                    shielded_instance_integrity_policy_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.set_shielded_instance_integrity_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_tags_unary(
        self,
        request: Union[compute.SetTagsInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        tags_resource: compute.Tags = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets network tags for the specified instance to the
        data included in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetTagsInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetTags. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tags_resource (google.cloud.compute_v1.types.Tags):
                The body resource for this request
                This corresponds to the ``tags_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, tags_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetTagsInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetTagsInstanceRequest):
            request = compute.SetTagsInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if tags_resource is not None:
                request.tags_resource = tags_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_tags]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_tags(
        self,
        request: Union[compute.SetTagsInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        tags_resource: compute.Tags = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets network tags for the specified instance to the
        data included in the request.

        Args:
            request (Union[google.cloud.compute_v1.types.SetTagsInstanceRequest, dict]):
                The request object. A request message for
                Instances.SetTags. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tags_resource (google.cloud.compute_v1.types.Tags):
                The body resource for this request
                This corresponds to the ``tags_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, tags_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetTagsInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetTagsInstanceRequest):
            request = compute.SetTagsInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if tags_resource is not None:
                request.tags_resource = tags_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_tags]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def simulate_maintenance_event_unary(
        self,
        request: Union[compute.SimulateMaintenanceEventInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Simulates a host maintenance event on a VM. For more
        information, see Simulate a host maintenance event.

        Args:
            request (Union[google.cloud.compute_v1.types.SimulateMaintenanceEventInstanceRequest, dict]):
                The request object. A request message for
                Instances.SimulateMaintenanceEvent. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SimulateMaintenanceEventInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SimulateMaintenanceEventInstanceRequest):
            request = compute.SimulateMaintenanceEventInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.simulate_maintenance_event
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def simulate_maintenance_event(
        self,
        request: Union[compute.SimulateMaintenanceEventInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Simulates a host maintenance event on a VM. For more
        information, see Simulate a host maintenance event.

        Args:
            request (Union[google.cloud.compute_v1.types.SimulateMaintenanceEventInstanceRequest, dict]):
                The request object. A request message for
                Instances.SimulateMaintenanceEvent. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SimulateMaintenanceEventInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SimulateMaintenanceEventInstanceRequest):
            request = compute.SimulateMaintenanceEventInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.simulate_maintenance_event
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def start_unary(
        self,
        request: Union[compute.StartInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Starts an instance that was stopped using the
        instances().stop method. For more information, see
        Restart an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.StartInstanceRequest, dict]):
                The request object. A request message for
                Instances.Start. See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                start.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.StartInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.StartInstanceRequest):
            request = compute.StartInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def start(
        self,
        request: Union[compute.StartInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Starts an instance that was stopped using the
        instances().stop method. For more information, see
        Restart an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.StartInstanceRequest, dict]):
                The request object. A request message for
                Instances.Start. See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                start.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.StartInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.StartInstanceRequest):
            request = compute.StartInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def start_with_encryption_key_unary(
        self,
        request: Union[compute.StartWithEncryptionKeyInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_start_with_encryption_key_request_resource: compute.InstancesStartWithEncryptionKeyRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Starts an instance that was stopped using the
        instances().stop method. For more information, see
        Restart an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.StartWithEncryptionKeyInstanceRequest, dict]):
                The request object. A request message for
                Instances.StartWithEncryptionKey. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                start.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_start_with_encryption_key_request_resource (google.cloud.compute_v1.types.InstancesStartWithEncryptionKeyRequest):
                The body resource for this request
                This corresponds to the ``instances_start_with_encryption_key_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance,
                instances_start_with_encryption_key_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.StartWithEncryptionKeyInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.StartWithEncryptionKeyInstanceRequest):
            request = compute.StartWithEncryptionKeyInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_start_with_encryption_key_request_resource is not None:
                request.instances_start_with_encryption_key_request_resource = (
                    instances_start_with_encryption_key_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.start_with_encryption_key
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def start_with_encryption_key(
        self,
        request: Union[compute.StartWithEncryptionKeyInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instances_start_with_encryption_key_request_resource: compute.InstancesStartWithEncryptionKeyRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Starts an instance that was stopped using the
        instances().stop method. For more information, see
        Restart an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.StartWithEncryptionKeyInstanceRequest, dict]):
                The request object. A request message for
                Instances.StartWithEncryptionKey. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                start.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instances_start_with_encryption_key_request_resource (google.cloud.compute_v1.types.InstancesStartWithEncryptionKeyRequest):
                The body resource for this request
                This corresponds to the ``instances_start_with_encryption_key_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance,
                instances_start_with_encryption_key_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.StartWithEncryptionKeyInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.StartWithEncryptionKeyInstanceRequest):
            request = compute.StartWithEncryptionKeyInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instances_start_with_encryption_key_request_resource is not None:
                request.instances_start_with_encryption_key_request_resource = (
                    instances_start_with_encryption_key_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.start_with_encryption_key
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def stop_unary(
        self,
        request: Union[compute.StopInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Stops a running instance, shutting it down cleanly,
        and allows you to restart the instance at a later time.
        Stopped instances do not incur VM usage charges while
        they are stopped. However, resources that the VM is
        using, such as persistent disks and static IP addresses,
        will continue to be charged until they are deleted. For
        more information, see Stopping an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.StopInstanceRequest, dict]):
                The request object. A request message for
                Instances.Stop. See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                stop.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.StopInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.StopInstanceRequest):
            request = compute.StopInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def stop(
        self,
        request: Union[compute.StopInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Stops a running instance, shutting it down cleanly,
        and allows you to restart the instance at a later time.
        Stopped instances do not incur VM usage charges while
        they are stopped. However, resources that the VM is
        using, such as persistent disks and static IP addresses,
        will continue to be charged until they are deleted. For
        more information, see Stopping an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.StopInstanceRequest, dict]):
                The request object. A request message for
                Instances.Stop. See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                stop.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.StopInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.StopInstanceRequest):
            request = compute.StopInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def suspend_unary(
        self,
        request: Union[compute.SuspendInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""This method suspends a running instance, saving its
        state to persistent storage, and allows you to resume
        the instance at a later time. Suspended instances have
        no compute costs (cores or RAM), and incur only storage
        charges for the saved VM memory and localSSD data. Any
        charged resources the virtual machine was using, such as
        persistent disks and static IP addresses, will continue
        to be charged while the instance is suspended. For more
        information, see Suspending and resuming an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SuspendInstanceRequest, dict]):
                The request object. A request message for
                Instances.Suspend. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                suspend.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SuspendInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SuspendInstanceRequest):
            request = compute.SuspendInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.suspend]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def suspend(
        self,
        request: Union[compute.SuspendInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""This method suspends a running instance, saving its
        state to persistent storage, and allows you to resume
        the instance at a later time. Suspended instances have
        no compute costs (cores or RAM), and incur only storage
        charges for the saved VM memory and localSSD data. Any
        charged resources the virtual machine was using, such as
        persistent disks and static IP addresses, will continue
        to be charged while the instance is suspended. For more
        information, see Suspending and resuming an instance.

        Args:
            request (Union[google.cloud.compute_v1.types.SuspendInstanceRequest, dict]):
                The request object. A request message for
                Instances.Suspend. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                suspend.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SuspendInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SuspendInstanceRequest):
            request = compute.SuspendInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.suspend]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: Union[compute.TestIamPermissionsInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        resource: str = None,
        test_permissions_request_resource: compute.TestPermissionsRequest = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.TestPermissionsResponse:
        r"""Returns permissions that a caller has on the
        specified resource.

        Args:
            request (Union[google.cloud.compute_v1.types.TestIamPermissionsInstanceRequest, dict]):
                The request object. A request message for
                Instances.TestIamPermissions. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            test_permissions_request_resource (google.cloud.compute_v1.types.TestPermissionsRequest):
                The body resource for this request
                This corresponds to the ``test_permissions_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.TestPermissionsResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, resource, test_permissions_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.TestIamPermissionsInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.TestIamPermissionsInstanceRequest):
            request = compute.TestIamPermissionsInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource
            if test_permissions_request_resource is not None:
                request.test_permissions_request_resource = (
                    test_permissions_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_unary(
        self,
        request: Union[compute.UpdateInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instance_resource: compute.Instance = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Updates an instance only if the necessary resources
        are available. This method can update only a specific
        set of instance properties. See Updating a running
        instance for a list of updatable instance properties.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateInstanceRequest, dict]):
                The request object. A request message for
                Instances.Update. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                update.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_resource (google.cloud.compute_v1.types.Instance):
                The body resource for this request
                This corresponds to the ``instance_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, instance_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateInstanceRequest):
            request = compute.UpdateInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instance_resource is not None:
                request.instance_resource = instance_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update(
        self,
        request: Union[compute.UpdateInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        instance_resource: compute.Instance = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Updates an instance only if the necessary resources
        are available. This method can update only a specific
        set of instance properties. See Updating a running
        instance for a list of updatable instance properties.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateInstanceRequest, dict]):
                The request object. A request message for
                Instances.Update. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance resource to
                update.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_resource (google.cloud.compute_v1.types.Instance):
                The body resource for this request
                This corresponds to the ``instance_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, instance_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateInstanceRequest):
            request = compute.UpdateInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if instance_resource is not None:
                request.instance_resource = instance_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def update_access_config_unary(
        self,
        request: Union[compute.UpdateAccessConfigInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        network_interface: str = None,
        access_config_resource: compute.AccessConfig = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Updates the specified access config from an
        instance's network interface with the data included in
        the request. This method supports PATCH semantics and
        uses the JSON merge patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateAccessConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateAccessConfig. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface
                where the access config is attached.

                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_config_resource (google.cloud.compute_v1.types.AccessConfig):
                The body resource for this request
                This corresponds to the ``access_config_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, network_interface, access_config_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateAccessConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateAccessConfigInstanceRequest):
            request = compute.UpdateAccessConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if network_interface is not None:
                request.network_interface = network_interface
            if access_config_resource is not None:
                request.access_config_resource = access_config_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_access_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_access_config(
        self,
        request: Union[compute.UpdateAccessConfigInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        network_interface: str = None,
        access_config_resource: compute.AccessConfig = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Updates the specified access config from an
        instance's network interface with the data included in
        the request. This method supports PATCH semantics and
        uses the JSON merge patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateAccessConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateAccessConfig. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface
                where the access config is attached.

                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_config_resource (google.cloud.compute_v1.types.AccessConfig):
                The body resource for this request
                This corresponds to the ``access_config_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, network_interface, access_config_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateAccessConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateAccessConfigInstanceRequest):
            request = compute.UpdateAccessConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if network_interface is not None:
                request.network_interface = network_interface
            if access_config_resource is not None:
                request.access_config_resource = access_config_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_access_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def update_display_device_unary(
        self,
        request: Union[compute.UpdateDisplayDeviceInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        display_device_resource: compute.DisplayDevice = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Updates the Display config for a VM instance. You can
        only use this method on a stopped VM instance. This
        method supports PATCH semantics and uses the JSON merge
        patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateDisplayDeviceInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateDisplayDevice. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_device_resource (google.cloud.compute_v1.types.DisplayDevice):
                The body resource for this request
                This corresponds to the ``display_device_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, display_device_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateDisplayDeviceInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateDisplayDeviceInstanceRequest):
            request = compute.UpdateDisplayDeviceInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if display_device_resource is not None:
                request.display_device_resource = display_device_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_display_device]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_display_device(
        self,
        request: Union[compute.UpdateDisplayDeviceInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        display_device_resource: compute.DisplayDevice = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Updates the Display config for a VM instance. You can
        only use this method on a stopped VM instance. This
        method supports PATCH semantics and uses the JSON merge
        patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateDisplayDeviceInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateDisplayDevice. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name of the instance scoping this
                request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_device_resource (google.cloud.compute_v1.types.DisplayDevice):
                The body resource for this request
                This corresponds to the ``display_device_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance, display_device_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateDisplayDeviceInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateDisplayDeviceInstanceRequest):
            request = compute.UpdateDisplayDeviceInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if display_device_resource is not None:
                request.display_device_resource = display_device_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_display_device]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def update_network_interface_unary(
        self,
        request: Union[compute.UpdateNetworkInterfaceInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        network_interface: str = None,
        network_interface_resource: compute.NetworkInterface = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Updates an instance's network interface. This method
        can only update an interface's alias IP range and
        attached network. See Modifying alias IP ranges for an
        existing instance for instructions on changing alias IP
        ranges. See Migrating a VM between networks for
        instructions on migrating an interface. This method
        follows PATCH semantics.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateNetworkInterfaceInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateNetworkInterface. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface to
                update.

                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface_resource (google.cloud.compute_v1.types.NetworkInterface):
                The body resource for this request
                This corresponds to the ``network_interface_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, network_interface, network_interface_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateNetworkInterfaceInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateNetworkInterfaceInstanceRequest):
            request = compute.UpdateNetworkInterfaceInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if network_interface is not None:
                request.network_interface = network_interface
            if network_interface_resource is not None:
                request.network_interface_resource = network_interface_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_network_interface]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_network_interface(
        self,
        request: Union[compute.UpdateNetworkInterfaceInstanceRequest, dict] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        network_interface: str = None,
        network_interface_resource: compute.NetworkInterface = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Updates an instance's network interface. This method
        can only update an interface's alias IP range and
        attached network. See Modifying alias IP ranges for an
        existing instance for instructions on changing alias IP
        ranges. See Migrating a VM between networks for
        instructions on migrating an interface. This method
        follows PATCH semantics.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateNetworkInterfaceInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateNetworkInterface. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                The instance name for this request.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface (str):
                The name of the network interface to
                update.

                This corresponds to the ``network_interface`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_interface_resource (google.cloud.compute_v1.types.NetworkInterface):
                The body resource for this request
                This corresponds to the ``network_interface_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, network_interface, network_interface_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateNetworkInterfaceInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateNetworkInterfaceInstanceRequest):
            request = compute.UpdateNetworkInterfaceInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if network_interface is not None:
                request.network_interface = network_interface
            if network_interface_resource is not None:
                request.network_interface_resource = network_interface_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_network_interface]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def update_shielded_instance_config_unary(
        self,
        request: Union[
            compute.UpdateShieldedInstanceConfigInstanceRequest, dict
        ] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        shielded_instance_config_resource: compute.ShieldedInstanceConfig = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Updates the Shielded Instance config for an instance.
        You can only use this method on a stopped instance. This
        method supports PATCH semantics and uses the JSON merge
        patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateShieldedInstanceConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateShieldedInstanceConfig. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name or id of the instance scoping
                this request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            shielded_instance_config_resource (google.cloud.compute_v1.types.ShieldedInstanceConfig):
                The body resource for this request
                This corresponds to the ``shielded_instance_config_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, shielded_instance_config_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateShieldedInstanceConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateShieldedInstanceConfigInstanceRequest):
            request = compute.UpdateShieldedInstanceConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if shielded_instance_config_resource is not None:
                request.shielded_instance_config_resource = (
                    shielded_instance_config_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_shielded_instance_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_shielded_instance_config(
        self,
        request: Union[
            compute.UpdateShieldedInstanceConfigInstanceRequest, dict
        ] = None,
        *,
        project: str = None,
        zone: str = None,
        instance: str = None,
        shielded_instance_config_resource: compute.ShieldedInstanceConfig = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Updates the Shielded Instance config for an instance.
        You can only use this method on a stopped instance. This
        method supports PATCH semantics and uses the JSON merge
        patch format and processing rules.

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateShieldedInstanceConfigInstanceRequest, dict]):
                The request object. A request message for
                Instances.UpdateShieldedInstanceConfig. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (str):
                Name or id of the instance scoping
                this request.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            shielded_instance_config_resource (google.cloud.compute_v1.types.ShieldedInstanceConfig):
                The body resource for this request
                This corresponds to the ``shielded_instance_config_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, instance, shielded_instance_config_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.UpdateShieldedInstanceConfigInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.UpdateShieldedInstanceConfigInstanceRequest):
            request = compute.UpdateShieldedInstanceConfigInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance is not None:
                request.instance = instance
            if shielded_instance_config_resource is not None:
                request.shielded_instance_config_resource = (
                    shielded_instance_config_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_shielded_instance_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("instance", request.instance),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

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
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-compute",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("InstancesClient",)
