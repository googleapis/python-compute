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

import dataclasses
import json  # type: ignore
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.compute_v1.types import compute

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import RegionCommitmentsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RegionCommitmentsRestInterceptor:
    """Interceptor for RegionCommitments.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionCommitmentsRestTransport.

    .. code-block:: python
        class MyCustomRegionCommitmentsInterceptor(RegionCommitmentsRestInterceptor):
            def pre_aggregated_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RegionCommitmentsRestTransport(interceptor=MyCustomRegionCommitmentsInterceptor())
        client = RegionCommitmentsClient(transport=transport)


    """

    def pre_aggregated_list(
        self,
        request: compute.AggregatedListRegionCommitmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AggregatedListRegionCommitmentsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionCommitments server.
        """
        return request, metadata

    def post_aggregated_list(
        self, response: compute.CommitmentAggregatedList
    ) -> compute.CommitmentAggregatedList:
        """Post-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the response
        after it is returned by the RegionCommitments server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetRegionCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetRegionCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionCommitments server.
        """
        return request, metadata

    def post_get(self, response: compute.Commitment) -> compute.Commitment:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionCommitments server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertRegionCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.InsertRegionCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionCommitments server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the RegionCommitments server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListRegionCommitmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListRegionCommitmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionCommitments server.
        """
        return request, metadata

    def post_list(self, response: compute.CommitmentList) -> compute.CommitmentList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionCommitments server but before
        it is returned to user code.
        """
        return response

    def pre_update(
        self,
        request: compute.UpdateRegionCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.UpdateRegionCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionCommitments server.
        """
        return request, metadata

    def post_update(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for update

        Override in a subclass to manipulate the response
        after it is returned by the RegionCommitments server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionCommitmentsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionCommitmentsRestInterceptor


class RegionCommitmentsRestTransport(RegionCommitmentsTransport):
    """REST backend transport for RegionCommitments.

    The RegionCommitments API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RegionCommitmentsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

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
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or RegionCommitmentsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AggregatedList(RegionCommitmentsRestStub):
        def __hash__(self):
            return hash("AggregatedList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.AggregatedListRegionCommitmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.CommitmentAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListRegionCommitmentsRequest):
                    The request object. A request message for
                RegionCommitments.AggregatedList. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.CommitmentAggregatedList:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/aggregated/commitments",
                },
            ]
            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            pb_request = compute.AggregatedListRegionCommitmentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.CommitmentAggregatedList()
            pb_resp = compute.CommitmentAggregatedList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregated_list(resp)
            return resp

    class _Get(RegionCommitmentsRestStub):
        def __hash__(self):
            return hash("Get")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetRegionCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Commitment:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionCommitmentRequest):
                    The request object. A request message for
                RegionCommitments.Get. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Commitment:
                    Represents a regional Commitment
                resource. Creating a commitment resource
                means that you are purchasing a
                committed use contract with an explicit
                start and end time. You can create
                commitments based on vCPUs and memory
                usage and receive discounted rates. For
                full details, read Signing Up for
                Committed Use Discounts.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/commitments/{commitment}",
                },
            ]
            request, metadata = self._interceptor.pre_get(request, metadata)
            pb_request = compute.GetRegionCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Commitment()
            pb_resp = compute.Commitment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(RegionCommitmentsRestStub):
        def __hash__(self):
            return hash("Insert")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.InsertRegionCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertRegionCommitmentRequest):
                    The request object. A request message for
                RegionCommitments.Insert. See the method
                description for details.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/commitments",
                    "body": "commitment_resource",
                },
            ]
            request, metadata = self._interceptor.pre_insert(request, metadata)
            pb_request = compute.InsertRegionCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_insert(resp)
            return resp

    class _List(RegionCommitmentsRestStub):
        def __hash__(self):
            return hash("List")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ListRegionCommitmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.CommitmentList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionCommitmentsRequest):
                    The request object. A request message for
                RegionCommitments.List. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.CommitmentList:
                    Contains a list of Commitment
                resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/commitments",
                },
            ]
            request, metadata = self._interceptor.pre_list(request, metadata)
            pb_request = compute.ListRegionCommitmentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.CommitmentList()
            pb_resp = compute.CommitmentList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _Update(RegionCommitmentsRestStub):
        def __hash__(self):
            return hash("Update")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.UpdateRegionCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update method over HTTP.

            Args:
                request (~.compute.UpdateRegionCommitmentRequest):
                    The request object. A request message for
                RegionCommitments.Update. See the method
                description for details.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/commitments/{commitment}",
                    "body": "commitment_resource",
                },
            ]
            request, metadata = self._interceptor.pre_update(request, metadata)
            pb_request = compute.UpdateRegionCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update(resp)
            return resp

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListRegionCommitmentsRequest],
        compute.CommitmentAggregatedList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(self) -> Callable[[compute.GetRegionCommitmentRequest], compute.Commitment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertRegionCommitmentRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[[compute.ListRegionCommitmentsRequest], compute.CommitmentList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update(
        self,
    ) -> Callable[[compute.UpdateRegionCommitmentRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Update(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegionCommitmentsRestTransport",)
