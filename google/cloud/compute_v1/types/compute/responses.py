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
import proto  # type: ignore


__manifest__ = (
    "DeleteGlobalOperationResponse",
    "DeleteGlobalOrganizationOperationResponse",
    "DeleteRegionOperationResponse",
    "DeleteZoneOperationResponse",
    "FirewallPoliciesListAssociationsResponse",
    "InstanceGroupManagersListErrorsResponse",
    "InstanceGroupManagersListManagedInstancesResponse",
    "InstancesGetEffectiveFirewallsResponse",
    "InterconnectsGetDiagnosticsResponse",
    "LicensesListResponse",
    "NetworksGetEffectiveFirewallsResponse",
    "RegionInstanceGroupManagersListErrorsResponse",
    "RegionInstanceGroupManagersListInstancesResponse",
    "RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse",
    "RouterStatusResponse",
    "RoutersPreviewResponse",
    "SecurityPoliciesListPreconfiguredExpressionSetsResponse",
    "SendDiagnosticInterruptInstanceResponse",
    "SslPoliciesListAvailableFeaturesResponse",
    "TestPermissionsResponse",
    "UrlMapsValidateResponse",
    "VpnGatewaysGetStatusResponse",
)


class DeleteGlobalOperationResponse(proto.Message):
    r"""A response message for GlobalOperations.Delete. See the
    method description for details.

    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


class DeleteGlobalOrganizationOperationResponse(proto.Message):
    r"""A response message for GlobalOrganizationOperations.Delete.
    See the method description for details.

    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


class DeleteRegionOperationResponse(proto.Message):
    r"""A response message for RegionOperations.Delete. See the
    method description for details.

    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


class DeleteZoneOperationResponse(proto.Message):
    r"""A response message for ZoneOperations.Delete. See the method
    description for details.

    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


class FirewallPoliciesListAssociationsResponse(proto.Message):
    r"""

    Attributes:
        associations (Sequence[google.cloud.compute_v1.types.FirewallPolicyAssociation]):
            A list of associations.
        kind (str):
            [Output Only] Type of firewallPolicy associations. Always
            compute#FirewallPoliciesListAssociations for lists of
            firewallPolicy associations.

            This field is a member of `oneof`_ ``_kind``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    associations = proto.RepeatedField(
        proto.MESSAGE,
        number=508736530,
        message="FirewallPolicyAssociation",
    )
    kind = proto.Field(
        proto.STRING,
        number=3292052,
        optional=True,
    )


class InstanceGroupManagersListErrorsResponse(proto.Message):
    r"""

    Attributes:
        items (Sequence[google.cloud.compute_v1.types.InstanceManagedByIgmError]):
            [Output Only] The list of errors of the managed instance
            group.
        next_page_token (str):
            [Output Only] This token allows you to get the next page of
            results for list requests. If the number of results is
            larger than maxResults, use the nextPageToken as a value for
            the query parameter pageToken in the next list request.
            Subsequent list requests will have their own nextPageToken
            to continue paging through the results.

            This field is a member of `oneof`_ ``_next_page_token``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    items = proto.RepeatedField(
        proto.MESSAGE,
        number=100526016,
        message="InstanceManagedByIgmError",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=79797525,
        optional=True,
    )


class InstanceGroupManagersListManagedInstancesResponse(proto.Message):
    r"""

    Attributes:
        managed_instances (Sequence[google.cloud.compute_v1.types.ManagedInstance]):
            [Output Only] The list of instances in the managed instance
            group.
        next_page_token (str):
            [Output Only] This token allows you to get the next page of
            results for list requests. If the number of results is
            larger than maxResults, use the nextPageToken as a value for
            the query parameter pageToken in the next list request.
            Subsequent list requests will have their own nextPageToken
            to continue paging through the results.

            This field is a member of `oneof`_ ``_next_page_token``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    managed_instances = proto.RepeatedField(
        proto.MESSAGE,
        number=336219614,
        message="ManagedInstance",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=79797525,
        optional=True,
    )


class InstancesGetEffectiveFirewallsResponse(proto.Message):
    r"""

    Attributes:
        firewall_policys (Sequence[google.cloud.compute_v1.types.InstancesGetEffectiveFirewallsResponseEffectiveFirewallPolicy]):
            Effective firewalls from firewall policies.
        firewalls (Sequence[google.cloud.compute_v1.types.Firewall]):
            Effective firewalls on the instance.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    firewall_policys = proto.RepeatedField(
        proto.MESSAGE,
        number=410985794,
        message="InstancesGetEffectiveFirewallsResponseEffectiveFirewallPolicy",
    )
    firewalls = proto.RepeatedField(
        proto.MESSAGE,
        number=272245619,
        message="Firewall",
    )


