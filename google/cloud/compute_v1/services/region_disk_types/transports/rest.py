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
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.auth.transport.requests import AuthorizedSession

from google.cloud.compute_v1.types import compute

from .base import RegionDiskTypesTransport, DEFAULT_CLIENT_INFO


class RegionDiskTypesRestTransport(RegionDiskTypesTransport):
    """REST backend transport for RegionDiskTypes.

    The RegionDiskTypes API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
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
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host, credentials=credentials, client_info=client_info,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._prep_wrapped_messages(client_info)

    def get(
        self,
        request: compute.GetRegionDiskTypeRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.DiskType:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetRegionDiskTypeRequest):
                The request object. A request message for
                RegionDiskTypes.Get. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.DiskType:
                Represents a Disk Type resource.

                Google Compute Engine has two Disk Type resources:

                -  `Regional </compute/docs/reference/rest/{$api_version}/regionDiskTypes>`__
                   \*
                   `Zonal </compute/docs/reference/rest/{$api_version}/diskTypes>`__

                You can choose from a variety of disk types based on
                your needs. For more information, read Storage options.

                The diskTypes resource represents disk types for a zonal
                persistent disk. For more information, read Zonal
                persistent disks.

                The regionDiskTypes resource represents disk types for a
                regional persistent disk. For more information, read
                Regional persistent disks. (== resource_for
                {$api_version}.diskTypes ==) (== resource_for
                {$api_version}.regionDiskTypes ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/diskTypes/{disk_type}".format(
            host=self._host,
            project=request.project,
            region=request.region,
            disk_type=request.disk_type,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}

        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = ["{k}={v}".format(k=k, v=v) for k, v in query_params.items()]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.get(url, headers=headers,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.DiskType.from_json(response.content, ignore_unknown_fields=True)

    def list(
        self,
        request: compute.ListRegionDiskTypesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.RegionDiskTypeList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListRegionDiskTypesRequest):
                The request object. A request message for
                RegionDiskTypes.List. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.RegionDiskTypeList:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/diskTypes".format(
            host=self._host, project=request.project, region=request.region,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListRegionDiskTypesRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListRegionDiskTypesRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListRegionDiskTypesRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListRegionDiskTypesRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.ListRegionDiskTypesRequest.return_partial_success in request:
            query_params["returnPartialSuccess"] = request.return_partial_success

        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = ["{k}={v}".format(k=k, v=v) for k, v in query_params.items()]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.get(url, headers=headers,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.RegionDiskTypeList.from_json(
            response.content, ignore_unknown_fields=True
        )


__all__ = ("RegionDiskTypesRestTransport",)
