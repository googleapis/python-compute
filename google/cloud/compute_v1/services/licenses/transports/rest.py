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

from .base import LicensesTransport, DEFAULT_CLIENT_INFO


class LicensesRestTransport(LicensesTransport):
    """REST backend transport for Licenses.

    The Licenses API.

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

    def delete(
        self,
        request: compute.DeleteLicenseRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteLicenseRequest):
                The request object. A request message for
                Licenses.Delete. See the method
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
        url = "https://{host}/compute/v1/projects/{project}/global/licenses/{license}".format(
            host=self._host, project=request.project, license=request.license_,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if request.license_:
            query_params["license"] = request.license_
        if compute.DeleteLicenseRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = ["{k}={v}".format(k=k, v=v) for k, v in query_params.items()]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.delete(url, headers=headers,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def get(
        self,
        request: compute.GetLicenseRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.License:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetLicenseRequest):
                The request object. A request message for Licenses.Get.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.License:
                Represents a License resource.

                A License represents billing and aggregate usage data
                for public and marketplace images. Caution This resource
                is intended for use only by third-party partners who are
                creating Cloud Marketplace images. (== resource_for
                {$api_version}.licenses ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/licenses/{license}".format(
            host=self._host, project=request.project, license=request.license_,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if request.license_:
            query_params["license"] = request.license_

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
        return compute.License.from_json(response.content, ignore_unknown_fields=True)

    def get_iam_policy(
        self,
        request: compute.GetIamPolicyLicenseRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Call the get iam policy method over HTTP.

        Args:
            request (~.compute.GetIamPolicyLicenseRequest):
                The request object. A request message for
                Licenses.GetIamPolicy. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions; each ``role``
                can be an IAM predefined role or a user-created custom
                role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                { "bindings": [ { "role":
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
                "BwWWja0YfJA=", "version": 3 }

                **YAML example:**

                bindings: - members: - user:mike@example.com -
                group:admins@example.com - domain:google.com -
                serviceAccount:my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') - etag:
                BwWWja0YfJA= - version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/licenses/{resource}/getIamPolicy".format(
            host=self._host, project=request.project, resource=request.resource,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.GetIamPolicyLicenseRequest.options_requested_policy_version
            in request
        ):
            query_params[
                "optionsRequestedPolicyVersion"
            ] = request.options_requested_policy_version

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
        return compute.Policy.from_json(response.content, ignore_unknown_fields=True)

    def insert(
        self,
        request: compute.InsertLicenseRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertLicenseRequest):
                The request object. A request message for
                Licenses.Insert. See the method
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
        body = compute.License.to_json(
            request.license_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/licenses".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.InsertLicenseRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = ["{k}={v}".format(k=k, v=v) for k, v in query_params.items()]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.post(url, headers=headers, data=body,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def list(
        self,
        request: compute.ListLicensesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.LicensesListResponse:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListLicensesRequest):
                The request object. A request message for Licenses.List.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.LicensesListResponse:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/licenses".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListLicensesRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListLicensesRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListLicensesRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListLicensesRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.ListLicensesRequest.return_partial_success in request:
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
        return compute.LicensesListResponse.from_json(
            response.content, ignore_unknown_fields=True
        )

    def set_iam_policy(
        self,
        request: compute.SetIamPolicyLicenseRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Call the set iam policy method over HTTP.

        Args:
            request (~.compute.SetIamPolicyLicenseRequest):
                The request object. A request message for
                Licenses.SetIamPolicy. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions; each ``role``
                can be an IAM predefined role or a user-created custom
                role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                { "bindings": [ { "role":
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
                "BwWWja0YfJA=", "version": 3 }

                **YAML example:**

                bindings: - members: - user:mike@example.com -
                group:admins@example.com - domain:google.com -
                serviceAccount:my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') - etag:
                BwWWja0YfJA= - version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

        """

        # Jsonify the request body
        body = compute.GlobalSetPolicyRequest.to_json(
            request.global_set_policy_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/licenses/{resource}/setIamPolicy".format(
            host=self._host, project=request.project, resource=request.resource,
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
        response = self._session.post(url, headers=headers, data=body,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Policy.from_json(response.content, ignore_unknown_fields=True)

    def test_iam_permissions(
        self,
        request: compute.TestIamPermissionsLicenseRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.TestPermissionsResponse:
        r"""Call the test iam permissions method over HTTP.

        Args:
            request (~.compute.TestIamPermissionsLicenseRequest):
                The request object. A request message for
                Licenses.TestIamPermissions. See the
                method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.TestPermissionsResponse:

        """

        # Jsonify the request body
        body = compute.TestPermissionsRequest.to_json(
            request.test_permissions_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/licenses/{resource}/testIamPermissions".format(
            host=self._host, project=request.project, resource=request.resource,
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
        response = self._session.post(url, headers=headers, data=body,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.TestPermissionsResponse.from_json(
            response.content, ignore_unknown_fields=True
        )


__all__ = ("LicensesRestTransport",)
