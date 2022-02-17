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

from .base import RegionTargetHttpProxiesTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RegionTargetHttpProxiesRestInterceptor:
    """Interceptor for RegionTargetHttpProxies.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionTargetHttpProxiesRestTransport.

    .. code-block:
        class MyCustomRegionTargetHttpProxiesInterceptor(RegionTargetHttpProxiesRestInterceptor):
            def pre_delete(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(response):
                logging.log(f"Received response: {response}")

            def pre_get(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(response):
                logging.log(f"Received response: {response}")

            def pre_insert(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert(response):
                logging.log(f"Received response: {response}")

            def pre_list(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(response):
                logging.log(f"Received response: {response}")

            def pre_set_url_map(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_url_map(response):
                logging.log(f"Received response: {response}")

        transport = RegionTargetHttpProxiesRestTransport(interceptor=MyCustomRegionTargetHttpProxiesInterceptor())
        client = RegionTargetHttpProxiesClient(transport=transport)


    """
    def pre_delete(self, request: compute.DeleteRegionTargetHttpProxyRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.DeleteRegionTargetHttpProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionTargetHttpProxies server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the RegionTargetHttpProxies server but before
        it is returned to user code.
        """
        return response

    def pre_get(self, request: compute.GetRegionTargetHttpProxyRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.GetRegionTargetHttpProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionTargetHttpProxies server.
        """
        return request, metadata

    def post_get(self, response: compute.TargetHttpProxy) -> compute.TargetHttpProxy:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionTargetHttpProxies server but before
        it is returned to user code.
        """
        return response

    def pre_insert(self, request: compute.InsertRegionTargetHttpProxyRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.InsertRegionTargetHttpProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionTargetHttpProxies server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the RegionTargetHttpProxies server but before
        it is returned to user code.
        """
        return response

    def pre_list(self, request: compute.ListRegionTargetHttpProxiesRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.ListRegionTargetHttpProxiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionTargetHttpProxies server.
        """
        return request, metadata

    def post_list(self, response: compute.TargetHttpProxyList) -> compute.TargetHttpProxyList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionTargetHttpProxies server but before
        it is returned to user code.
        """
        return response

    def pre_set_url_map(self, request: compute.SetUrlMapRegionTargetHttpProxyRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.SetUrlMapRegionTargetHttpProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_url_map

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionTargetHttpProxies server.
        """
        return request, metadata

    def post_set_url_map(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_url_map

        Override in a subclass to manipulate the response
        after it is returned by the RegionTargetHttpProxies server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionTargetHttpProxiesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionTargetHttpProxiesRestInterceptor


class RegionTargetHttpProxiesRestTransport(RegionTargetHttpProxiesTransport):
    """REST backend transport for RegionTargetHttpProxies.

    The RegionTargetHttpProxies API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """
    _STUBS: Dict[str, RegionTargetHttpProxiesRestStub] = {}

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
            interceptor: Optional[RegionTargetHttpProxiesRestInterceptor] = None,
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
        self._interceptor = interceptor or RegionTargetHttpProxiesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _Delete(RegionTargetHttpProxiesRestStub):
        def __hash__(self):
            return hash("Delete")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.DeleteRegionTargetHttpProxyRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteRegionTargetHttpProxyRequest):
                    The request object. A request message for
                RegionTargetHttpProxies.Delete. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/compute/v1/projects/{project}/regions/{region}/targetHttpProxies/{target_http_proxy}',
            },
            ]
            request, metadata = self._interceptor.pre_delete(request, metadata)
            request_kwargs = compute.DeleteRegionTargetHttpProxyRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.DeleteRegionTargetHttpProxyRequest.to_json(
                compute.DeleteRegionTargetHttpProxyRequest(transcoded_request['query_params']),
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
            resp = compute.Operation.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_delete(resp)
            return resp

    class _Get(RegionTargetHttpProxiesRestStub):
        def __hash__(self):
            return hash("Get")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.GetRegionTargetHttpProxyRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.TargetHttpProxy:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionTargetHttpProxyRequest):
                    The request object. A request message for
                RegionTargetHttpProxies.Get. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetHttpProxy:
                    Represents a Target HTTP Proxy resource. Google Compute
                Engine has two Target HTTP Proxy resources: \*
                `Global </compute/docs/reference/rest/v1/targetHttpProxies>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionTargetHttpProxies>`__
                A target HTTP proxy is a component of GCP HTTP load
                balancers. \* targetHttpProxies are used by external
                HTTP load balancers and Traffic Director. \*
                regionTargetHttpProxies are used by internal HTTP load
                balancers. Forwarding rules reference a target HTTP
                proxy, and the target proxy then references a URL map.
                For more information, read Using Target Proxies and
                Forwarding rule concepts.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/regions/{region}/targetHttpProxies/{target_http_proxy}',
            },
            ]
            request, metadata = self._interceptor.pre_get(request, metadata)
            request_kwargs = compute.GetRegionTargetHttpProxyRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.GetRegionTargetHttpProxyRequest.to_json(
                compute.GetRegionTargetHttpProxyRequest(transcoded_request['query_params']),
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
            resp = compute.TargetHttpProxy.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(RegionTargetHttpProxiesRestStub):
        def __hash__(self):
            return hash("Insert")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.InsertRegionTargetHttpProxyRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertRegionTargetHttpProxyRequest):
                    The request object. A request message for
                RegionTargetHttpProxies.Insert. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/compute/v1/projects/{project}/regions/{region}/targetHttpProxies',
                'body': 'target_http_proxy_resource',
            },
            ]
            request, metadata = self._interceptor.pre_insert(request, metadata)
            request_kwargs = compute.InsertRegionTargetHttpProxyRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.TargetHttpProxy.to_json(
                compute.TargetHttpProxy(transcoded_request['body']),                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.InsertRegionTargetHttpProxyRequest.to_json(
                compute.InsertRegionTargetHttpProxyRequest(transcoded_request['query_params']),
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
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_insert(resp)
            return resp

    class _List(RegionTargetHttpProxiesRestStub):
        def __hash__(self):
            return hash("List")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.ListRegionTargetHttpProxiesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.TargetHttpProxyList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionTargetHttpProxiesRequest):
                    The request object. A request message for
                RegionTargetHttpProxies.List. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetHttpProxyList:
                    A list of TargetHttpProxy resources.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/regions/{region}/targetHttpProxies',
            },
            ]
            request, metadata = self._interceptor.pre_list(request, metadata)
            request_kwargs = compute.ListRegionTargetHttpProxiesRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.ListRegionTargetHttpProxiesRequest.to_json(
                compute.ListRegionTargetHttpProxiesRequest(transcoded_request['query_params']),
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
            resp = compute.TargetHttpProxyList.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list(resp)
            return resp

    class _SetUrlMap(RegionTargetHttpProxiesRestStub):
        def __hash__(self):
            return hash("SetUrlMap")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.SetUrlMapRegionTargetHttpProxyRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.Operation:
            r"""Call the set url map method over HTTP.

            Args:
                request (~.compute.SetUrlMapRegionTargetHttpProxyRequest):
                    The request object. A request message for
                RegionTargetHttpProxies.SetUrlMap. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/compute/v1/projects/{project}/regions/{region}/targetHttpProxies/{target_http_proxy}/setUrlMap',
                'body': 'url_map_reference_resource',
            },
            ]
            request, metadata = self._interceptor.pre_set_url_map(request, metadata)
            request_kwargs = compute.SetUrlMapRegionTargetHttpProxyRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.UrlMapReference.to_json(
                compute.UrlMapReference(transcoded_request['body']),                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.SetUrlMapRegionTargetHttpProxyRequest.to_json(
                compute.SetUrlMapRegionTargetHttpProxyRequest(transcoded_request['query_params']),
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
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_set_url_map(resp)
            return resp

    @property
    def delete(self) -> Callable[
            [compute.DeleteRegionTargetHttpProxyRequest],
            compute.Operation]:
        stub = self._STUBS.get("delete")
        if not stub:
            stub = self._STUBS["delete"] = self._Delete(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def get(self) -> Callable[
            [compute.GetRegionTargetHttpProxyRequest],
            compute.TargetHttpProxy]:
        stub = self._STUBS.get("get")
        if not stub:
            stub = self._STUBS["get"] = self._Get(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def insert(self) -> Callable[
            [compute.InsertRegionTargetHttpProxyRequest],
            compute.Operation]:
        stub = self._STUBS.get("insert")
        if not stub:
            stub = self._STUBS["insert"] = self._Insert(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def list(self) -> Callable[
            [compute.ListRegionTargetHttpProxiesRequest],
            compute.TargetHttpProxyList]:
        stub = self._STUBS.get("list")
        if not stub:
            stub = self._STUBS["list"] = self._List(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def set_url_map(self) -> Callable[
            [compute.SetUrlMapRegionTargetHttpProxyRequest],
            compute.Operation]:
        stub = self._STUBS.get("set_url_map")
        if not stub:
            stub = self._STUBS["set_url_map"] = self._SetUrlMap(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    def close(self):
        self._session.close()


__all__=(
    'RegionTargetHttpProxiesRestTransport',
)