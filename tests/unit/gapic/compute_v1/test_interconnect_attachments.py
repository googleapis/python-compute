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

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from requests import Response
from requests.sessions import Session

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.compute_v1.services.interconnect_attachments import (
    InterconnectAttachmentsClient,
)
from google.cloud.compute_v1.services.interconnect_attachments import transports
from google.cloud.compute_v1.types import compute
from google.oauth2 import service_account


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert InterconnectAttachmentsClient._get_default_mtls_endpoint(None) is None
    assert (
        InterconnectAttachmentsClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        InterconnectAttachmentsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        InterconnectAttachmentsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        InterconnectAttachmentsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        InterconnectAttachmentsClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test_interconnect_attachments_client_from_service_account_info():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = InterconnectAttachmentsClient.from_service_account_info(info)
        assert client.transport._credentials == creds

        assert client.transport._host == "compute.googleapis.com:443"


@pytest.mark.parametrize("client_class", [InterconnectAttachmentsClient,])
def test_interconnect_attachments_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "compute.googleapis.com:443"


def test_interconnect_attachments_client_get_transport_class():
    transport = InterconnectAttachmentsClient.get_transport_class()
    available_transports = [
        transports.InterconnectAttachmentsRestTransport,
    ]
    assert transport in available_transports

    transport = InterconnectAttachmentsClient.get_transport_class("rest")
    assert transport == transports.InterconnectAttachmentsRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            InterconnectAttachmentsClient,
            transports.InterconnectAttachmentsRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    InterconnectAttachmentsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(InterconnectAttachmentsClient),
)
def test_interconnect_attachments_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(InterconnectAttachmentsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(InterconnectAttachmentsClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            InterconnectAttachmentsClient,
            transports.InterconnectAttachmentsRestTransport,
            "rest",
            "true",
        ),
        (
            InterconnectAttachmentsClient,
            transports.InterconnectAttachmentsRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    InterconnectAttachmentsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(InterconnectAttachmentsClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_interconnect_attachments_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            InterconnectAttachmentsClient,
            transports.InterconnectAttachmentsRestTransport,
            "rest",
        ),
    ],
)
def test_interconnect_attachments_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            InterconnectAttachmentsClient,
            transports.InterconnectAttachmentsRestTransport,
            "rest",
        ),
    ],
)
def test_interconnect_attachments_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_aggregated_list_rest(
    transport: str = "rest",
    request_type=compute.AggregatedListInterconnectAttachmentsRequest,
):
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InterconnectAttachmentAggregatedList(
            id="id_value",
            items={
                "key_value": compute.InterconnectAttachmentsScopedList(
                    interconnect_attachments=[
                        compute.InterconnectAttachment(admin_enabled=True)
                    ]
                )
            },
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            unreachables=["unreachables_value"],
            warning=compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED),
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InterconnectAttachmentAggregatedList.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.aggregated_list(request)

    assert response.raw_page is response

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InterconnectAttachmentAggregatedList)
    assert response.id == "id_value"
    assert response.items == {
        "key_value": compute.InterconnectAttachmentsScopedList(
            interconnect_attachments=[
                compute.InterconnectAttachment(admin_enabled=True)
            ]
        )
    }
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.unreachables == ["unreachables_value"]
    assert response.warning == compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED)


def test_aggregated_list_rest_from_dict():
    test_aggregated_list_rest(request_type=dict)


def test_aggregated_list_rest_flattened():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InterconnectAttachmentAggregatedList()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InterconnectAttachmentAggregatedList.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.aggregated_list(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)


def test_aggregated_list_rest_flattened_error():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListInterconnectAttachmentsRequest(),
            project="project_value",
        )


def test_delete_rest(
    transport: str = "rest", request_type=compute.DeleteInterconnectAttachmentRequest
):
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete(request)

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_delete_rest_from_dict():
    test_delete_rest(request_type=dict)


