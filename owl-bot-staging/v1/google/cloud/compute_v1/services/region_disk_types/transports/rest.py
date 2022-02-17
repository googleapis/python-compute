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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from requests import __version__ as requests_version
import dataclasses
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.compute_v1.types import compute

from .base import RegionDiskTypesTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RegionDiskTypesRestInterceptor:
    """Interceptor for RegionDiskTypes.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionDiskTypesRestTransport.

    .. code-block:
        class MyCustomRegionDiskTypesInterceptor(RegionDiskTypesRestInterceptor):
            def pre_get(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(response):
                logging.log(f"Received response: {response}")

            def pre_list(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(response):
                logging.log(f"Received response: {response}")

        transport = RegionDiskTypesRestTransport(interceptor=MyCustomRegionDiskTypesInterceptor())
        client = RegionDiskTypesClient(transport=transport)


    """
    def pre_get(self, request: compute.GetRegionDiskTypeRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.GetRegionDiskTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDiskTypes server.
        """
        return request, metadata

    def post_get(self, response: compute.DiskType) -> compute.DiskType:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionDiskTypes server but before
        it is returned to user code.
        """
        return response

    def pre_list(self, request: compute.ListRegionDiskTypesRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.ListRegionDiskTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDiskTypes server.
        """
        return request, metadata

    def post_list(self, response: compute.RegionDiskTypeList) -> compute.RegionDiskTypeList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionDiskTypes server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionDiskTypesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionDiskTypesRestInterceptor


class RegionDiskTypesRestTransport(RegionDiskTypesTransport):
    """REST backend transport for RegionDiskTypes.

    The RegionDiskTypes API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """
    _STUBS: Dict[str, RegionDiskTypesRestStub] = {}

    def __init__(self, *,
            host: str = 'compute.googleapis.com',
            credentials: ga_credentials.Credentials=None,
            credentials_file: str=None,
            scopes: Sequence[str]=None,
            client_cert_source_for_mtls: Callable[[
                ], Tuple[bytes, bytes]]=None,
            quota_project_id: Optional[str]=None,
            client_info: gapic_v1.client_info.ClientInfo=DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool]=False,
            url_scheme: str='https',
            interceptor: Optional[RegionDiskTypesRestInterceptor] = None,
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
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(f"Unexpected hostname structure: {host}")  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or RegionDiskTypesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _Get(RegionDiskTypesRestStub):
        def __hash__(self):
            return hash("Get")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.GetRegionDiskTypeRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.DiskType:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionDiskTypeRequest):
                    The request object. A request message for
                RegionDiskTypes.Get. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.DiskType:
                    Represents a Disk Type resource. Google Compute Engine
                has two Disk Type resources: \*
                `Regional </compute/docs/reference/rest/v1/regionDiskTypes>`__
                \* `Zonal </compute/docs/reference/rest/v1/diskTypes>`__
                You can choose from a variety of disk types based on
                your needs. For more information, read Storage options.
                The diskTypes resource represents disk types for a zonal
                persistent disk. For more information, read Zonal
                persistent disks. The regionDiskTypes resource
                represents disk types for a regional persistent disk.
                For more information, read Regional persistent disks.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/regions/{region}/diskTypes/{disk_type}',
            },
            ]
            request, metadata = self._interceptor.pre_get(request, metadata)
            request_kwargs = compute.GetRegionDiskTypeRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.GetRegionDiskTypeRequest.to_json(
                compute.GetRegionDiskTypeRequest(transcoded_request['query_params']),
                including_default_value_fields=False,
                use_integers_for_enums=False
            ))

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.DiskType.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_get(resp)
            return resp

    class _List(RegionDiskTypesRestStub):
        def __hash__(self):
            return hash("List")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.ListRegionDiskTypesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.RegionDiskTypeList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionDiskTypesRequest):
                    The request object. A request message for
                RegionDiskTypes.List. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionDiskTypeList:

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/regions/{region}/diskTypes',
            },
            ]
            request, metadata = self._interceptor.pre_list(request, metadata)
            request_kwargs = compute.ListRegionDiskTypesRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.ListRegionDiskTypesRequest.to_json(
                compute.ListRegionDiskTypesRequest(transcoded_request['query_params']),
                including_default_value_fields=False,
                use_integers_for_enums=False
            ))

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.RegionDiskTypeList.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list(resp)
            return resp

    @property
    def get(self) -> Callable[
            [compute.GetRegionDiskTypeRequest],
            compute.DiskType]:
        stub = self._STUBS.get("get")
        if not stub:
            stub = self._STUBS["get"] = self._Get(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def list(self) -> Callable[
            [compute.ListRegionDiskTypesRequest],
            compute.RegionDiskTypeList]:
        stub = self._STUBS.get("list")
        if not stub:
            stub = self._STUBS["list"] = self._List(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    def close(self):
        self._session.close()


__all__=(
    'RegionDiskTypesRestTransport',
)