class InterconnectsGetDiagnosticsResponse(proto.Message):
    r"""Response for the InterconnectsGetDiagnosticsRequest.

    Attributes:
        result (google.cloud.compute_v1.types.InterconnectDiagnostics):

            This field is a member of `oneof`_ ``_result``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    result = proto.Field(
        proto.MESSAGE,
        number=139315229,
        optional=True,
        message="InterconnectDiagnostics",
    )


class LicensesListResponse(proto.Message):
    r"""

    Attributes:
        id (str):
            [Output Only] Unique identifier for the resource; defined by
            the server.

            This field is a member of `oneof`_ ``_id``.
        items (Sequence[google.cloud.compute_v1.types.License]):
            A list of License resources.
        next_page_token (str):
            [Output Only] This token allows you to get the next page of
            results for list requests. If the number of results is
            larger than maxResults, use the nextPageToken as a value for
            the query parameter pageToken in the next list request.
            Subsequent list requests will have their own nextPageToken
            to continue paging through the results.

            This field is a member of `oneof`_ ``_next_page_token``.
        self_link (str):
            [Output Only] Server-defined URL for this resource.

            This field is a member of `oneof`_ ``_self_link``.
        warning (google.cloud.compute_v1.types.Warning):
            [Output Only] Informational warning message.

            This field is a member of `oneof`_ ``_warning``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    id = proto.Field(
        proto.STRING,
        number=3355,
        optional=True,
    )
    items = proto.RepeatedField(
        proto.MESSAGE,
        number=100526016,
        message="License",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=79797525,
        optional=True,
    )
    self_link = proto.Field(
        proto.STRING,
        number=456214797,
        optional=True,
    )
    warning = proto.Field(
        proto.MESSAGE,
        number=50704284,
        optional=True,
        message="Warning",
    )


class NetworksGetEffectiveFirewallsResponse(proto.Message):
    r"""

    Attributes:
        firewall_policys (Sequence[google.cloud.compute_v1.types.NetworksGetEffectiveFirewallsResponseEffectiveFirewallPolicy]):
            Effective firewalls from firewall policy.
        firewalls (Sequence[google.cloud.compute_v1.types.Firewall]):
            Effective firewalls on the network.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    firewall_policys = proto.RepeatedField(
        proto.MESSAGE,
        number=410985794,
        message="NetworksGetEffectiveFirewallsResponseEffectiveFirewallPolicy",
    )
    firewalls = proto.RepeatedField(
        proto.MESSAGE,
        number=272245619,
        message="Firewall",
    )


class RegionInstanceGroupManagersListErrorsResponse(proto.Message):
    r"""

    Attributes:
        items (Sequence[google.cloud.compute_v1.types.InstanceManagedByIgmError]):
            [Output Only] The list of errors of the managed instance
            group.
        next_page_token (str):
            [Output Only] This token allows you to get the next page of
            results for list requests. If the number of results is
            larger than maxResults, use the nextPageToken as a value for
            the query parameter pageToken in the next list request.
            Subsequent list requests will have their own nextPageToken
            to continue paging through the results.

            This field is a member of `oneof`_ ``_next_page_token``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    items = proto.RepeatedField(
        proto.MESSAGE,
        number=100526016,
        message="InstanceManagedByIgmError",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=79797525,
        optional=True,
    )