def test_delete_rest_flattened():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete(
            project="project_value",
            region="region_value",
            interconnect_attachment="interconnect_attachment_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "region_value" in http_call[1] + str(body)

        assert "interconnect_attachment_value" in http_call[1] + str(body)


def test_delete_rest_flattened_error():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete(
            compute.DeleteInterconnectAttachmentRequest(),
            project="project_value",
            region="region_value",
            interconnect_attachment="interconnect_attachment_value",
        )


def test_get_rest(
    transport: str = "rest", request_type=compute.GetInterconnectAttachmentRequest
):
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InterconnectAttachment(
            admin_enabled=True,
            bandwidth=compute.InterconnectAttachment.Bandwidth.BPS_100M,
            candidate_subnets=["candidate_subnets_value"],
            cloud_router_ip_address="cloud_router_ip_address_value",
            creation_timestamp="creation_timestamp_value",
            customer_router_ip_address="customer_router_ip_address_value",
            dataplane_version=1807,
            description="description_value",
            edge_availability_domain=compute.InterconnectAttachment.EdgeAvailabilityDomain.AVAILABILITY_DOMAIN_1,
            google_reference_id="google_reference_id_value",
            id="id_value",
            interconnect="interconnect_value",
            kind="kind_value",
            mtu=342,
            name="name_value",
            operational_status=compute.InterconnectAttachment.OperationalStatus.OS_ACTIVE,
            pairing_key="pairing_key_value",
            partner_asn="partner_asn_value",
            partner_metadata=compute.InterconnectAttachmentPartnerMetadata(
                interconnect_name="interconnect_name_value"
            ),
            private_interconnect_info=compute.InterconnectAttachmentPrivateInfo(
                tag8021q=632
            ),
            region="region_value",
            router="router_value",
            self_link="self_link_value",
            state=compute.InterconnectAttachment.State.ACTIVE,
            type_=compute.InterconnectAttachment.Type.DEDICATED,
            vlan_tag8021q=1160,
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InterconnectAttachment.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get(request)

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InterconnectAttachment)

    assert response.admin_enabled is True
    assert response.bandwidth == compute.InterconnectAttachment.Bandwidth.BPS_100M
    assert response.candidate_subnets == ["candidate_subnets_value"]
    assert response.cloud_router_ip_address == "cloud_router_ip_address_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.customer_router_ip_address == "customer_router_ip_address_value"
    assert response.dataplane_version == 1807
    assert response.description == "description_value"
    assert (
        response.edge_availability_domain
        == compute.InterconnectAttachment.EdgeAvailabilityDomain.AVAILABILITY_DOMAIN_1
    )
    assert response.google_reference_id == "google_reference_id_value"
    assert response.id == "id_value"
    assert response.interconnect == "interconnect_value"
    assert response.kind == "kind_value"
    assert response.mtu == 342
    assert response.name == "name_value"
    assert (
        response.operational_status
        == compute.InterconnectAttachment.OperationalStatus.OS_ACTIVE
    )
    assert response.pairing_key == "pairing_key_value"
    assert response.partner_asn == "partner_asn_value"
    assert response.partner_metadata == compute.InterconnectAttachmentPartnerMetadata(
        interconnect_name="interconnect_name_value"
    )
    assert (
        response.private_interconnect_info
        == compute.InterconnectAttachmentPrivateInfo(tag8021q=632)
    )
    assert response.region == "region_value"
    assert response.router == "router_value"
    assert response.self_link == "self_link_value"
    assert response.state == compute.InterconnectAttachment.State.ACTIVE
    assert response.type_ == compute.InterconnectAttachment.Type.DEDICATED
    assert response.vlan_tag8021q == 1160


def test_get_rest_from_dict():
    test_get_rest(request_type=dict)


def test_get_rest_flattened():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InterconnectAttachment()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InterconnectAttachment.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get(
            project="project_value",
            region="region_value",
            interconnect_attachment="interconnect_attachment_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "region_value" in http_call[1] + str(body)

        assert "interconnect_attachment_value" in http_call[1] + str(body)


def test_get_rest_flattened_error():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetInterconnectAttachmentRequest(),
            project="project_value",
            region="region_value",
            interconnect_attachment="interconnect_attachment_value",
        )


def test_insert_rest(
    transport: str = "rest", request_type=compute.InsertInterconnectAttachmentRequest
):
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.insert(request)

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_insert_rest_from_dict():
    test_insert_rest(request_type=dict)


def test_insert_rest_flattened():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        interconnect_attachment_resource = compute.InterconnectAttachment(
            admin_enabled=True
        )

        client.insert(
            project="project_value",
            region="region_value",
            interconnect_attachment_resource=interconnect_attachment_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "region_value" in http_call[1] + str(body)

        assert compute.InterconnectAttachment.to_json(
            interconnect_attachment_resource, including_default_value_fields=False
        ) in http_call[1] + str(body)


def test_insert_rest_flattened_error():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert(
            compute.InsertInterconnectAttachmentRequest(),
            project="project_value",
            region="region_value",
            interconnect_attachment_resource=compute.InterconnectAttachment(
                admin_enabled=True
            ),
        )


def test_list_rest(
    transport: str = "rest", request_type=compute.ListInterconnectAttachmentsRequest
):
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InterconnectAttachmentList(
            id="id_value",
            items=[compute.InterconnectAttachment(admin_enabled=True)],
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            warning=compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED),
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InterconnectAttachmentList.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list(request)

    assert response.raw_page is response

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InterconnectAttachmentList)
    assert response.id == "id_value"
    assert response.items == [compute.InterconnectAttachment(admin_enabled=True)]
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.warning == compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED)


