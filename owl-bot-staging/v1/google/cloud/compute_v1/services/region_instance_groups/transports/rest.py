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

from .base import RegionInstanceGroupsTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RegionInstanceGroupsRestInterceptor:
    """Interceptor for RegionInstanceGroups.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionInstanceGroupsRestTransport.

    .. code-block:
        class MyCustomRegionInstanceGroupsInterceptor(RegionInstanceGroupsRestInterceptor):
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

            def pre_list_instances(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_instances(response):
                logging.log(f"Received response: {response}")

            def pre_set_named_ports(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_named_ports(response):
                logging.log(f"Received response: {response}")

        transport = RegionInstanceGroupsRestTransport(interceptor=MyCustomRegionInstanceGroupsInterceptor())
        client = RegionInstanceGroupsClient(transport=transport)


    """
    def pre_get(self, request: compute.GetRegionInstanceGroupRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.GetRegionInstanceGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroups server.
        """
        return request, metadata

    def post_get(self, response: compute.InstanceGroup) -> compute.InstanceGroup:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroups server but before
        it is returned to user code.
        """
        return response

    def pre_list(self, request: compute.ListRegionInstanceGroupsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.ListRegionInstanceGroupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroups server.
        """
        return request, metadata

    def post_list(self, response: compute.RegionInstanceGroupList) -> compute.RegionInstanceGroupList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroups server but before
        it is returned to user code.
        """
        return response

    def pre_list_instances(self, request: compute.ListInstancesRegionInstanceGroupsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.ListInstancesRegionInstanceGroupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroups server.
        """
        return request, metadata

    def post_list_instances(self, response: compute.RegionInstanceGroupsListInstances) -> compute.RegionInstanceGroupsListInstances:
        """Post-rpc interceptor for list_instances

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroups server but before
        it is returned to user code.
        """
        return response

    def pre_set_named_ports(self, request: compute.SetNamedPortsRegionInstanceGroupRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[compute.SetNamedPortsRegionInstanceGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_named_ports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroups server.
        """
        return request, metadata

    def post_set_named_ports(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_named_ports

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroups server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionInstanceGroupsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionInstanceGroupsRestInterceptor


class RegionInstanceGroupsRestTransport(RegionInstanceGroupsTransport):
    """REST backend transport for RegionInstanceGroups.

    The RegionInstanceGroups API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """
    _STUBS: Dict[str, RegionInstanceGroupsRestStub] = {}

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
            interceptor: Optional[RegionInstanceGroupsRestInterceptor] = None,
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
        self._interceptor = interceptor or RegionInstanceGroupsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _Get(RegionInstanceGroupsRestStub):
        def __hash__(self):
            return hash("Get")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.GetRegionInstanceGroupRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.InstanceGroup:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionInstanceGroupRequest):
                    The request object. A request message for
                RegionInstanceGroups.Get. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceGroup:
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

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/regions/{region}/instanceGroups/{instance_group}',
            },
            ]
            request, metadata = self._interceptor.pre_get(request, metadata)
            request_kwargs = compute.GetRegionInstanceGroupRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.GetRegionInstanceGroupRequest.to_json(
                compute.GetRegionInstanceGroupRequest(transcoded_request['query_params']),
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
            resp = compute.InstanceGroup.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_get(resp)
            return resp

    class _List(RegionInstanceGroupsRestStub):
        def __hash__(self):
            return hash("List")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.ListRegionInstanceGroupsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.RegionInstanceGroupList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionInstanceGroupsRequest):
                    The request object. A request message for
                RegionInstanceGroups.List. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionInstanceGroupList:
                    Contains a list of InstanceGroup
                resources.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/regions/{region}/instanceGroups',
            },
            ]
            request, metadata = self._interceptor.pre_list(request, metadata)
            request_kwargs = compute.ListRegionInstanceGroupsRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.ListRegionInstanceGroupsRequest.to_json(
                compute.ListRegionInstanceGroupsRequest(transcoded_request['query_params']),
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
            resp = compute.RegionInstanceGroupList.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list(resp)
            return resp

    class _ListInstances(RegionInstanceGroupsRestStub):
        def __hash__(self):
            return hash("ListInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.ListInstancesRegionInstanceGroupsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.RegionInstanceGroupsListInstances:
            r"""Call the list instances method over HTTP.

            Args:
                request (~.compute.ListInstancesRegionInstanceGroupsRequest):
                    The request object. A request message for
                RegionInstanceGroups.ListInstances. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionInstanceGroupsListInstances:

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/compute/v1/projects/{project}/regions/{region}/instanceGroups/{instance_group}/listInstances',
                'body': 'region_instance_groups_list_instances_request_resource',
            },
            ]
            request, metadata = self._interceptor.pre_list_instances(request, metadata)
            request_kwargs = compute.ListInstancesRegionInstanceGroupsRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.RegionInstanceGroupsListInstancesRequest.to_json(
                compute.RegionInstanceGroupsListInstancesRequest(transcoded_request['body']),                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.ListInstancesRegionInstanceGroupsRequest.to_json(
                compute.ListInstancesRegionInstanceGroupsRequest(transcoded_request['query_params']),
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
            resp = compute.RegionInstanceGroupsListInstances.from_json(
                response.content,
                ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list_instances(resp)
            return resp

    class _SetNamedPorts(RegionInstanceGroupsRestStub):
        def __hash__(self):
            return hash("SetNamedPorts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.SetNamedPortsRegionInstanceGroupRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.Operation:
            r"""Call the set named ports method over HTTP.

            Args:
                request (~.compute.SetNamedPortsRegionInstanceGroupRequest):
                    The request object. A request message for
                RegionInstanceGroups.SetNamedPorts. See
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
                'uri': '/compute/v1/projects/{project}/regions/{region}/instanceGroups/{instance_group}/setNamedPorts',
                'body': 'region_instance_groups_set_named_ports_request_resource',
            },
            ]
            request, metadata = self._interceptor.pre_set_named_ports(request, metadata)
            request_kwargs = compute.SetNamedPortsRegionInstanceGroupRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.RegionInstanceGroupsSetNamedPortsRequest.to_json(
                compute.RegionInstanceGroupsSetNamedPortsRequest(transcoded_request['body']),                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.SetNamedPortsRegionInstanceGroupRequest.to_json(
                compute.SetNamedPortsRegionInstanceGroupRequest(transcoded_request['query_params']),
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
            resp = self._interceptor.post_set_named_ports(resp)
            return resp

    @property
    def get(self) -> Callable[
            [compute.GetRegionInstanceGroupRequest],
            compute.InstanceGroup]:
        stub = self._STUBS.get("get")
        if not stub:
            stub = self._STUBS["get"] = self._Get(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def list(self) -> Callable[
            [compute.ListRegionInstanceGroupsRequest],
            compute.RegionInstanceGroupList]:
        stub = self._STUBS.get("list")
        if not stub:
            stub = self._STUBS["list"] = self._List(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def list_instances(self) -> Callable[
            [compute.ListInstancesRegionInstanceGroupsRequest],
            compute.RegionInstanceGroupsListInstances]:
        stub = self._STUBS.get("list_instances")
        if not stub:
            stub = self._STUBS["list_instances"] = self._ListInstances(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    @property
    def set_named_ports(self) -> Callable[
            [compute.SetNamedPortsRegionInstanceGroupRequest],
            compute.Operation]:
        stub = self._STUBS.get("set_named_ports")
        if not stub:
            stub = self._STUBS["set_named_ports"] = self._SetNamedPorts(self._session, self._host, self._interceptor)

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub # type: ignore

    def close(self):
        self._session.close()


__all__=(
    'RegionInstanceGroupsRestTransport',
)