class RegionInstanceGroupManagersListInstancesResponse(proto.Message):
    r"""

    Attributes:
        managed_instances (Sequence[google.cloud.compute_v1.types.ManagedInstance]):
            A list of managed instances.
        next_page_token (str):
            [Output Only] This token allows you to get the next page of
            results for list requests. If the number of results is
            larger than maxResults, use the nextPageToken as a value for
            the query parameter pageToken in the next list request.
            Subsequent list requests will have their own nextPageToken
            to continue paging through the results.

            This field is a member of `oneof`_ ``_next_page_token``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    managed_instances = proto.RepeatedField(
        proto.MESSAGE,
        number=336219614,
        message="ManagedInstance",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=79797525,
        optional=True,
    )


class RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse(proto.Message):
    r"""

    Attributes:
        firewall_policys (Sequence[google.cloud.compute_v1.types.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponseEffectiveFirewallPolicy]):
            Effective firewalls from firewall policy.
        firewalls (Sequence[google.cloud.compute_v1.types.Firewall]):
            Effective firewalls on the network.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    firewall_policys = proto.RepeatedField(
        proto.MESSAGE,
        number=410985794,
        message="RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponseEffectiveFirewallPolicy",
    )
    firewalls = proto.RepeatedField(
        proto.MESSAGE,
        number=272245619,
        message="Firewall",
    )


class RouterStatusResponse(proto.Message):
    r"""

    Attributes:
        kind (str):
            Type of resource.

            This field is a member of `oneof`_ ``_kind``.
        result (google.cloud.compute_v1.types.RouterStatus):

            This field is a member of `oneof`_ ``_result``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    kind = proto.Field(
        proto.STRING,
        number=3292052,
        optional=True,
    )
    result = proto.Field(
        proto.MESSAGE,
        number=139315229,
        optional=True,
        message="RouterStatus",
    )


class RoutersPreviewResponse(proto.Message):
    r"""

    Attributes:
        resource (google.cloud.compute_v1.types.Router):
            Preview of given router.

            This field is a member of `oneof`_ ``_resource``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    resource = proto.Field(
        proto.MESSAGE,
        number=195806222,
        optional=True,
        message="Router",
    )


class SecurityPoliciesListPreconfiguredExpressionSetsResponse(proto.Message):
    r"""

    Attributes:
        preconfigured_expression_sets (google.cloud.compute_v1.types.SecurityPoliciesWafConfig):

            This field is a member of `oneof`_ ``_preconfigured_expression_sets``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    preconfigured_expression_sets = proto.Field(
        proto.MESSAGE,
        number=536200826,
        optional=True,
        message="SecurityPoliciesWafConfig",
    )


class SendDiagnosticInterruptInstanceResponse(proto.Message):
    r"""A response message for Instances.SendDiagnosticInterrupt. See
    the method description for details.

    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


class SslPoliciesListAvailableFeaturesResponse(proto.Message):
    r"""

    Attributes:
        features (Sequence[str]):

    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    features = proto.RepeatedField(
        proto.STRING,
        number=246211645,
    )


class TestPermissionsResponse(proto.Message):
    r"""

    Attributes:
        permissions (Sequence[str]):
            A subset of ``TestPermissionsRequest.permissions`` that the
            caller is allowed.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    permissions = proto.RepeatedField(
        proto.STRING,
        number=59962500,
    )


class UrlMapsValidateResponse(proto.Message):
    r"""

    Attributes:
        result (google.cloud.compute_v1.types.UrlMapValidationResult):

            This field is a member of `oneof`_ ``_result``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    result = proto.Field(
        proto.MESSAGE,
        number=139315229,
        optional=True,
        message="UrlMapValidationResult",
    )


class VpnGatewaysGetStatusResponse(proto.Message):
    r"""

    Attributes:
        result (google.cloud.compute_v1.types.VpnGatewayStatus):

            This field is a member of `oneof`_ ``_result``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    result = proto.Field(
        proto.MESSAGE,
        number=139315229,
        optional=True,
        message="VpnGatewayStatus",
    )


__all__ = tuple(sorted(__manifest__))