def test_list_rest_from_dict():
    test_list_rest(request_type=dict)


def test_list_rest_flattened():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InterconnectAttachmentList()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InterconnectAttachmentList.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list(
            project="project_value", region="region_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "region_value" in http_call[1] + str(body)


def test_list_rest_flattened_error():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListInterconnectAttachmentsRequest(),
            project="project_value",
            region="region_value",
        )


def test_patch_rest(
    transport: str = "rest", request_type=compute.PatchInterconnectAttachmentRequest
):
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.patch(request)

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_patch_rest_from_dict():
    test_patch_rest(request_type=dict)


def test_patch_rest_flattened():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        interconnect_attachment_resource = compute.InterconnectAttachment(
            admin_enabled=True
        )

        client.patch(
            project="project_value",
            region="region_value",
            interconnect_attachment="interconnect_attachment_value",
            interconnect_attachment_resource=interconnect_attachment_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "region_value" in http_call[1] + str(body)

        assert "interconnect_attachment_value" in http_call[1] + str(body)

        assert compute.InterconnectAttachment.to_json(
            interconnect_attachment_resource, including_default_value_fields=False
        ) in http_call[1] + str(body)


def test_patch_rest_flattened_error():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch(
            compute.PatchInterconnectAttachmentRequest(),
            project="project_value",
            region="region_value",
            interconnect_attachment="interconnect_attachment_value",
            interconnect_attachment_resource=compute.InterconnectAttachment(
                admin_enabled=True
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.InterconnectAttachmentsRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InterconnectAttachmentsClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.InterconnectAttachmentsRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InterconnectAttachmentsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.InterconnectAttachmentsRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InterconnectAttachmentsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.InterconnectAttachmentsRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = InterconnectAttachmentsClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class", [transports.InterconnectAttachmentsRestTransport,]
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_interconnect_attachments_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.InterconnectAttachmentsTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_interconnect_attachments_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.interconnect_attachments.transports.InterconnectAttachmentsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.InterconnectAttachmentsTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "aggregated_list",
        "delete",
        "get",
        "insert",
        "list",
        "patch",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_interconnect_attachments_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.interconnect_attachments.transports.InterconnectAttachmentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.InterconnectAttachmentsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_interconnect_attachments_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.compute_v1.services.interconnect_attachments.transports.InterconnectAttachmentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.InterconnectAttachmentsTransport()
        adc.assert_called_once()


def test_interconnect_attachments_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        InterconnectAttachmentsClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_interconnect_attachments_http_transport_client_cert_source_for_mtls():
    cred = credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.InterconnectAttachmentsRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_interconnect_attachments_host_no_port():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_interconnect_attachments_host_with_port():
    client = InterconnectAttachmentsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:8000"


def test_common_billing_account_path():
    billing_account = "squid"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = InterconnectAttachmentsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = InterconnectAttachmentsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = InterconnectAttachmentsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = InterconnectAttachmentsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = InterconnectAttachmentsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = InterconnectAttachmentsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = InterconnectAttachmentsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = InterconnectAttachmentsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = InterconnectAttachmentsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"

    expected = "projects/{project}".format(project=project,)
    actual = InterconnectAttachmentsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = InterconnectAttachmentsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = InterconnectAttachmentsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = InterconnectAttachmentsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = InterconnectAttachmentsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = InterconnectAttachmentsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.InterconnectAttachmentsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = InterconnectAttachmentsClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.InterconnectAttachmentsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = InterconnectAttachmentsClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
