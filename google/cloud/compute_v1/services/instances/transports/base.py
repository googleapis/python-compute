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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources

from google import auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.compute_v1.types import compute

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-compute",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None

_API_CORE_VERSION = google.api_core.__version__


class InstancesTransport(abc.ABC):
    """Abstract transport class for Instances."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/compute",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    DEFAULT_HOST: str = "compute.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
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
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): These two class methods are in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-api-core
    # and google-auth are increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

    # TODO: Remove this function once google-api-core >= 1.26.0 is required
    @classmethod
    def _get_self_signed_jwt_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Union[Optional[Sequence[str]], str]]:
        """Returns kwargs to pass to grpc_helpers.create_channel depending on the google-api-core version"""

        self_signed_jwt_kwargs: Dict[str, Union[Optional[Sequence[str]], str]] = {}

        if _API_CORE_VERSION and (
            packaging.version.parse(_API_CORE_VERSION)
            >= packaging.version.parse("1.26.0")
        ):
            self_signed_jwt_kwargs["default_scopes"] = cls.AUTH_SCOPES
            self_signed_jwt_kwargs["scopes"] = scopes
            self_signed_jwt_kwargs["default_host"] = cls.DEFAULT_HOST
        else:
            self_signed_jwt_kwargs["scopes"] = scopes or cls.AUTH_SCOPES

        return self_signed_jwt_kwargs

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.add_access_config: gapic_v1.method.wrap_method(
                self.add_access_config, default_timeout=None, client_info=client_info,
            ),
            self.add_resource_policies: gapic_v1.method.wrap_method(
                self.add_resource_policies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.aggregated_list: gapic_v1.method.wrap_method(
                self.aggregated_list, default_timeout=None, client_info=client_info,
            ),
            self.attach_disk: gapic_v1.method.wrap_method(
                self.attach_disk, default_timeout=None, client_info=client_info,
            ),
            self.delete: gapic_v1.method.wrap_method(
                self.delete, default_timeout=None, client_info=client_info,
            ),
            self.delete_access_config: gapic_v1.method.wrap_method(
                self.delete_access_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.detach_disk: gapic_v1.method.wrap_method(
                self.detach_disk, default_timeout=None, client_info=client_info,
            ),
            self.get: gapic_v1.method.wrap_method(
                self.get, default_timeout=None, client_info=client_info,
            ),
            self.get_guest_attributes: gapic_v1.method.wrap_method(
                self.get_guest_attributes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.get_screenshot: gapic_v1.method.wrap_method(
                self.get_screenshot, default_timeout=None, client_info=client_info,
            ),
            self.get_serial_port_output: gapic_v1.method.wrap_method(
                self.get_serial_port_output,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_shielded_instance_identity: gapic_v1.method.wrap_method(
                self.get_shielded_instance_identity,
                default_timeout=None,
                client_info=client_info,
            ),
            self.insert: gapic_v1.method.wrap_method(
                self.insert, default_timeout=None, client_info=client_info,
            ),
            self.list: gapic_v1.method.wrap_method(
                self.list, default_timeout=None, client_info=client_info,
            ),
            self.list_referrers: gapic_v1.method.wrap_method(
                self.list_referrers, default_timeout=None, client_info=client_info,
            ),
            self.remove_resource_policies: gapic_v1.method.wrap_method(
                self.remove_resource_policies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.reset: gapic_v1.method.wrap_method(
                self.reset, default_timeout=None, client_info=client_info,
            ),
            self.set_deletion_protection: gapic_v1.method.wrap_method(
                self.set_deletion_protection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_disk_auto_delete: gapic_v1.method.wrap_method(
                self.set_disk_auto_delete,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.set_labels: gapic_v1.method.wrap_method(
                self.set_labels, default_timeout=None, client_info=client_info,
            ),
            self.set_machine_resources: gapic_v1.method.wrap_method(
                self.set_machine_resources,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_machine_type: gapic_v1.method.wrap_method(
                self.set_machine_type, default_timeout=None, client_info=client_info,
            ),
            self.set_metadata: gapic_v1.method.wrap_method(
                self.set_metadata, default_timeout=None, client_info=client_info,
            ),
            self.set_min_cpu_platform: gapic_v1.method.wrap_method(
                self.set_min_cpu_platform,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_scheduling: gapic_v1.method.wrap_method(
                self.set_scheduling, default_timeout=None, client_info=client_info,
            ),
            self.set_service_account: gapic_v1.method.wrap_method(
                self.set_service_account, default_timeout=None, client_info=client_info,
            ),
            self.set_shielded_instance_integrity_policy: gapic_v1.method.wrap_method(
                self.set_shielded_instance_integrity_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_tags: gapic_v1.method.wrap_method(
                self.set_tags, default_timeout=None, client_info=client_info,
            ),
            self.simulate_maintenance_event: gapic_v1.method.wrap_method(
                self.simulate_maintenance_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.start: gapic_v1.method.wrap_method(
                self.start, default_timeout=None, client_info=client_info,
            ),
            self.start_with_encryption_key: gapic_v1.method.wrap_method(
                self.start_with_encryption_key,
                default_timeout=None,
                client_info=client_info,
            ),
            self.stop: gapic_v1.method.wrap_method(
                self.stop, default_timeout=None, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update: gapic_v1.method.wrap_method(
                self.update, default_timeout=None, client_info=client_info,
            ),
            self.update_access_config: gapic_v1.method.wrap_method(
                self.update_access_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_display_device: gapic_v1.method.wrap_method(
                self.update_display_device,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_network_interface: gapic_v1.method.wrap_method(
                self.update_network_interface,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_shielded_instance_config: gapic_v1.method.wrap_method(
                self.update_shielded_instance_config,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def add_access_config(
        self,
    ) -> Callable[
        [compute.AddAccessConfigInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def add_resource_policies(
        self,
    ) -> Callable[
        [compute.AddResourcePoliciesInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListInstancesRequest],
        Union[
            compute.InstanceAggregatedList, Awaitable[compute.InstanceAggregatedList]
        ],
    ]:
        raise NotImplementedError()

    @property
    def attach_disk(
        self,
    ) -> Callable[
        [compute.AttachDiskInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete(
        self,
    ) -> Callable[
        [compute.DeleteInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_access_config(
        self,
    ) -> Callable[
        [compute.DeleteAccessConfigInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def detach_disk(
        self,
    ) -> Callable[
        [compute.DetachDiskInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetInstanceRequest],
        Union[compute.Instance, Awaitable[compute.Instance]],
    ]:
        raise NotImplementedError()

    @property
    def get_guest_attributes(
        self,
    ) -> Callable[
        [compute.GetGuestAttributesInstanceRequest],
        Union[compute.GuestAttributes, Awaitable[compute.GuestAttributes]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [compute.GetIamPolicyInstanceRequest],
        Union[compute.Policy, Awaitable[compute.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_screenshot(
        self,
    ) -> Callable[
        [compute.GetScreenshotInstanceRequest],
        Union[compute.Screenshot, Awaitable[compute.Screenshot]],
    ]:
        raise NotImplementedError()

    @property
    def get_serial_port_output(
        self,
    ) -> Callable[
        [compute.GetSerialPortOutputInstanceRequest],
        Union[compute.SerialPortOutput, Awaitable[compute.SerialPortOutput]],
    ]:
        raise NotImplementedError()

    @property
    def get_shielded_instance_identity(
        self,
    ) -> Callable[
        [compute.GetShieldedInstanceIdentityInstanceRequest],
        Union[
            compute.ShieldedInstanceIdentity,
            Awaitable[compute.ShieldedInstanceIdentity],
        ],
    ]:
        raise NotImplementedError()

    @property
    def insert(
        self,
    ) -> Callable[
        [compute.InsertInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListInstancesRequest],
        Union[compute.InstanceList, Awaitable[compute.InstanceList]],
    ]:
        raise NotImplementedError()

    @property
    def list_referrers(
        self,
    ) -> Callable[
        [compute.ListReferrersInstancesRequest],
        Union[compute.InstanceListReferrers, Awaitable[compute.InstanceListReferrers]],
    ]:
        raise NotImplementedError()

    @property
    def remove_resource_policies(
        self,
    ) -> Callable[
        [compute.RemoveResourcePoliciesInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def reset(
        self,
    ) -> Callable[
        [compute.ResetInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_deletion_protection(
        self,
    ) -> Callable[
        [compute.SetDeletionProtectionInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_disk_auto_delete(
        self,
    ) -> Callable[
        [compute.SetDiskAutoDeleteInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [compute.SetIamPolicyInstanceRequest],
        Union[compute.Policy, Awaitable[compute.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def set_labels(
        self,
    ) -> Callable[
        [compute.SetLabelsInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_machine_resources(
        self,
    ) -> Callable[
        [compute.SetMachineResourcesInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_machine_type(
        self,
    ) -> Callable[
        [compute.SetMachineTypeInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_metadata(
        self,
    ) -> Callable[
        [compute.SetMetadataInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_min_cpu_platform(
        self,
    ) -> Callable[
        [compute.SetMinCpuPlatformInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_scheduling(
        self,
    ) -> Callable[
        [compute.SetSchedulingInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_service_account(
        self,
    ) -> Callable[
        [compute.SetServiceAccountInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_shielded_instance_integrity_policy(
        self,
    ) -> Callable[
        [compute.SetShieldedInstanceIntegrityPolicyInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_tags(
        self,
    ) -> Callable[
        [compute.SetTagsInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def simulate_maintenance_event(
        self,
    ) -> Callable[
        [compute.SimulateMaintenanceEventInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start(
        self,
    ) -> Callable[
        [compute.StartInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_with_encryption_key(
        self,
    ) -> Callable[
        [compute.StartWithEncryptionKeyInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop(
        self,
    ) -> Callable[
        [compute.StopInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsInstanceRequest],
        Union[
            compute.TestPermissionsResponse, Awaitable[compute.TestPermissionsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update(
        self,
    ) -> Callable[
        [compute.UpdateInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_access_config(
        self,
    ) -> Callable[
        [compute.UpdateAccessConfigInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_display_device(
        self,
    ) -> Callable[
        [compute.UpdateDisplayDeviceInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_network_interface(
        self,
    ) -> Callable[
        [compute.UpdateNetworkInterfaceInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_shielded_instance_config(
        self,
    ) -> Callable[
        [compute.UpdateShieldedInstanceConfigInstanceRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("InstancesTransport",)
