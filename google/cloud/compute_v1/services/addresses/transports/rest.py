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

import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple


from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.auth.transport.requests import AuthorizedSession


from google.cloud.compute_v1.types import compute


from .base import AddressesTransport, DEFAULT_CLIENT_INFO


class AddressesRestTransport(AddressesTransport):
    """REST backend transport for Addresses.

    The Addresses API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
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
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        super().__init__(
            host=host, credentials=credentials, client_info=client_info,
        )
        self._session = AuthorizedSession(self._credentials)

    def aggregated_list(
        self,
        request: compute.AggregatedListAddressesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.AddressAggregatedList:
        r"""Call the aggregated list method over HTTP.

        Args:
            request (~.compute.AggregatedListAddressesRequest):
                The request object.
                A request message for
                Addresses.AggregatedList. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.AddressAggregatedList:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/aggregated/addresses".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "returnPartialSuccess": request.return_partial_success,
            "filter": request.filter,
            "includeAllScopes": request.include_all_scopes,
            "maxResults": request.max_results,
            "orderBy": request.order_by,
            "pageToken": request.page_token,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url)

        # Return the response
        return compute.AddressAggregatedList.from_json(response.content)

    def delete(
        self,
        request: compute.DeleteAddressRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteAddressRequest):
                The request object.
                A request message for
                Addresses.Delete. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource.

                Google Compute Engine has three Operation resources:

                -  `Global </compute/docs/reference/rest/{$api_version}/globalOperations>`__
                   \*
                   `Regional </compute/docs/reference/rest/{$api_version}/regionOperations>`__
                   \*
                   `Zonal </compute/docs/reference/rest/{$api_version}/zoneOperations>`__

                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses.

                Operations can be global, regional or zonal.

                -  For global operations, use the ``globalOperations``
                   resource.
                -  For regional operations, use the ``regionOperations``
                   resource.
                -  For zonal operations, use the ``zonalOperations``
                   resource.

                For more information, read Global, Regional, and Zonal
                Resources. (== resource_for
                {$api_version}.globalOperations ==) (== resource_for
                {$api_version}.regionOperations ==) (== resource_for
                {$api_version}.zoneOperations ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/addresses/{address}".format(
            host=self._host,
            project=request.project,
            region=request.region,
            address=request.address,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.delete(url)

        # Return the response
        return compute.Operation.from_json(response.content)

    def get(
        self,
        request: compute.GetAddressRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Address:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetAddressRequest):
                The request object.
                A request message for Addresses.Get.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Address:
                Use global external addresses for GFE-based external
                HTTP(S) load balancers in Premium Tier.

                Use global internal addresses for reserved peering
                network range.

                Use regional external addresses for the following
                resources:

                -  External IP addresses for VM instances - Regional
                   external forwarding rules - Cloud NAT external IP
                   addresses - GFE based LBs in Standard Tier - Network
                   LBs in Premium or Standard Tier - Cloud VPN gateways
                   (both Classic and HA)

                Use regional internal IP addresses for subnet IP ranges
                (primary and secondary). This includes:

                -  Internal IP addresses for VM instances - Alias IP
                   ranges of VM instances (/32 only) - Regional internal
                   forwarding rules - Internal TCP/UDP load balancer
                   addresses - Internal HTTP(S) load balancer addresses
                   - Cloud DNS inbound forwarding IP addresses

                For more information, read reserved IP address.

                (== resource_for {$api_version}.addresses ==) (==
                resource_for {$api_version}.globalAddresses ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/addresses/{address}".format(
            host=self._host,
            project=request.project,
            region=request.region,
            address=request.address,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url)

        # Return the response
        return compute.Address.from_json(response.content)

    def insert(
        self,
        request: compute.InsertAddressRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertAddressRequest):
                The request object.
                A request message for
                Addresses.Insert. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource.

                Google Compute Engine has three Operation resources:

                -  `Global </compute/docs/reference/rest/{$api_version}/globalOperations>`__
                   \*
                   `Regional </compute/docs/reference/rest/{$api_version}/regionOperations>`__
                   \*
                   `Zonal </compute/docs/reference/rest/{$api_version}/zoneOperations>`__

                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses.

                Operations can be global, regional or zonal.

                -  For global operations, use the ``globalOperations``
                   resource.
                -  For regional operations, use the ``regionOperations``
                   resource.
                -  For zonal operations, use the ``zonalOperations``
                   resource.

                For more information, read Global, Regional, and Zonal
                Resources. (== resource_for
                {$api_version}.globalOperations ==) (== resource_for
                {$api_version}.regionOperations ==) (== resource_for
                {$api_version}.zoneOperations ==)

        """

        # Jsonify the request body
        body = compute.Address.to_json(
            request.address_resource, including_default_value_fields=False
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/addresses".format(
            host=self._host, project=request.project, region=request.region,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.post(url, json=body,)

        # Return the response
        return compute.Operation.from_json(response.content)

    def list(
        self,
        request: compute.ListAddressesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.AddressList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListAddressesRequest):
                The request object.
                A request message for Addresses.List.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.AddressList:
                Contains a list of addresses.
        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/addresses".format(
            host=self._host, project=request.project, region=request.region,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "returnPartialSuccess": request.return_partial_success,
            "filter": request.filter,
            "maxResults": request.max_results,
            "orderBy": request.order_by,
            "pageToken": request.page_token,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url)

        # Return the response
        return compute.AddressList.from_json(response.content)


__all__ = ("AddressesRestTransport",)
