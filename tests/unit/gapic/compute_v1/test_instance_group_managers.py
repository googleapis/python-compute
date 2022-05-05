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
import os
import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import extended_operation  # type: ignore
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.compute_v1.services.instance_group_managers import (
    InstanceGroupManagersClient,
)
from google.cloud.compute_v1.services.instance_group_managers import pagers
from google.cloud.compute_v1.services.instance_group_managers import transports
from google.cloud.compute_v1.types import compute
from google.oauth2 import service_account
import google.auth


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


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (InstanceGroupManagersClient, "rest"),
    ],
)
def test_instance_group_managers_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "compute.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://compute.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.InstanceGroupManagersRestTransport, "rest"),
    ],
)
def test_instance_group_managers_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (InstanceGroupManagersClient, "rest"),
    ],
)
def test_instance_group_managers_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "compute.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://compute.googleapis.com"
        )


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
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
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
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
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
            client = client_class(client_options=options, transport=transport_name)

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
                always_use_jwt_access=True,
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
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
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
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize("client_class", [InstanceGroupManagersClient])
@mock.patch.object(
    InstanceGroupManagersClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(InstanceGroupManagersClient),
)
def test_instance_group_managers_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


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
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            InstanceGroupManagersClient,
            transports.InstanceGroupManagersRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_instance_group_managers_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.AbandonInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_abandon_instances_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_abandon_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.abandon_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_abandon_instances_rest_required_fields(
    request_type=compute.AbandonInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).abandon_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).abandon_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.abandon_instances(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_abandon_instances_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.abandon_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersAbandonInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_abandon_instances_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_abandon_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_abandon_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.AbandonInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.abandon_instances(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_abandon_instances_rest_bad_request(
    transport: str = "rest",
    request_type=compute.AbandonInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_abandon_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.abandon_instances(request)


def test_abandon_instances_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_abandon_instances_request_resource=compute.InstanceGroupManagersAbandonInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.abandon_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/abandonInstances"
            % client.transport._host,
            args[1],
        )


def test_abandon_instances_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_abandon_instances_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.AbandonInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_abandon_instances_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_abandon_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.abandon_instances_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_abandon_instances_unary_rest_required_fields(
    request_type=compute.AbandonInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).abandon_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).abandon_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.abandon_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_abandon_instances_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.abandon_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersAbandonInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_abandon_instances_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_abandon_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_abandon_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.AbandonInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.abandon_instances_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_abandon_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.AbandonInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_abandon_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.abandon_instances_unary(request)


def test_abandon_instances_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_abandon_instances_request_resource=compute.InstanceGroupManagersAbandonInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.abandon_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/abandonInstances"
            % client.transport._host,
            args[1],
        )


