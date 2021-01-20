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
from google.cloud.compute_v1.services.instance_group_managers import (
    InstanceGroupManagersClient,
)
from google.cloud.compute_v1.services.instance_group_managers import transports
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

    assert InstanceGroupManagersClient._get_default_mtls_endpoint(None) is None
    assert (
        InstanceGroupManagersClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        InstanceGroupManagersClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        InstanceGroupManagersClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        InstanceGroupManagersClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        InstanceGroupManagersClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test_instance_group_managers_client_from_service_account_info():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = InstanceGroupManagersClient.from_service_account_info(info)
        assert client.transport._credentials == creds

        assert client.transport._host == "compute.googleapis.com:443"


@pytest.mark.parametrize("client_class", [InstanceGroupManagersClient,])
def test_instance_group_managers_client_from_service_account_file(client_class):
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


def test_instance_group_managers_client_get_transport_class():
    transport = InstanceGroupManagersClient.get_transport_class()
    available_transports = [
        transports.InstanceGroupManagersRestTransport,
    ]
    assert transport in available_transports

    transport = InstanceGroupManagersClient.get_transport_class("rest")
    assert transport == transports.InstanceGroupManagersRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            InstanceGroupManagersClient,
            transports.InstanceGroupManagersRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    InstanceGroupManagersClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(InstanceGroupManagersClient),
)
def test_instance_group_managers_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(InstanceGroupManagersClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(InstanceGroupManagersClient, "get_transport_class") as gtc:
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
            InstanceGroupManagersClient,
            transports.InstanceGroupManagersRestTransport,
            "rest",
            "true",
        ),
        (
            InstanceGroupManagersClient,
            transports.InstanceGroupManagersRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    InstanceGroupManagersClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(InstanceGroupManagersClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_instance_group_managers_client_mtls_env_auto(
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
            InstanceGroupManagersClient,
            transports.InstanceGroupManagersRestTransport,
            "rest",
        ),
    ],
)
def test_instance_group_managers_client_client_options_scopes(
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
            InstanceGroupManagersClient,
            transports.InstanceGroupManagersRestTransport,
            "rest",
        ),
    ],
)
def test_instance_group_managers_client_client_options_credentials_file(
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


def test_abandon_instances_rest(
    transport: str = "rest",
    request_type=compute.AbandonInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.abandon_instances(request)

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


def test_abandon_instances_rest_from_dict():
    test_abandon_instances_rest(request_type=dict)


def test_abandon_instances_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_abandon_instances_request_resource = compute.InstanceGroupManagersAbandonInstancesRequest(
            instances=["instances_value"]
        )

        client.abandon_instances(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_abandon_instances_request_resource=instance_group_managers_abandon_instances_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersAbandonInstancesRequest.to_json(
            instance_group_managers_abandon_instances_request_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_abandon_instances_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.abandon_instances(
            compute.AbandonInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_abandon_instances_request_resource=compute.InstanceGroupManagersAbandonInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_aggregated_list_rest(
    transport: str = "rest",
    request_type=compute.AggregatedListInstanceGroupManagersRequest,
):
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerAggregatedList(
            id="id_value",
            items={
                "key_value": compute.InstanceGroupManagersScopedList(
                    instance_group_managers=[
                        compute.InstanceGroupManager(
                            auto_healing_policies=[
                                compute.InstanceGroupManagerAutoHealingPolicy(
                                    health_check="health_check_value"
                                )
                            ]
                        )
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
        json_return_value = compute.InstanceGroupManagerAggregatedList.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.aggregated_list(request)

    assert response.raw_page is response

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InstanceGroupManagerAggregatedList)
    assert response.id == "id_value"
    assert response.items == {
        "key_value": compute.InstanceGroupManagersScopedList(
            instance_group_managers=[
                compute.InstanceGroupManager(
                    auto_healing_policies=[
                        compute.InstanceGroupManagerAutoHealingPolicy(
                            health_check="health_check_value"
                        )
                    ]
                )
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
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerAggregatedList()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagerAggregatedList.to_json(
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
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListInstanceGroupManagersRequest(),
            project="project_value",
        )


def test_apply_updates_to_instances_rest(
    transport: str = "rest",
    request_type=compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.apply_updates_to_instances(request)

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


def test_apply_updates_to_instances_rest_from_dict():
    test_apply_updates_to_instances_rest(request_type=dict)


def test_apply_updates_to_instances_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_apply_updates_request_resource = compute.InstanceGroupManagersApplyUpdatesRequest(
            all_instances=True
        )

        client.apply_updates_to_instances(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_apply_updates_request_resource=instance_group_managers_apply_updates_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersApplyUpdatesRequest.to_json(
            instance_group_managers_apply_updates_request_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_apply_updates_to_instances_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_updates_to_instances(
            compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_apply_updates_request_resource=compute.InstanceGroupManagersApplyUpdatesRequest(
                all_instances=True
            ),
        )


def test_create_instances_rest(
    transport: str = "rest",
    request_type=compute.CreateInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.create_instances(request)

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


def test_create_instances_rest_from_dict():
    test_create_instances_rest(request_type=dict)


def test_create_instances_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_create_instances_request_resource = compute.InstanceGroupManagersCreateInstancesRequest(
            instances=[compute.PerInstanceConfig(fingerprint="fingerprint_value")]
        )

        client.create_instances(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_create_instances_request_resource=instance_group_managers_create_instances_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersCreateInstancesRequest.to_json(
            instance_group_managers_create_instances_request_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_create_instances_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_instances(
            compute.CreateInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_create_instances_request_resource=compute.InstanceGroupManagersCreateInstancesRequest(
                instances=[compute.PerInstanceConfig(fingerprint="fingerprint_value")]
            ),
        )


def test_delete_rest(
    transport: str = "rest", request_type=compute.DeleteInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
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
    client = InstanceGroupManagersClient(
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
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)


def test_delete_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete(
            compute.DeleteInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_delete_instances_rest(
    transport: str = "rest",
    request_type=compute.DeleteInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.delete_instances(request)

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


def test_delete_instances_rest_from_dict():
    test_delete_instances_rest(request_type=dict)


def test_delete_instances_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_delete_instances_request_resource = compute.InstanceGroupManagersDeleteInstancesRequest(
            instances=["instances_value"]
        )

        client.delete_instances(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_instances_request_resource=instance_group_managers_delete_instances_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersDeleteInstancesRequest.to_json(
            instance_group_managers_delete_instances_request_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_delete_instances_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_instances(
            compute.DeleteInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_instances_request_resource=compute.InstanceGroupManagersDeleteInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_delete_per_instance_configs_rest(
    transport: str = "rest",
    request_type=compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.delete_per_instance_configs(request)

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


def test_delete_per_instance_configs_rest_from_dict():
    test_delete_per_instance_configs_rest(request_type=dict)


def test_delete_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_delete_per_instance_configs_req_resource = compute.InstanceGroupManagersDeletePerInstanceConfigsReq(
            names=["names_value"]
        )

        client.delete_per_instance_configs(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_per_instance_configs_req_resource=instance_group_managers_delete_per_instance_configs_req_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersDeletePerInstanceConfigsReq.to_json(
            instance_group_managers_delete_per_instance_configs_req_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_delete_per_instance_configs_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_per_instance_configs(
            compute.DeletePerInstanceConfigsInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_per_instance_configs_req_resource=compute.InstanceGroupManagersDeletePerInstanceConfigsReq(
                names=["names_value"]
            ),
        )


def test_get_rest(
    transport: str = "rest", request_type=compute.GetInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManager(
            auto_healing_policies=[
                compute.InstanceGroupManagerAutoHealingPolicy(
                    health_check="health_check_value"
                )
            ],
            base_instance_name="base_instance_name_value",
            creation_timestamp="creation_timestamp_value",
            current_actions=compute.InstanceGroupManagerActionsSummary(abandoning=1041),
            description="description_value",
            distribution_policy=compute.DistributionPolicy(
                zones=[compute.DistributionPolicyZoneConfiguration(zone="zone_value")]
            ),
            fingerprint="fingerprint_value",
            id="id_value",
            instance_group="instance_group_value",
            instance_template="instance_template_value",
            kind="kind_value",
            name="name_value",
            named_ports=[compute.NamedPort(name="name_value")],
            region="region_value",
            self_link="self_link_value",
            stateful_policy=compute.StatefulPolicy(
                preserved_state=compute.StatefulPolicyPreservedState(
                    disks={
                        "key_value": compute.StatefulPolicyPreservedStateDiskDevice(
                            auto_delete=compute.StatefulPolicyPreservedStateDiskDevice.AutoDelete.NEVER
                        )
                    }
                )
            ),
            status=compute.InstanceGroupManagerStatus(autoscaler="autoscaler_value"),
            target_pools=["target_pools_value"],
            target_size=1185,
            update_policy=compute.InstanceGroupManagerUpdatePolicy(
                instance_redistribution_type="instance_redistribution_type_value"
            ),
            versions=[
                compute.InstanceGroupManagerVersion(
                    instance_template="instance_template_value"
                )
            ],
            zone="zone_value",
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManager.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get(request)

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InstanceGroupManager)
    assert response.auto_healing_policies == [
        compute.InstanceGroupManagerAutoHealingPolicy(health_check="health_check_value")
    ]
    assert response.base_instance_name == "base_instance_name_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.current_actions == compute.InstanceGroupManagerActionsSummary(
        abandoning=1041
    )
    assert response.description == "description_value"
    assert response.distribution_policy == compute.DistributionPolicy(
        zones=[compute.DistributionPolicyZoneConfiguration(zone="zone_value")]
    )
    assert response.fingerprint == "fingerprint_value"
    assert response.id == "id_value"
    assert response.instance_group == "instance_group_value"
    assert response.instance_template == "instance_template_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.named_ports == [compute.NamedPort(name="name_value")]
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.stateful_policy == compute.StatefulPolicy(
        preserved_state=compute.StatefulPolicyPreservedState(
            disks={
                "key_value": compute.StatefulPolicyPreservedStateDiskDevice(
                    auto_delete=compute.StatefulPolicyPreservedStateDiskDevice.AutoDelete.NEVER
                )
            }
        )
    )
    assert response.status == compute.InstanceGroupManagerStatus(
        autoscaler="autoscaler_value"
    )
    assert response.target_pools == ["target_pools_value"]
    assert response.target_size == 1185
    assert response.update_policy == compute.InstanceGroupManagerUpdatePolicy(
        instance_redistribution_type="instance_redistribution_type_value"
    )
    assert response.versions == [
        compute.InstanceGroupManagerVersion(instance_template="instance_template_value")
    ]
    assert response.zone == "zone_value"


def test_get_rest_from_dict():
    test_get_rest(request_type=dict)


def test_get_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManager()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManager.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)


def test_get_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_insert_rest(
    transport: str = "rest", request_type=compute.InsertInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
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
    client = InstanceGroupManagersClient(
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
        instance_group_manager_resource = compute.InstanceGroupManager(
            auto_healing_policies=[
                compute.InstanceGroupManagerAutoHealingPolicy(
                    health_check="health_check_value"
                )
            ]
        )

        client.insert(
            project="project_value",
            zone="zone_value",
            instance_group_manager_resource=instance_group_manager_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManager.to_json(
            instance_group_manager_resource, including_default_value_fields=False
        ) in http_call[1] + str(body)


def test_insert_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert(
            compute.InsertInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager_resource=compute.InstanceGroupManager(
                auto_healing_policies=[
                    compute.InstanceGroupManagerAutoHealingPolicy(
                        health_check="health_check_value"
                    )
                ]
            ),
        )


def test_list_rest(
    transport: str = "rest", request_type=compute.ListInstanceGroupManagersRequest
):
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerList(
            id="id_value",
            items=[
                compute.InstanceGroupManager(
                    auto_healing_policies=[
                        compute.InstanceGroupManagerAutoHealingPolicy(
                            health_check="health_check_value"
                        )
                    ]
                )
            ],
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            warning=compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED),
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagerList.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list(request)

    assert response.raw_page is response

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InstanceGroupManagerList)
    assert response.id == "id_value"
    assert response.items == [
        compute.InstanceGroupManager(
            auto_healing_policies=[
                compute.InstanceGroupManagerAutoHealingPolicy(
                    health_check="health_check_value"
                )
            ]
        )
    ]
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.warning == compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED)


def test_list_rest_from_dict():
    test_list_rest(request_type=dict)


def test_list_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerList()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagerList.to_json(return_value)
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list(
            project="project_value", zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)


def test_list_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListInstanceGroupManagersRequest(),
            project="project_value",
            zone="zone_value",
        )


def test_list_errors_rest(
    transport: str = "rest", request_type=compute.ListErrorsInstanceGroupManagersRequest
):
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListErrorsResponse(
            items=[
                compute.InstanceManagedByIgmError(
                    error=compute.InstanceManagedByIgmErrorManagedInstanceError(
                        code="code_value"
                    )
                )
            ],
            next_page_token="next_page_token_value",
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagersListErrorsResponse.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_errors(request)

    assert response.raw_page is response

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InstanceGroupManagersListErrorsResponse)
    assert response.items == [
        compute.InstanceManagedByIgmError(
            error=compute.InstanceManagedByIgmErrorManagedInstanceError(
                code="code_value"
            )
        )
    ]
    assert response.next_page_token == "next_page_token_value"


def test_list_errors_rest_from_dict():
    test_list_errors_rest(request_type=dict)


def test_list_errors_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListErrorsResponse()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagersListErrorsResponse.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_errors(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)


def test_list_errors_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_errors(
            compute.ListErrorsInstanceGroupManagersRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_list_managed_instances_rest(
    transport: str = "rest",
    request_type=compute.ListManagedInstancesInstanceGroupManagersRequest,
):
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListManagedInstancesResponse(
            managed_instances=[
                compute.ManagedInstance(
                    current_action=compute.ManagedInstance.CurrentAction.ABANDONING
                )
            ],
            next_page_token="next_page_token_value",
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagersListManagedInstancesResponse.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_managed_instances(request)

    assert response.raw_page is response

    # Establish that the response is the type that we expect.

    assert isinstance(
        response, compute.InstanceGroupManagersListManagedInstancesResponse
    )
    assert response.managed_instances == [
        compute.ManagedInstance(
            current_action=compute.ManagedInstance.CurrentAction.ABANDONING
        )
    ]
    assert response.next_page_token == "next_page_token_value"


def test_list_managed_instances_rest_from_dict():
    test_list_managed_instances_rest(request_type=dict)


def test_list_managed_instances_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListManagedInstancesResponse()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagersListManagedInstancesResponse.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_managed_instances(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)


def test_list_managed_instances_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_managed_instances(
            compute.ListManagedInstancesInstanceGroupManagersRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_list_per_instance_configs_rest(
    transport: str = "rest",
    request_type=compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
):
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp(
            items=[compute.PerInstanceConfig(fingerprint="fingerprint_value")],
            next_page_token="next_page_token_value",
            warning=compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED),
        )
        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_per_instance_configs(request)

    assert response.raw_page is response

    # Establish that the response is the type that we expect.

    assert isinstance(response, compute.InstanceGroupManagersListPerInstanceConfigsResp)
    assert response.items == [
        compute.PerInstanceConfig(fingerprint="fingerprint_value")
    ]
    assert response.next_page_token == "next_page_token_value"
    assert response.warning == compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED)


def test_list_per_instance_configs_rest_from_dict():
    test_list_per_instance_configs_rest(request_type=dict)


def test_list_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp()

        # Wrap the value into a proper Response obj
        json_return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp.to_json(
            return_value
        )
        response_value = Response()
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_per_instance_configs(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)


def test_list_per_instance_configs_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_per_instance_configs(
            compute.ListPerInstanceConfigsInstanceGroupManagersRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_patch_rest(
    transport: str = "rest", request_type=compute.PatchInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
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
    client = InstanceGroupManagersClient(
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
        instance_group_manager_resource = compute.InstanceGroupManager(
            auto_healing_policies=[
                compute.InstanceGroupManagerAutoHealingPolicy(
                    health_check="health_check_value"
                )
            ]
        )

        client.patch(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_manager_resource=instance_group_manager_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManager.to_json(
            instance_group_manager_resource, including_default_value_fields=False
        ) in http_call[1] + str(body)


def test_patch_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch(
            compute.PatchInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_manager_resource=compute.InstanceGroupManager(
                auto_healing_policies=[
                    compute.InstanceGroupManagerAutoHealingPolicy(
                        health_check="health_check_value"
                    )
                ]
            ),
        )


def test_patch_per_instance_configs_rest(
    transport: str = "rest",
    request_type=compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.patch_per_instance_configs(request)

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


def test_patch_per_instance_configs_rest_from_dict():
    test_patch_per_instance_configs_rest(request_type=dict)


def test_patch_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_patch_per_instance_configs_req_resource = compute.InstanceGroupManagersPatchPerInstanceConfigsReq(
            per_instance_configs=[
                compute.PerInstanceConfig(fingerprint="fingerprint_value")
            ]
        )

        client.patch_per_instance_configs(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_patch_per_instance_configs_req_resource=instance_group_managers_patch_per_instance_configs_req_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersPatchPerInstanceConfigsReq.to_json(
            instance_group_managers_patch_per_instance_configs_req_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_patch_per_instance_configs_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_per_instance_configs(
            compute.PatchPerInstanceConfigsInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_patch_per_instance_configs_req_resource=compute.InstanceGroupManagersPatchPerInstanceConfigsReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )


def test_recreate_instances_rest(
    transport: str = "rest",
    request_type=compute.RecreateInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.recreate_instances(request)

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


def test_recreate_instances_rest_from_dict():
    test_recreate_instances_rest(request_type=dict)


def test_recreate_instances_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_recreate_instances_request_resource = compute.InstanceGroupManagersRecreateInstancesRequest(
            instances=["instances_value"]
        )

        client.recreate_instances(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_recreate_instances_request_resource=instance_group_managers_recreate_instances_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersRecreateInstancesRequest.to_json(
            instance_group_managers_recreate_instances_request_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_recreate_instances_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.recreate_instances(
            compute.RecreateInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_recreate_instances_request_resource=compute.InstanceGroupManagersRecreateInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_resize_rest(
    transport: str = "rest", request_type=compute.ResizeInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
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

        response = client.resize(request)

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


def test_resize_rest_from_dict():
    test_resize_rest(request_type=dict)


def test_resize_rest_flattened():
    client = InstanceGroupManagersClient(
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
        client.resize(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            size=443,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert str(443) in http_call[1] + str(body)


def test_resize_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resize(
            compute.ResizeInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            size=443,
        )


def test_set_instance_template_rest(
    transport: str = "rest",
    request_type=compute.SetInstanceTemplateInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.set_instance_template(request)

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


def test_set_instance_template_rest_from_dict():
    test_set_instance_template_rest(request_type=dict)


def test_set_instance_template_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_set_instance_template_request_resource = compute.InstanceGroupManagersSetInstanceTemplateRequest(
            instance_template="instance_template_value"
        )

        client.set_instance_template(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_instance_template_request_resource=instance_group_managers_set_instance_template_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersSetInstanceTemplateRequest.to_json(
            instance_group_managers_set_instance_template_request_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_set_instance_template_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_instance_template(
            compute.SetInstanceTemplateInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_instance_template_request_resource=compute.InstanceGroupManagersSetInstanceTemplateRequest(
                instance_template="instance_template_value"
            ),
        )


def test_set_target_pools_rest(
    transport: str = "rest",
    request_type=compute.SetTargetPoolsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.set_target_pools(request)

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


def test_set_target_pools_rest_from_dict():
    test_set_target_pools_rest(request_type=dict)


def test_set_target_pools_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_set_target_pools_request_resource = compute.InstanceGroupManagersSetTargetPoolsRequest(
            fingerprint="fingerprint_value"
        )

        client.set_target_pools(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_target_pools_request_resource=instance_group_managers_set_target_pools_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersSetTargetPoolsRequest.to_json(
            instance_group_managers_set_target_pools_request_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_set_target_pools_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_target_pools(
            compute.SetTargetPoolsInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_target_pools_request_resource=compute.InstanceGroupManagersSetTargetPoolsRequest(
                fingerprint="fingerprint_value"
            ),
        )


def test_update_per_instance_configs_rest(
    transport: str = "rest",
    request_type=compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
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

        response = client.update_per_instance_configs(request)

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


def test_update_per_instance_configs_rest_from_dict():
    test_update_per_instance_configs_rest(request_type=dict)


def test_update_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
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
        instance_group_managers_update_per_instance_configs_req_resource = compute.InstanceGroupManagersUpdatePerInstanceConfigsReq(
            per_instance_configs=[
                compute.PerInstanceConfig(fingerprint="fingerprint_value")
            ]
        )

        client.update_per_instance_configs(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_update_per_instance_configs_req_resource=instance_group_managers_update_per_instance_configs_req_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("json")

        assert "project_value" in http_call[1] + str(body)

        assert "zone_value" in http_call[1] + str(body)

        assert "instance_group_manager_value" in http_call[1] + str(body)

        assert compute.InstanceGroupManagersUpdatePerInstanceConfigsReq.to_json(
            instance_group_managers_update_per_instance_configs_req_resource,
            including_default_value_fields=False,
        ) in http_call[1] + str(body)


def test_update_per_instance_configs_rest_flattened_error():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_per_instance_configs(
            compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_update_per_instance_configs_req_resource=compute.InstanceGroupManagersUpdatePerInstanceConfigsReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class", [transports.InstanceGroupManagersRestTransport,]
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_instance_group_managers_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.InstanceGroupManagersTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_instance_group_managers_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.instance_group_managers.transports.InstanceGroupManagersTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.InstanceGroupManagersTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "abandon_instances",
        "aggregated_list",
        "apply_updates_to_instances",
        "create_instances",
        "delete",
        "delete_instances",
        "delete_per_instance_configs",
        "get",
        "insert",
        "list",
        "list_errors",
        "list_managed_instances",
        "list_per_instance_configs",
        "patch",
        "patch_per_instance_configs",
        "recreate_instances",
        "resize",
        "set_instance_template",
        "set_target_pools",
        "update_per_instance_configs",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_instance_group_managers_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.instance_group_managers.transports.InstanceGroupManagersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.InstanceGroupManagersTransport(
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


def test_instance_group_managers_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.compute_v1.services.instance_group_managers.transports.InstanceGroupManagersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.InstanceGroupManagersTransport()
        adc.assert_called_once()


def test_instance_group_managers_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        InstanceGroupManagersClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_instance_group_managers_http_transport_client_cert_source_for_mtls():
    cred = credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.InstanceGroupManagersRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_instance_group_managers_host_no_port():
    client = InstanceGroupManagersClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_instance_group_managers_host_with_port():
    client = InstanceGroupManagersClient(
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
    actual = InstanceGroupManagersClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = InstanceGroupManagersClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = InstanceGroupManagersClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = InstanceGroupManagersClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = InstanceGroupManagersClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = InstanceGroupManagersClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = InstanceGroupManagersClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = InstanceGroupManagersClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = InstanceGroupManagersClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"

    expected = "projects/{project}".format(project=project,)
    actual = InstanceGroupManagersClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = InstanceGroupManagersClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = InstanceGroupManagersClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = InstanceGroupManagersClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = InstanceGroupManagersClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = InstanceGroupManagersClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.InstanceGroupManagersTransport, "_prep_wrapped_messages"
    ) as prep:
        client = InstanceGroupManagersClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.InstanceGroupManagersTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = InstanceGroupManagersClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