def test_abandon_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.abandon_instances_unary(
            compute.AbandonInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_abandon_instances_request_resource=compute.InstanceGroupManagersAbandonInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_abandon_instances_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.AggregatedListInstanceGroupManagersRequest,
        dict,
    ],
)
def test_aggregated_list_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerAggregatedList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            unreachables=["unreachables_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManagerAggregatedList.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.aggregated_list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AggregatedListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.unreachables == ["unreachables_value"]


def test_aggregated_list_rest_required_fields(
    request_type=compute.AggregatedListInstanceGroupManagersRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).aggregated_list._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).aggregated_list._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "include_all_scopes",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.InstanceGroupManagerAggregatedList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.InstanceGroupManagerAggregatedList.to_json(
                return_value
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.aggregated_list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_aggregated_list_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.aggregated_list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "includeAllScopes",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(("project",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_aggregated_list_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_aggregated_list"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_aggregated_list"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.InstanceGroupManagerAggregatedList.to_json(
            compute.InstanceGroupManagerAggregatedList()
        )

        request = compute.AggregatedListInstanceGroupManagersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.InstanceGroupManagerAggregatedList

        client.aggregated_list(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_aggregated_list_rest_bad_request(
    transport: str = "rest",
    request_type=compute.AggregatedListInstanceGroupManagersRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.aggregated_list(request)


def test_aggregated_list_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerAggregatedList()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManagerAggregatedList.to_json(
            return_value
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.aggregated_list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/aggregated/instanceGroupManagers"
            % client.transport._host,
            args[1],
        )


def test_aggregated_list_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListInstanceGroupManagersRequest(),
            project="project_value",
        )


def test_aggregated_list_rest_pager(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceGroupManagerAggregatedList(
                items={
                    "a": compute.InstanceGroupManagersScopedList(),
                    "b": compute.InstanceGroupManagersScopedList(),
                    "c": compute.InstanceGroupManagersScopedList(),
                },
                next_page_token="abc",
            ),
            compute.InstanceGroupManagerAggregatedList(
                items={},
                next_page_token="def",
            ),
            compute.InstanceGroupManagerAggregatedList(
                items={
                    "g": compute.InstanceGroupManagersScopedList(),
                },
                next_page_token="ghi",
            ),
            compute.InstanceGroupManagerAggregatedList(
                items={
                    "h": compute.InstanceGroupManagersScopedList(),
                    "i": compute.InstanceGroupManagersScopedList(),
                },
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.InstanceGroupManagerAggregatedList.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1"}

        pager = client.aggregated_list(request=sample_request)

        assert isinstance(pager.get("a"), compute.InstanceGroupManagersScopedList)
        assert pager.get("h") is None

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tuple) for i in results)
        for result in results:
            assert isinstance(result, tuple)
            assert tuple(type(t) for t in result) == (
                str,
                compute.InstanceGroupManagersScopedList,
            )

        assert pager.get("a") is None
        assert isinstance(pager.get("h"), compute.InstanceGroupManagersScopedList)

        pages = list(client.aggregated_list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_apply_updates_to_instances_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_apply_updates_request_resource"] = {
        "all_instances": True,
        "instances": ["instances_value_1", "instances_value_2"],
        "minimal_action": "minimal_action_value",
        "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.apply_updates_to_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_apply_updates_to_instances_rest_required_fields(
    request_type=compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_updates_to_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_updates_to_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.apply_updates_to_instances(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_apply_updates_to_instances_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.apply_updates_to_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersApplyUpdatesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_apply_updates_to_instances_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_apply_updates_to_instances",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_apply_updates_to_instances",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.apply_updates_to_instances(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_apply_updates_to_instances_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_apply_updates_request_resource"] = {
        "all_instances": True,
        "instances": ["instances_value_1", "instances_value_2"],
        "minimal_action": "minimal_action_value",
        "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.apply_updates_to_instances(request)


def test_apply_updates_to_instances_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_apply_updates_request_resource=compute.InstanceGroupManagersApplyUpdatesRequest(
                all_instances=True
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.apply_updates_to_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/applyUpdatesToInstances"
            % client.transport._host,
            args[1],
        )


def test_apply_updates_to_instances_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_apply_updates_to_instances_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_apply_updates_to_instances_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_apply_updates_request_resource"] = {
        "all_instances": True,
        "instances": ["instances_value_1", "instances_value_2"],
        "minimal_action": "minimal_action_value",
        "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.apply_updates_to_instances_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_apply_updates_to_instances_unary_rest_required_fields(
    request_type=compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_updates_to_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_updates_to_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.apply_updates_to_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_apply_updates_to_instances_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.apply_updates_to_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersApplyUpdatesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_apply_updates_to_instances_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_apply_updates_to_instances",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_apply_updates_to_instances",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.apply_updates_to_instances_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_apply_updates_to_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_apply_updates_request_resource"] = {
        "all_instances": True,
        "instances": ["instances_value_1", "instances_value_2"],
        "minimal_action": "minimal_action_value",
        "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.apply_updates_to_instances_unary(request)


def test_apply_updates_to_instances_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_apply_updates_request_resource=compute.InstanceGroupManagersApplyUpdatesRequest(
                all_instances=True
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.apply_updates_to_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/applyUpdatesToInstances"
            % client.transport._host,
            args[1],
        )


def test_apply_updates_to_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_updates_to_instances_unary(
            compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_apply_updates_request_resource=compute.InstanceGroupManagersApplyUpdatesRequest(
                all_instances=True
            ),
        )


def test_apply_updates_to_instances_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.CreateInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_create_instances_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_create_instances_request_resource"] = {
        "instances": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_create_instances_rest_required_fields(
    request_type=compute.CreateInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_instances(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_instances_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersCreateInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_instances_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_create_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_create_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.CreateInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.create_instances(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_instances_rest_bad_request(
    transport: str = "rest",
    request_type=compute.CreateInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_create_instances_request_resource"] = {
        "instances": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_instances(request)


def test_create_instances_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_create_instances_request_resource=compute.InstanceGroupManagersCreateInstancesRequest(
                instances=[compute.PerInstanceConfig(fingerprint="fingerprint_value")]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/createInstances"
            % client.transport._host,
            args[1],
        )


def test_create_instances_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_create_instances_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.CreateInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_create_instances_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_create_instances_request_resource"] = {
        "instances": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_instances_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_create_instances_unary_rest_required_fields(
    request_type=compute.CreateInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_instances_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersCreateInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_instances_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_create_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_create_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.CreateInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.create_instances_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.CreateInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_create_instances_request_resource"] = {
        "instances": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_instances_unary(request)


def test_create_instances_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_create_instances_request_resource=compute.InstanceGroupManagersCreateInstancesRequest(
                instances=[compute.PerInstanceConfig(fingerprint="fingerprint_value")]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/createInstances"
            % client.transport._host,
            args[1],
        )


def test_create_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_instances_unary(
            compute.CreateInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_create_instances_request_resource=compute.InstanceGroupManagersCreateInstancesRequest(
                instances=[compute.PerInstanceConfig(fingerprint="fingerprint_value")]
            ),
        )


def test_create_instances_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeleteInstanceGroupManagerRequest,
        dict,
    ],
)
def test_delete_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_rest_required_fields(
    request_type=compute.DeleteInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_delete"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_delete"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeleteInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.delete(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete(request)


def test_delete_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_delete_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_delete_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeleteInstanceGroupManagerRequest,
        dict,
    ],
)
def test_delete_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_delete_unary_rest_required_fields(
    request_type=compute.DeleteInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_delete"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_delete"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeleteInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.delete_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_unary(request)


def test_delete_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_delete_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_unary(
            compute.DeleteInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_delete_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeleteInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_delete_instances_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"],
        "skip_instances_on_validation_error": True,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_instances_rest_required_fields(
    request_type=compute.DeleteInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_instances(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_instances_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersDeleteInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_instances_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_delete_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_delete_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeleteInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.delete_instances(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_instances_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeleteInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"],
        "skip_instances_on_validation_error": True,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_instances(request)


def test_delete_instances_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_instances_request_resource=compute.InstanceGroupManagersDeleteInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/deleteInstances"
            % client.transport._host,
            args[1],
        )


def test_delete_instances_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_delete_instances_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeleteInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_delete_instances_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"],
        "skip_instances_on_validation_error": True,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_instances_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_delete_instances_unary_rest_required_fields(
    request_type=compute.DeleteInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_instances_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersDeleteInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_instances_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_delete_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_delete_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeleteInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.delete_instances_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeleteInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"],
        "skip_instances_on_validation_error": True,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_instances_unary(request)


def test_delete_instances_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_instances_request_resource=compute.InstanceGroupManagersDeleteInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/deleteInstances"
            % client.transport._host,
            args[1],
        )


def test_delete_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_instances_unary(
            compute.DeleteInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_instances_request_resource=compute.InstanceGroupManagersDeleteInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_delete_instances_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_delete_per_instance_configs_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_per_instance_configs_req_resource"] = {
        "names": ["names_value_1", "names_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_per_instance_configs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_per_instance_configs_rest_required_fields(
    request_type=compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_per_instance_configs(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_per_instance_configs_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersDeletePerInstanceConfigsReqResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_per_instance_configs_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_delete_per_instance_configs",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_delete_per_instance_configs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeletePerInstanceConfigsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.delete_per_instance_configs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_per_instance_configs_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_per_instance_configs_req_resource"] = {
        "names": ["names_value_1", "names_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_per_instance_configs(request)


def test_delete_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_per_instance_configs_req_resource=compute.InstanceGroupManagersDeletePerInstanceConfigsReq(
                names=["names_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_per_instance_configs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/deletePerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_delete_per_instance_configs_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_delete_per_instance_configs_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_delete_per_instance_configs_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_per_instance_configs_req_resource"] = {
        "names": ["names_value_1", "names_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_per_instance_configs_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_delete_per_instance_configs_unary_rest_required_fields(
    request_type=compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_per_instance_configs_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_per_instance_configs_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersDeletePerInstanceConfigsReqResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_per_instance_configs_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_delete_per_instance_configs",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_delete_per_instance_configs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeletePerInstanceConfigsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.delete_per_instance_configs_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_per_instance_configs_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_delete_per_instance_configs_req_resource"] = {
        "names": ["names_value_1", "names_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_per_instance_configs_unary(request)


def test_delete_per_instance_configs_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_per_instance_configs_req_resource=compute.InstanceGroupManagersDeletePerInstanceConfigsReq(
                names=["names_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_per_instance_configs_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/deletePerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_delete_per_instance_configs_unary_rest_flattened_error(
    transport: str = "rest",
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_per_instance_configs_unary(
            compute.DeletePerInstanceConfigsInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_delete_per_instance_configs_req_resource=compute.InstanceGroupManagersDeletePerInstanceConfigsReq(
                names=["names_value"]
            ),
        )


def test_delete_per_instance_configs_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.GetInstanceGroupManagerRequest,
        dict,
    ],
)
def test_get_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManager(
            base_instance_name="base_instance_name_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            fingerprint="fingerprint_value",
            id=205,
            instance_group="instance_group_value",
            instance_template="instance_template_value",
            kind="kind_value",
            name="name_value",
            region="region_value",
            self_link="self_link_value",
            target_pools=["target_pools_value"],
            target_size=1185,
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManager.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.InstanceGroupManager)
    assert response.base_instance_name == "base_instance_name_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.fingerprint == "fingerprint_value"
    assert response.id == 205
    assert response.instance_group == "instance_group_value"
    assert response.instance_template == "instance_template_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.target_pools == ["target_pools_value"]
    assert response.target_size == 1185
    assert response.zone == "zone_value"


def test_get_rest_required_fields(request_type=compute.GetInstanceGroupManagerRequest):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.InstanceGroupManager()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.InstanceGroupManager.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instanceGroupManager",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_get"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_get"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.InstanceGroupManager.to_json(
            compute.InstanceGroupManager()
        )

        request = compute.GetInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.InstanceGroupManager

        client.get(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_rest_bad_request(
    transport: str = "rest", request_type=compute.GetInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get(request)


def test_get_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManager()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManager.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_get_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.InsertInstanceGroupManagerRequest,
        dict,
    ],
)
def test_insert_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_insert_rest_required_fields(
    request_type=compute.InsertInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.insert(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_insert_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManagerResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_insert_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_insert"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_insert"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.InsertInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.insert(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_insert_rest_bad_request(
    transport: str = "rest", request_type=compute.InsertInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.insert(request)


def test_insert_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
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
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.insert(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers"
            % client.transport._host,
            args[1],
        )


def test_insert_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_insert_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.InsertInstanceGroupManagerRequest,
        dict,
    ],
)
def test_insert_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_insert_unary_rest_required_fields(
    request_type=compute.InsertInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.insert_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_insert_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManagerResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_insert_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_insert"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_insert"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.InsertInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.insert_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_insert_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.InsertInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.insert_unary(request)


def test_insert_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
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
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.insert_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers"
            % client.transport._host,
            args[1],
        )


def test_insert_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert_unary(
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


def test_insert_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ListInstanceGroupManagersRequest,
        dict,
    ],
)
def test_list_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManagerList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"


def test_list_rest_required_fields(
    request_type=compute.ListInstanceGroupManagersRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.InstanceGroupManagerList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.InstanceGroupManagerList.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(
            (
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_list"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_list"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.InstanceGroupManagerList.to_json(
            compute.InstanceGroupManagerList()
        )

        request = compute.ListInstanceGroupManagersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.InstanceGroupManagerList

        client.list(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_rest_bad_request(
    transport: str = "rest", request_type=compute.ListInstanceGroupManagersRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list(request)


def test_list_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagerList()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManagerList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers"
            % client.transport._host,
            args[1],
        )


def test_list_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListInstanceGroupManagersRequest(),
            project="project_value",
            zone="zone_value",
        )


def test_list_rest_pager(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceGroupManagerList(
                items=[
                    compute.InstanceGroupManager(),
                    compute.InstanceGroupManager(),
                    compute.InstanceGroupManager(),
                ],
                next_page_token="abc",
            ),
            compute.InstanceGroupManagerList(
                items=[],
                next_page_token="def",
            ),
            compute.InstanceGroupManagerList(
                items=[
                    compute.InstanceGroupManager(),
                ],
                next_page_token="ghi",
            ),
            compute.InstanceGroupManagerList(
                items=[
                    compute.InstanceGroupManager(),
                    compute.InstanceGroupManager(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.InstanceGroupManagerList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1", "zone": "sample2"}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.InstanceGroupManager) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ListErrorsInstanceGroupManagersRequest,
        dict,
    ],
)
def test_list_errors_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListErrorsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManagersListErrorsResponse.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_errors(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListErrorsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_errors_rest_required_fields(
    request_type=compute.ListErrorsInstanceGroupManagersRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_errors._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_errors._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.InstanceGroupManagersListErrorsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.InstanceGroupManagersListErrorsResponse.to_json(
                return_value
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_errors(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_errors_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_errors._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(
            (
                "instanceGroupManager",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_errors_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_list_errors"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_list_errors"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            compute.InstanceGroupManagersListErrorsResponse.to_json(
                compute.InstanceGroupManagersListErrorsResponse()
            )
        )

        request = compute.ListErrorsInstanceGroupManagersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.InstanceGroupManagersListErrorsResponse

        client.list_errors(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_errors_rest_bad_request(
    transport: str = "rest", request_type=compute.ListErrorsInstanceGroupManagersRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_errors(request)


def test_list_errors_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListErrorsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManagersListErrorsResponse.to_json(
            return_value
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_errors(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/listErrors"
            % client.transport._host,
            args[1],
        )


def test_list_errors_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_errors_rest_pager(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceGroupManagersListErrorsResponse(
                items=[
                    compute.InstanceManagedByIgmError(),
                    compute.InstanceManagedByIgmError(),
                    compute.InstanceManagedByIgmError(),
                ],
                next_page_token="abc",
            ),
            compute.InstanceGroupManagersListErrorsResponse(
                items=[],
                next_page_token="def",
            ),
            compute.InstanceGroupManagersListErrorsResponse(
                items=[
                    compute.InstanceManagedByIgmError(),
                ],
                next_page_token="ghi",
            ),
            compute.InstanceGroupManagersListErrorsResponse(
                items=[
                    compute.InstanceManagedByIgmError(),
                    compute.InstanceManagedByIgmError(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.InstanceGroupManagersListErrorsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        pager = client.list_errors(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.InstanceManagedByIgmError) for i in results)

        pages = list(client.list_errors(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ListManagedInstancesInstanceGroupManagersRequest,
        dict,
    ],
)
def test_list_managed_instances_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListManagedInstancesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = (
            compute.InstanceGroupManagersListManagedInstancesResponse.to_json(
                return_value
            )
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_managed_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListManagedInstancesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_managed_instances_rest_required_fields(
    request_type=compute.ListManagedInstancesInstanceGroupManagersRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_managed_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_managed_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.InstanceGroupManagersListManagedInstancesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = (
                compute.InstanceGroupManagersListManagedInstancesResponse.to_json(
                    return_value
                )
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_managed_instances(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_managed_instances_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_managed_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(
            (
                "instanceGroupManager",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_managed_instances_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_list_managed_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_list_managed_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            compute.InstanceGroupManagersListManagedInstancesResponse.to_json(
                compute.InstanceGroupManagersListManagedInstancesResponse()
            )
        )

        request = compute.ListManagedInstancesInstanceGroupManagersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.InstanceGroupManagersListManagedInstancesResponse

        client.list_managed_instances(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_managed_instances_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ListManagedInstancesInstanceGroupManagersRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_managed_instances(request)


def test_list_managed_instances_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListManagedInstancesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = (
            compute.InstanceGroupManagersListManagedInstancesResponse.to_json(
                return_value
            )
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_managed_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/listManagedInstances"
            % client.transport._host,
            args[1],
        )


def test_list_managed_instances_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_managed_instances_rest_pager(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceGroupManagersListManagedInstancesResponse(
                managed_instances=[
                    compute.ManagedInstance(),
                    compute.ManagedInstance(),
                    compute.ManagedInstance(),
                ],
                next_page_token="abc",
            ),
            compute.InstanceGroupManagersListManagedInstancesResponse(
                managed_instances=[],
                next_page_token="def",
            ),
            compute.InstanceGroupManagersListManagedInstancesResponse(
                managed_instances=[
                    compute.ManagedInstance(),
                ],
                next_page_token="ghi",
            ),
            compute.InstanceGroupManagersListManagedInstancesResponse(
                managed_instances=[
                    compute.ManagedInstance(),
                    compute.ManagedInstance(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.InstanceGroupManagersListManagedInstancesResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        pager = client.list_managed_instances(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.ManagedInstance) for i in results)

        pages = list(client.list_managed_instances(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
        dict,
    ],
)
def test_list_per_instance_configs_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = (
            compute.InstanceGroupManagersListPerInstanceConfigsResp.to_json(
                return_value
            )
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_per_instance_configs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPerInstanceConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_per_instance_configs_rest_required_fields(
    request_type=compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = (
                compute.InstanceGroupManagersListPerInstanceConfigsResp.to_json(
                    return_value
                )
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_per_instance_configs(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_per_instance_configs_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(
            (
                "instanceGroupManager",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_per_instance_configs_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_list_per_instance_configs",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_list_per_instance_configs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            compute.InstanceGroupManagersListPerInstanceConfigsResp.to_json(
                compute.InstanceGroupManagersListPerInstanceConfigsResp()
            )
        )

        request = compute.ListPerInstanceConfigsInstanceGroupManagersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp

        client.list_per_instance_configs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_per_instance_configs_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_per_instance_configs(request)


def test_list_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManagersListPerInstanceConfigsResp()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = (
            compute.InstanceGroupManagersListPerInstanceConfigsResp.to_json(
                return_value
            )
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_per_instance_configs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/listPerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_list_per_instance_configs_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_per_instance_configs_rest_pager(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceGroupManagersListPerInstanceConfigsResp(
                items=[
                    compute.PerInstanceConfig(),
                    compute.PerInstanceConfig(),
                    compute.PerInstanceConfig(),
                ],
                next_page_token="abc",
            ),
            compute.InstanceGroupManagersListPerInstanceConfigsResp(
                items=[],
                next_page_token="def",
            ),
            compute.InstanceGroupManagersListPerInstanceConfigsResp(
                items=[
                    compute.PerInstanceConfig(),
                ],
                next_page_token="ghi",
            ),
            compute.InstanceGroupManagersListPerInstanceConfigsResp(
                items=[
                    compute.PerInstanceConfig(),
                    compute.PerInstanceConfig(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.InstanceGroupManagersListPerInstanceConfigsResp.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        pager = client.list_per_instance_configs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.PerInstanceConfig) for i in results)

        pages = list(client.list_per_instance_configs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchInstanceGroupManagerRequest,
        dict,
    ],
)
def test_patch_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_patch_rest_required_fields(
    request_type=compute.PatchInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagerResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_patch"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_patch"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.patch(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch(request)


def test_patch_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
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
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_patch_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_patch_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchInstanceGroupManagerRequest,
        dict,
    ],
)
def test_patch_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_patch_unary_rest_required_fields(
    request_type=compute.PatchInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagerResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_patch"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_patch"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.patch_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "resuming": 874,
            "starting": 876,
            "stopping": 884,
            "suspending": 1088,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {},
            "minimal_action": "minimal_action_value",
            "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {},
            }
        ],
        "zone": "zone_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_unary(request)


def test_patch_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
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
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_patch_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_unary(
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


def test_patch_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_patch_per_instance_configs_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_patch_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_per_instance_configs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_patch_per_instance_configs_rest_required_fields(
    request_type=compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_per_instance_configs(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_per_instance_configs_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersPatchPerInstanceConfigsReqResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_per_instance_configs_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_patch_per_instance_configs",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_patch_per_instance_configs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchPerInstanceConfigsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.patch_per_instance_configs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_per_instance_configs_rest_bad_request(
    transport: str = "rest",
    request_type=compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_patch_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_per_instance_configs(request)


def test_patch_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_patch_per_instance_configs_req_resource=compute.InstanceGroupManagersPatchPerInstanceConfigsReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch_per_instance_configs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/patchPerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_patch_per_instance_configs_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_patch_per_instance_configs_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_patch_per_instance_configs_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_patch_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_per_instance_configs_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_patch_per_instance_configs_unary_rest_required_fields(
    request_type=compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_per_instance_configs_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_per_instance_configs_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersPatchPerInstanceConfigsReqResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_per_instance_configs_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_patch_per_instance_configs",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_patch_per_instance_configs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchPerInstanceConfigsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.patch_per_instance_configs_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_per_instance_configs_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_patch_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_per_instance_configs_unary(request)


def test_patch_per_instance_configs_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_patch_per_instance_configs_req_resource=compute.InstanceGroupManagersPatchPerInstanceConfigsReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch_per_instance_configs_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/patchPerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_patch_per_instance_configs_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_per_instance_configs_unary(
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


def test_patch_per_instance_configs_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.RecreateInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_recreate_instances_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_recreate_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.recreate_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_recreate_instances_rest_required_fields(
    request_type=compute.RecreateInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).recreate_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).recreate_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.recreate_instances(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_recreate_instances_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.recreate_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersRecreateInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_recreate_instances_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_recreate_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_recreate_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.RecreateInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.recreate_instances(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_recreate_instances_rest_bad_request(
    transport: str = "rest",
    request_type=compute.RecreateInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_recreate_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.recreate_instances(request)


def test_recreate_instances_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_recreate_instances_request_resource=compute.InstanceGroupManagersRecreateInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.recreate_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/recreateInstances"
            % client.transport._host,
            args[1],
        )


def test_recreate_instances_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_recreate_instances_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.RecreateInstancesInstanceGroupManagerRequest,
        dict,
    ],
)
def test_recreate_instances_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_recreate_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.recreate_instances_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_recreate_instances_unary_rest_required_fields(
    request_type=compute.RecreateInstancesInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).recreate_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).recreate_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.recreate_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_recreate_instances_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.recreate_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersRecreateInstancesRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_recreate_instances_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_recreate_instances"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_recreate_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.RecreateInstancesInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.recreate_instances_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_recreate_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.RecreateInstancesInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_recreate_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.recreate_instances_unary(request)


def test_recreate_instances_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_recreate_instances_request_resource=compute.InstanceGroupManagersRecreateInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.recreate_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/recreateInstances"
            % client.transport._host,
            args[1],
        )


def test_recreate_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.recreate_instances_unary(
            compute.RecreateInstancesInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_recreate_instances_request_resource=compute.InstanceGroupManagersRecreateInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_recreate_instances_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ResizeInstanceGroupManagerRequest,
        dict,
    ],
)
def test_resize_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.resize(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_resize_rest_required_fields(
    request_type=compute.ResizeInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["size"] = 0
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped
    assert "size" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).resize._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "size" in jsonified_request
    assert jsonified_request["size"] == request_init["size"]

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["size"] = 443
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).resize._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "size",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "size" in jsonified_request
    assert jsonified_request["size"] == 443
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.resize(request)

            expected_params = [
                (
                    "size",
                    0,
                ),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_resize_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.resize._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "size",
            )
        )
        & set(
            (
                "instanceGroupManager",
                "project",
                "size",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_resize_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_resize"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_resize"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.ResizeInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.resize(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_resize_rest_bad_request(
    transport: str = "rest", request_type=compute.ResizeInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.resize(request)


def test_resize_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            size=443,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.resize(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/resize"
            % client.transport._host,
            args[1],
        )


def test_resize_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_resize_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ResizeInstanceGroupManagerRequest,
        dict,
    ],
)
def test_resize_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.resize_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_resize_unary_rest_required_fields(
    request_type=compute.ResizeInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["size"] = 0
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped
    assert "size" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).resize._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "size" in jsonified_request
    assert jsonified_request["size"] == request_init["size"]

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["size"] = 443
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).resize._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "size",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "size" in jsonified_request
    assert jsonified_request["size"] == 443
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.resize_unary(request)

            expected_params = [
                (
                    "size",
                    0,
                ),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_resize_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.resize._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "size",
            )
        )
        & set(
            (
                "instanceGroupManager",
                "project",
                "size",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_resize_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_resize"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_resize"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.ResizeInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.resize_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_resize_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.ResizeInstanceGroupManagerRequest
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.resize_unary(request)


def test_resize_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            size=443,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.resize_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/resize"
            % client.transport._host,
            args[1],
        )


def test_resize_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resize_unary(
            compute.ResizeInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            size=443,
        )


def test_resize_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.SetInstanceTemplateInstanceGroupManagerRequest,
        dict,
    ],
)
def test_set_instance_template_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_instance_template_request_resource"] = {
        "instance_template": "instance_template_value"
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_instance_template(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_instance_template_rest_required_fields(
    request_type=compute.SetInstanceTemplateInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_instance_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_instance_template._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_instance_template(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_instance_template_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_instance_template._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersSetInstanceTemplateRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_instance_template_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_set_instance_template"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_set_instance_template"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.SetInstanceTemplateInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.set_instance_template(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_set_instance_template_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SetInstanceTemplateInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_instance_template_request_resource"] = {
        "instance_template": "instance_template_value"
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_instance_template(request)


def test_set_instance_template_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_instance_template_request_resource=compute.InstanceGroupManagersSetInstanceTemplateRequest(
                instance_template="instance_template_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.set_instance_template(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/setInstanceTemplate"
            % client.transport._host,
            args[1],
        )


def test_set_instance_template_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_set_instance_template_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.SetInstanceTemplateInstanceGroupManagerRequest,
        dict,
    ],
)
def test_set_instance_template_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_instance_template_request_resource"] = {
        "instance_template": "instance_template_value"
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_instance_template_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_set_instance_template_unary_rest_required_fields(
    request_type=compute.SetInstanceTemplateInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_instance_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_instance_template._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_instance_template_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_instance_template_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_instance_template._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersSetInstanceTemplateRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_instance_template_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_set_instance_template"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_set_instance_template"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.SetInstanceTemplateInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.set_instance_template_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_set_instance_template_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SetInstanceTemplateInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_instance_template_request_resource"] = {
        "instance_template": "instance_template_value"
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_instance_template_unary(request)


def test_set_instance_template_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_instance_template_request_resource=compute.InstanceGroupManagersSetInstanceTemplateRequest(
                instance_template="instance_template_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.set_instance_template_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/setInstanceTemplate"
            % client.transport._host,
            args[1],
        )


def test_set_instance_template_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_instance_template_unary(
            compute.SetInstanceTemplateInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_instance_template_request_resource=compute.InstanceGroupManagersSetInstanceTemplateRequest(
                instance_template="instance_template_value"
            ),
        )


def test_set_instance_template_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.SetTargetPoolsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_set_target_pools_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_target_pools_request_resource"] = {
        "fingerprint": "fingerprint_value",
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_target_pools(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_target_pools_rest_required_fields(
    request_type=compute.SetTargetPoolsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_target_pools._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_target_pools._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_target_pools(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_target_pools_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_target_pools._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersSetTargetPoolsRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_target_pools_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_set_target_pools"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_set_target_pools"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.SetTargetPoolsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.set_target_pools(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_set_target_pools_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SetTargetPoolsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_target_pools_request_resource"] = {
        "fingerprint": "fingerprint_value",
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_target_pools(request)


def test_set_target_pools_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_target_pools_request_resource=compute.InstanceGroupManagersSetTargetPoolsRequest(
                fingerprint="fingerprint_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.set_target_pools(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/setTargetPools"
            % client.transport._host,
            args[1],
        )


def test_set_target_pools_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_set_target_pools_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.SetTargetPoolsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_set_target_pools_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_target_pools_request_resource"] = {
        "fingerprint": "fingerprint_value",
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_target_pools_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_set_target_pools_unary_rest_required_fields(
    request_type=compute.SetTargetPoolsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_target_pools._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_target_pools._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_target_pools_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_target_pools_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_target_pools._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersSetTargetPoolsRequestResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_target_pools_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "post_set_target_pools"
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor, "pre_set_target_pools"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.SetTargetPoolsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.set_target_pools_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_set_target_pools_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SetTargetPoolsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_set_target_pools_request_resource"] = {
        "fingerprint": "fingerprint_value",
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_target_pools_unary(request)


def test_set_target_pools_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_target_pools_request_resource=compute.InstanceGroupManagersSetTargetPoolsRequest(
                fingerprint="fingerprint_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.set_target_pools_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/setTargetPools"
            % client.transport._host,
            args[1],
        )


def test_set_target_pools_unary_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_target_pools_unary(
            compute.SetTargetPoolsInstanceGroupManagerRequest(),
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_set_target_pools_request_resource=compute.InstanceGroupManagersSetTargetPoolsRequest(
                fingerprint="fingerprint_value"
            ),
        )


def test_set_target_pools_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_update_per_instance_configs_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_update_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_per_instance_configs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_update_per_instance_configs_rest_required_fields(
    request_type=compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_per_instance_configs(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_per_instance_configs_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersUpdatePerInstanceConfigsReqResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_per_instance_configs_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_update_per_instance_configs",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_update_per_instance_configs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.update_per_instance_configs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_per_instance_configs_rest_bad_request(
    transport: str = "rest",
    request_type=compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_update_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_per_instance_configs(request)


def test_update_per_instance_configs_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_update_per_instance_configs_req_resource=compute.InstanceGroupManagersUpdatePerInstanceConfigsReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_per_instance_configs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/updatePerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_update_per_instance_configs_rest_flattened_error(transport: str = "rest"):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_update_per_instance_configs_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
        dict,
    ],
)
def test_update_per_instance_configs_unary_rest(request_type):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_update_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_per_instance_configs_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_update_per_instance_configs_unary_rest_required_fields(
    request_type=compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
):
    transport_class = transports.InstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["zone"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["zone"] = "zone_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "zone" in jsonified_request
    assert jsonified_request["zone"] == "zone_value"

    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_per_instance_configs_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_per_instance_configs_unary_rest_unset_required_fields():
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagersUpdatePerInstanceConfigsReqResource",
                "project",
                "zone",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_per_instance_configs_unary_rest_interceptors(null_interceptor):
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.InstanceGroupManagersRestInterceptor(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "post_update_per_instance_configs",
    ) as post, mock.patch.object(
        transports.InstanceGroupManagersRestInterceptor,
        "pre_update_per_instance_configs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()

        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": None,
            "query_params": {},
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation

        client.update_per_instance_configs_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_per_instance_configs_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "zone": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_managers_update_per_instance_configs_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_per_instance_configs_unary(request)


def test_update_per_instance_configs_unary_rest_flattened():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_managers_update_per_instance_configs_req_resource=compute.InstanceGroupManagersUpdatePerInstanceConfigsReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_per_instance_configs_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/updatePerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_update_per_instance_configs_unary_rest_flattened_error(
    transport: str = "rest",
):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_per_instance_configs_unary(
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


def test_update_per_instance_configs_unary_rest_error():
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstanceGroupManagersClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.InstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = InstanceGroupManagersClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.InstanceGroupManagersRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = InstanceGroupManagersClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_instance_group_managers_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.InstanceGroupManagersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_instance_group_managers_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.instance_group_managers.transports.InstanceGroupManagersTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.InstanceGroupManagersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
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

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_instance_group_managers_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.instance_group_managers.transports.InstanceGroupManagersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.InstanceGroupManagersTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_instance_group_managers_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.instance_group_managers.transports.InstanceGroupManagersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.InstanceGroupManagersTransport()
        adc.assert_called_once()


def test_instance_group_managers_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        InstanceGroupManagersClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_instance_group_managers_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.InstanceGroupManagersRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_instance_group_managers_host_no_port(transport_name):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "compute.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://compute.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_instance_group_managers_host_with_port(transport_name):
    client = InstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "compute.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://compute.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_instance_group_managers_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = InstanceGroupManagersClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = InstanceGroupManagersClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.abandon_instances._session
    session2 = client2.transport.abandon_instances._session
    assert session1 != session2
    session1 = client1.transport.aggregated_list._session
    session2 = client2.transport.aggregated_list._session
    assert session1 != session2
    session1 = client1.transport.apply_updates_to_instances._session
    session2 = client2.transport.apply_updates_to_instances._session
    assert session1 != session2
    session1 = client1.transport.create_instances._session
    session2 = client2.transport.create_instances._session
    assert session1 != session2
    session1 = client1.transport.delete._session
    session2 = client2.transport.delete._session
    assert session1 != session2
    session1 = client1.transport.delete_instances._session
    session2 = client2.transport.delete_instances._session
    assert session1 != session2
    session1 = client1.transport.delete_per_instance_configs._session
    session2 = client2.transport.delete_per_instance_configs._session
    assert session1 != session2
    session1 = client1.transport.get._session
    session2 = client2.transport.get._session
    assert session1 != session2
    session1 = client1.transport.insert._session
    session2 = client2.transport.insert._session
    assert session1 != session2
    session1 = client1.transport.list._session
    session2 = client2.transport.list._session
    assert session1 != session2
    session1 = client1.transport.list_errors._session
    session2 = client2.transport.list_errors._session
    assert session1 != session2
    session1 = client1.transport.list_managed_instances._session
    session2 = client2.transport.list_managed_instances._session
    assert session1 != session2
    session1 = client1.transport.list_per_instance_configs._session
    session2 = client2.transport.list_per_instance_configs._session
    assert session1 != session2
    session1 = client1.transport.patch._session
    session2 = client2.transport.patch._session
    assert session1 != session2
    session1 = client1.transport.patch_per_instance_configs._session
    session2 = client2.transport.patch_per_instance_configs._session
    assert session1 != session2
    session1 = client1.transport.recreate_instances._session
    session2 = client2.transport.recreate_instances._session
    assert session1 != session2
    session1 = client1.transport.resize._session
    session2 = client2.transport.resize._session
    assert session1 != session2
    session1 = client1.transport.set_instance_template._session
    session2 = client2.transport.set_instance_template._session
    assert session1 != session2
    session1 = client1.transport.set_target_pools._session
    session2 = client2.transport.set_target_pools._session
    assert session1 != session2
    session1 = client1.transport.update_per_instance_configs._session
    session2 = client2.transport.update_per_instance_configs._session
    assert session1 != session2


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
    expected = "folders/{folder}".format(
        folder=folder,
    )
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
    expected = "organizations/{organization}".format(
        organization=organization,
    )
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
    expected = "projects/{project}".format(
        project=project,
    )
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
        project=project,
        location=location,
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


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.InstanceGroupManagersTransport, "_prep_wrapped_messages"
    ) as prep:
        client = InstanceGroupManagersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.InstanceGroupManagersTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = InstanceGroupManagersClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close():
    transports = {
        "rest": "_session",
    }

    for transport, close_name in transports.items():
        client = InstanceGroupManagersClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
    ]
    for transport in transports:
        client = InstanceGroupManagersClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (InstanceGroupManagersClient, transports.InstanceGroupManagersRestTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )
