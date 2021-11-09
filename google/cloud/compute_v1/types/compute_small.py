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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.compute.v1",
    manifest={
        "Address",
        "AddressAggregatedList",
        "AddressList",
        "AddressesScopedList",
        "AggregatedListAddressesRequest",
        "Data",
        "DeleteAddressRequest",
        "Error",
        "Errors",
        "GetRegionOperationRequest",
        "InsertAddressRequest",
        "ListAddressesRequest",
        "Operation",
        "WaitRegionOperationRequest",
        "Warning",
        "Warnings",
    },
)


class Address(proto.Message):
    r"""Messages

    Use global external addresses for GFE-based external HTTP(S) load
    balancers in Premium Tier.

    Use global internal addresses for reserved peering network range.

    Use regional external addresses for the following resources:

    -  External IP addresses for VM instances - Regional external
       forwarding rules - Cloud NAT external IP addresses - GFE based
       LBs in Standard Tier - Network LBs in Premium or Standard Tier -
       Cloud VPN gateways (both Classic and HA)

    Use regional internal IP addresses for subnet IP ranges (primary and
    secondary). This includes:

    -  Internal IP addresses for VM instances - Alias IP ranges of VM
       instances (/32 only) - Regional internal forwarding rules -
       Internal TCP/UDP load balancer addresses - Internal HTTP(S) load
       balancer addresses - Cloud DNS inbound forwarding IP addresses

    For more information, read reserved IP address.

    (== resource_for {$api_version}.addresses ==) (== resource_for
    {$api_version}.globalAddresses ==)

    Attributes:
        address (str):
            The static IP address represented by this
            resource.

            This field is a member of `oneof`_ ``_address``.
        address_type (google.cloud.compute_v1.types.Address.AddressType):
            The type of address to reserve, either
            INTERNAL or EXTERNAL. If unspecified, defaults
            to EXTERNAL.

            This field is a member of `oneof`_ ``_address_type``.
        creation_timestamp (str):
            [Output Only] Creation timestamp in RFC3339 text format.

            This field is a member of `oneof`_ ``_creation_timestamp``.
        description (str):
            An optional description of this resource.
            Provide this field when you create the resource.

            This field is a member of `oneof`_ ``_description``.
        id (int):
            [Output Only] The unique identifier for the resource. This
            identifier is defined by the server.

            This field is a member of `oneof`_ ``_id``.
        ip_version (google.cloud.compute_v1.types.Address.IpVersion):
            The IP version that will be used by this
            address. Valid options are IPV4 or IPV6. This
            can only be specified for a global address.

            This field is a member of `oneof`_ ``_ip_version``.
        kind (str):
            [Output Only] Type of the resource. Always compute#address
            for addresses.

            This field is a member of `oneof`_ ``_kind``.
        name (str):
            Name of the resource. Provided by the client when the
            resource is created. The name must be 1-63 characters long,
            and comply with RFC1035. Specifically, the name must be 1-63
            characters long and match the regular expression
            ``[a-z]([-a-z0-9]*[a-z0-9])?``. The first character must be
            a lowercase letter, and all following characters (except for
            the last character) must be a dash, lowercase letter, or
            digit. The last character must be a lowercase letter or
            digit.

            This field is a member of `oneof`_ ``_name``.
        network (str):
            The URL of the network in which to reserve the address. This
            field can only be used with INTERNAL type with the
            VPC_PEERING purpose.

            This field is a member of `oneof`_ ``_network``.
        network_tier (google.cloud.compute_v1.types.Address.NetworkTier):
            This signifies the networking tier used for
            configuring this address and can only take the
            following values: PREMIUM or STANDARD. Global
            forwarding rules can only be Premium Tier.
            Regional forwarding rules can be either Premium
            or Standard Tier. Standard Tier addresses
            applied to regional forwarding rules can be used
            with any external load balancer. Regional
            forwarding rules in Premium Tier can only be
            used with a network load balancer.  If this
            field is not specified, it is assumed to be
            PREMIUM.

            This field is a member of `oneof`_ ``_network_tier``.
        prefix_length (int):
            The prefix length if the resource reprensents
            an IP range.

            This field is a member of `oneof`_ ``_prefix_length``.
        purpose (google.cloud.compute_v1.types.Address.Purpose):
            The purpose of this resource, which can be one of the
            following values:

            -  ``GCE_ENDPOINT`` for addresses that are used by VM
               instances, alias IP ranges, internal load balancers, and
               similar resources.
            -  ``DNS_RESOLVER`` for a DNS resolver address in a
               subnetwork
            -  ``VPC_PEERING`` for addresses that are reserved for VPC
               peer networks.
            -  ``NAT_AUTO`` for addresses that are external IP addresses
               automatically reserved for Cloud NAT.

            This field is a member of `oneof`_ ``_purpose``.
        region (str):
            [Output Only] The URL of the region where the regional
            address resides. This field is not applicable to global
            addresses. You must specify this field as part of the HTTP
            request URL.

            This field is a member of `oneof`_ ``_region``.
        self_link (str):
            [Output Only] Server-defined URL for the resource.

            This field is a member of `oneof`_ ``_self_link``.
        status (google.cloud.compute_v1.types.Address.Status):
            [Output Only] The status of the address, which can be one of
            RESERVING, RESERVED, or IN_USE. An address that is RESERVING
            is currently in the process of being reserved. A RESERVED
            address is currently reserved and available to use. An
            IN_USE address is currently being used by another resource
            and is not available.

            This field is a member of `oneof`_ ``_status``.
        subnetwork (str):
            The URL of the subnetwork in which to reserve the address.
            If an IP address is specified, it must be within the
            subnetwork's IP range. This field can only be used with
            INTERNAL type with a GCE_ENDPOINT or DNS_RESOLVER purpose.

            This field is a member of `oneof`_ ``_subnetwork``.
        users (Sequence[str]):
            [Output Only] The URLs of the resources that are using this
            address.
    """

    class AddressType(proto.Enum):
        r"""The type of address to reserve, either INTERNAL or EXTERNAL.
        If unspecified, defaults to EXTERNAL.
        """
        UNDEFINED_ADDRESS_TYPE = 0
        EXTERNAL = 35607499
        INTERNAL = 279295677
        UNSPECIFIED_TYPE = 53933922

    class IpVersion(proto.Enum):
        r"""The IP version that will be used by this address. Valid
        options are IPV4 or IPV6. This can only be specified for a
        global address.
        """
        UNDEFINED_IP_VERSION = 0
        IPV4 = 2254341
        IPV6 = 2254343
        UNSPECIFIED_VERSION = 21850000

    class NetworkTier(proto.Enum):
        r"""This signifies the networking tier used for configuring this
        address and can only take the following values: PREMIUM or
        STANDARD. Global forwarding rules can only be Premium Tier.
        Regional forwarding rules can be either Premium or Standard
        Tier. Standard Tier addresses applied to regional forwarding
        rules can be used with any external load balancer. Regional
        forwarding rules in Premium Tier can only be used with a network
        load balancer.  If this field is not specified, it is assumed to
        be PREMIUM.
        """
        UNDEFINED_NETWORK_TIER = 0
        PREMIUM = 399530551
        STANDARD = 484642493

    class Purpose(proto.Enum):
        r"""The purpose of this resource, which can be one of the following
        values:

        -  ``GCE_ENDPOINT`` for addresses that are used by VM instances,
           alias IP ranges, internal load balancers, and similar resources.
        -  ``DNS_RESOLVER`` for a DNS resolver address in a subnetwork
        -  ``VPC_PEERING`` for addresses that are reserved for VPC peer
           networks.
        -  ``NAT_AUTO`` for addresses that are external IP addresses
           automatically reserved for Cloud NAT.
        """
        UNDEFINED_PURPOSE = 0
        DNS_RESOLVER = 476114556
        GCE_ENDPOINT = 230515243
        NAT_AUTO = 163666477
        VPC_PEERING = 400800170

    class Status(proto.Enum):
        r"""[Output Only] The status of the address, which can be one of
        RESERVING, RESERVED, or IN_USE. An address that is RESERVING is
        currently in the process of being reserved. A RESERVED address is
        currently reserved and available to use. An IN_USE address is
        currently being used by another resource and is not available.
        """
        UNDEFINED_STATUS = 0
        IN_USE = 17393485
        RESERVED = 432241448
        RESERVING = 514587225

    address = proto.Field(proto.STRING, number=462920692, optional=True,)
    address_type = proto.Field(
        proto.ENUM, number=264307877, optional=True, enum=AddressType,
    )
    creation_timestamp = proto.Field(proto.STRING, number=30525366, optional=True,)
    description = proto.Field(proto.STRING, number=422937596, optional=True,)
    id = proto.Field(proto.UINT64, number=3355, optional=True,)
    ip_version = proto.Field(
        proto.ENUM, number=294959552, optional=True, enum=IpVersion,
    )
    kind = proto.Field(proto.STRING, number=3292052, optional=True,)
    name = proto.Field(proto.STRING, number=3373707, optional=True,)
    network = proto.Field(proto.STRING, number=232872494, optional=True,)
    network_tier = proto.Field(
        proto.ENUM, number=517397843, optional=True, enum=NetworkTier,
    )
    prefix_length = proto.Field(proto.INT32, number=453565747, optional=True,)
    purpose = proto.Field(proto.ENUM, number=316407070, optional=True, enum=Purpose,)
    region = proto.Field(proto.STRING, number=138946292, optional=True,)
    self_link = proto.Field(proto.STRING, number=456214797, optional=True,)
    status = proto.Field(proto.ENUM, number=181260274, optional=True, enum=Status,)
    subnetwork = proto.Field(proto.STRING, number=307827694, optional=True,)
    users = proto.RepeatedField(proto.STRING, number=111578632,)


class AddressAggregatedList(proto.Message):
    r"""

    Attributes:
        id (str):
            [Output Only] Unique identifier for the resource; defined by
            the server.

            This field is a member of `oneof`_ ``_id``.
        items (Sequence[google.cloud.compute_v1.types.AddressAggregatedList.ItemsEntry]):
            A list of AddressesScopedList resources.
        kind (str):
            [Output Only] Type of resource. Always
            compute#addressAggregatedList for aggregated lists of
            addresses.

            This field is a member of `oneof`_ ``_kind``.
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

    @property
    def raw_page(self):
        return self

    id = proto.Field(proto.STRING, number=3355, optional=True,)
    items = proto.MapField(
        proto.STRING, proto.MESSAGE, number=100526016, message="AddressesScopedList",
    )
    kind = proto.Field(proto.STRING, number=3292052, optional=True,)
    next_page_token = proto.Field(proto.STRING, number=79797525, optional=True,)
    self_link = proto.Field(proto.STRING, number=456214797, optional=True,)
    warning = proto.Field(
        proto.MESSAGE, number=50704284, optional=True, message="Warning",
    )


class AddressList(proto.Message):
    r"""Contains a list of addresses.

    Attributes:
        id (str):
            [Output Only] Unique identifier for the resource; defined by
            the server.

            This field is a member of `oneof`_ ``_id``.
        items (Sequence[google.cloud.compute_v1.types.Address]):
            A list of Address resources.
        kind (str):
            [Output Only] Type of resource. Always compute#addressList
            for lists of addresses.

            This field is a member of `oneof`_ ``_kind``.
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

    @property
    def raw_page(self):
        return self

    id = proto.Field(proto.STRING, number=3355, optional=True,)
    items = proto.RepeatedField(proto.MESSAGE, number=100526016, message="Address",)
    kind = proto.Field(proto.STRING, number=3292052, optional=True,)
    next_page_token = proto.Field(proto.STRING, number=79797525, optional=True,)
    self_link = proto.Field(proto.STRING, number=456214797, optional=True,)
    warning = proto.Field(
        proto.MESSAGE, number=50704284, optional=True, message="Warning",
    )


class AddressesScopedList(proto.Message):
    r"""

    Attributes:
        addresses (Sequence[google.cloud.compute_v1.types.Address]):
            [Output Only] A list of addresses contained in this scope.
        warning (google.cloud.compute_v1.types.Warning):
            [Output Only] Informational warning which replaces the list
            of addresses when the list is empty.

            This field is a member of `oneof`_ ``_warning``.
    """

    addresses = proto.RepeatedField(proto.MESSAGE, number=337673122, message="Address",)
    warning = proto.Field(
        proto.MESSAGE, number=50704284, optional=True, message="Warning",
    )


class AggregatedListAddressesRequest(proto.Message):
    r"""A request message for Addresses.AggregatedList. See the
    method description for details.

    Attributes:
        filter (str):
            A filter expression that filters resources listed in the
            response. The expression must specify the field name, a
            comparison operator, and the value that you want to use for
            filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be either ``=``,
            ``!=``, ``>``, or ``<``.

            For example, if you are filtering Compute Engine instances,
            you can exclude instances named ``example-instance`` by
            specifying ``name != example-instance``.

            You can also filter nested fields. For example, you could
            specify ``scheduling.automaticRestart = false`` to include
            instances only if they are not scheduled for automatic
            restarts. You can use filtering on nested fields to filter
            based on resource labels.

            To filter on multiple expressions, provide each separate
            expression within parentheses. For example:
            ``(scheduling.automaticRestart = true) (cpuPlatform = "Intel Skylake")``
            By default, each expression is an ``AND`` expression.
            However, you can include ``AND`` and ``OR`` expressions
            explicitly. For example:
            ``(cpuPlatform = "Intel Skylake") OR (cpuPlatform = "Intel Broadwell") AND (scheduling.automaticRestart = true)``

            This field is a member of `oneof`_ ``_filter``.
        include_all_scopes (bool):
            Indicates whether every visible scope for
            each scope type (zone, region, global) should be
            included in the response. For new resource types
            added after this field, the flag has no effect
            as new resource types will always include every
            visible scope for each scope type in response.
            For resource types which predate this field, if
            this flag is omitted or false, only scopes of
            the scope types where the resource type is
            expected to be found will be included.

            This field is a member of `oneof`_ ``_include_all_scopes``.
        max_results (int):
            The maximum number of results per page that should be
            returned. If the number of available results is larger than
            ``maxResults``, Compute Engine returns a ``nextPageToken``
            that can be used to get the next page of results in
            subsequent list requests. Acceptable values are ``0`` to
            ``500``, inclusive. (Default: ``500``)

            This field is a member of `oneof`_ ``_max_results``.
        order_by (str):
            Sorts list results by a certain order. By default, results
            are returned in alphanumerical order based on the resource
            name.

            You can also sort results in descending order based on the
            creation timestamp using
            ``orderBy="creationTimestamp desc"``. This sorts results
            based on the ``creationTimestamp`` field in reverse
            chronological order (newest result first). Use this to sort
            resources like operations so that the newest operation is
            returned first.

            Currently, only sorting by ``name`` or
            ``creationTimestamp desc`` is supported.

            This field is a member of `oneof`_ ``_order_by``.
        page_token (str):
            Specifies a page token to use. Set ``pageToken`` to the
            ``nextPageToken`` returned by a previous list request to get
            the next page of results.

            This field is a member of `oneof`_ ``_page_token``.
        project (str):
            Project ID for this request.
    """

    filter = proto.Field(proto.STRING, number=336120696, optional=True,)
    include_all_scopes = proto.Field(proto.BOOL, number=391327988, optional=True,)
    max_results = proto.Field(proto.UINT32, number=54715419, optional=True,)
    order_by = proto.Field(proto.STRING, number=160562920, optional=True,)
    page_token = proto.Field(proto.STRING, number=19994697, optional=True,)
    project = proto.Field(proto.STRING, number=227560217,)


class Data(proto.Message):
    r"""

    Attributes:
        key (str):
            [Output Only] A key that provides more detail on the warning
            being returned. For example, for warnings where there are no
            results in a list request for a particular zone, this key
            might be scope and the key value might be the zone name.
            Other examples might be a key indicating a deprecated
            resource and a suggested replacement, or a warning about
            invalid network settings (for example, if an instance
            attempts to perform IP forwarding but is not enabled for IP
            forwarding).

            This field is a member of `oneof`_ ``_key``.
        value (str):
            [Output Only] A warning data value corresponding to the key.

            This field is a member of `oneof`_ ``_value``.
    """

    key = proto.Field(proto.STRING, number=106079, optional=True,)
    value = proto.Field(proto.STRING, number=111972721, optional=True,)


class DeleteAddressRequest(proto.Message):
    r"""A request message for Addresses.Delete. See the method
    description for details.

    Attributes:
        address (str):
            Name of the address resource to delete.
        project (str):
            Project ID for this request.
        region (str):
            Name of the region for this request.
        request_id (str):
            An optional request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed.  For example, consider a situation
            where you make an initial request and the
            request times out. If you make the request again
            with the same request ID, the server can check
            if original operation with the same request ID
            was received, and if so, will ignore the second
            request. This prevents clients from accidentally
            creating duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).

            This field is a member of `oneof`_ ``_request_id``.
    """

    address = proto.Field(proto.STRING, number=462920692,)
    project = proto.Field(proto.STRING, number=227560217,)
    region = proto.Field(proto.STRING, number=138946292,)
    request_id = proto.Field(proto.STRING, number=37109963, optional=True,)


class Error(proto.Message):
    r"""[Output Only] If errors are generated during processing of the
    operation, this field will be populated.

    Attributes:
        errors (Sequence[google.cloud.compute_v1.types.Errors]):
            [Output Only] The array of errors encountered while
            processing this operation.
    """

    errors = proto.RepeatedField(proto.MESSAGE, number=315977579, message="Errors",)


class Errors(proto.Message):
    r"""

    Attributes:
        code (str):
            [Output Only] The error type identifier for this error.

            This field is a member of `oneof`_ ``_code``.
        location (str):
            [Output Only] Indicates the field in the request that caused
            the error. This property is optional.

            This field is a member of `oneof`_ ``_location``.
        message (str):
            [Output Only] An optional, human-readable error message.

            This field is a member of `oneof`_ ``_message``.
    """

    code = proto.Field(proto.STRING, number=3059181, optional=True,)
    location = proto.Field(proto.STRING, number=290430901, optional=True,)
    message = proto.Field(proto.STRING, number=418054151, optional=True,)


class GetRegionOperationRequest(proto.Message):
    r"""A request message for RegionOperations.Get. See the method
    description for details.

    Attributes:
        operation (str):
            Name of the Operations resource to return.
        project (str):
            Project ID for this request.
        region (str):
            Name of the region for this request.
    """

    operation = proto.Field(proto.STRING, number=52090215,)
    project = proto.Field(proto.STRING, number=227560217,)
    region = proto.Field(proto.STRING, number=138946292,)


class InsertAddressRequest(proto.Message):
    r"""A request message for Addresses.Insert. See the method
    description for details.

    Attributes:
        address_resource (google.cloud.compute_v1.types.Address):
            The body resource for this request
        project (str):
            Project ID for this request.
        region (str):
            Name of the region for this request.
        request_id (str):
            An optional request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed.  For example, consider a situation
            where you make an initial request and the
            request times out. If you make the request again
            with the same request ID, the server can check
            if original operation with the same request ID
            was received, and if so, will ignore the second
            request. This prevents clients from accidentally
            creating duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).

            This field is a member of `oneof`_ ``_request_id``.
    """

    address_resource = proto.Field(proto.MESSAGE, number=483888121, message="Address",)
    project = proto.Field(proto.STRING, number=227560217,)
    region = proto.Field(proto.STRING, number=138946292,)
    request_id = proto.Field(proto.STRING, number=37109963, optional=True,)


class ListAddressesRequest(proto.Message):
    r"""A request message for Addresses.List. See the method
    description for details.

    Attributes:
        filter (str):
            A filter expression that filters resources
            listed in the response. The expression must
            specify the field name, a comparison operator,
            and the value that you want to use for
            filtering. The value must be a string, a number,
            or a boolean. The comparison operator must be
            either =, !=, >, or <.  For example, if you are
            filtering Compute Engine instances, you can
            exclude instances named example-instance by
            specifying name != example-instance.
            You can also filter nested fields. For example,
            you could specify scheduling.automaticRestart =
            false to include instances only if they are not
            scheduled for automatic restarts. You can use
            filtering on nested fields to filter based on
            resource labels.
            To filter on multiple expressions, provide each
            separate expression within parentheses. For
            example, (scheduling.automaticRestart = true)
            (cpuPlatform = "Intel Skylake"). By default,
            each expression is an AND expression. However,
            you can include AND and OR expressions
            explicitly. For example, (cpuPlatform = "Intel
            Skylake") OR (cpuPlatform = "Intel Broadwell")
            AND (scheduling.automaticRestart = true).

            This field is a member of `oneof`_ ``_filter``.
        max_results (int):
            The maximum number of results per page that
            should be returned. If the number of available
            results is larger than maxResults, Compute
            Engine returns a nextPageToken that can be used
            to get the next page of results in subsequent
            list requests. Acceptable values are 0 to 500,
            inclusive. (Default: 500)

            This field is a member of `oneof`_ ``_max_results``.
        order_by (str):
            Sorts list results by a certain order. By
            default, results are returned in alphanumerical
            order based on the resource name.  You can also
            sort results in descending order based on the
            creation timestamp using
            orderBy="creationTimestamp desc". This sorts
            results based on the creationTimestamp field in
            reverse chronological order (newest result
            first). Use this to sort resources like
            operations so that the newest operation is
            returned first.
            Currently, only sorting by name or
            creationTimestamp desc is supported.
        page_token (str):
            Specifies a page token to use. Set pageToken
            to the nextPageToken returned by a previous list
            request to get the next page of results.

            This field is a member of `oneof`_ ``_page_token``.
        project (str):
            Project ID for this request.
        region (str):
            Name of the region for this request.
    """

    filter = proto.Field(proto.STRING, number=336120696, optional=True,)
    max_results = proto.Field(proto.UINT32, number=54715419, optional=True,)
    order_by = proto.Field(proto.STRING, number=160562920,)
    page_token = proto.Field(proto.STRING, number=19994697, optional=True,)
    project = proto.Field(proto.STRING, number=227560217,)
    region = proto.Field(proto.STRING, number=138946292,)


class Operation(proto.Message):
    r"""Represents an Operation resource.

    Google Compute Engine has three Operation resources:

    -  `Global </compute/docs/reference/rest/{$api_version}/globalOperations>`__
       \*
       `Regional </compute/docs/reference/rest/{$api_version}/regionOperations>`__
       \*
       `Zonal </compute/docs/reference/rest/{$api_version}/zoneOperations>`__

    You can use an operation resource to manage asynchronous API
    requests. For more information, read Handling API responses.

    Operations can be global, regional or zonal.

    -  For global operations, use the globalOperations resource.
    -  For regional operations, use the regionOperations resource.
    -  For zonal operations, use the zoneOperations resource.

    For more information, read Global, Regional, and Zonal Resources.
    (== resource_for {$api_version}.globalOperations ==) (==
    resource_for {$api_version}.regionOperations ==) (== resource_for
    {$api_version}.zoneOperations ==)

    Attributes:
        client_operation_id (str):
            [Output Only] The value of ``requestId`` if you provided it
            in the request. Not present otherwise.

            This field is a member of `oneof`_ ``_client_operation_id``.
        creation_timestamp (str):
            [Deprecated] This field is deprecated.

            This field is a member of `oneof`_ ``_creation_timestamp``.
        description (str):
            [Output Only] A textual description of the operation, which
            is set when the operation is created.

            This field is a member of `oneof`_ ``_description``.
        end_time (str):
            [Output Only] The time that this operation was completed.
            This value is in RFC3339 text format.

            This field is a member of `oneof`_ ``_end_time``.
        error (google.cloud.compute_v1.types.Error):
            [Output Only] If errors are generated during processing of
            the operation, this field will be populated.

            This field is a member of `oneof`_ ``_error``.
        http_error_message (str):
            [Output Only] If the operation fails, this field contains
            the HTTP error message that was returned, such as NOT FOUND.

            This field is a member of `oneof`_ ``_http_error_message``.
        http_error_status_code (int):
            [Output Only] If the operation fails, this field contains
            the HTTP error status code that was returned. For example, a
            404 means the resource was not found.

            This field is a member of `oneof`_ ``_http_error_status_code``.
        id (int):
            [Output Only] The unique identifier for the operation. This
            identifier is defined by the server.

            This field is a member of `oneof`_ ``_id``.
        insert_time (str):
            [Output Only] The time that this operation was requested.
            This value is in RFC3339 text format.

            This field is a member of `oneof`_ ``_insert_time``.
        kind (str):
            [Output Only] Type of the resource. Always compute#operation
            for Operation resources.

            This field is a member of `oneof`_ ``_kind``.
        name (str):
            [Output Only] Name of the operation.

            This field is a member of `oneof`_ ``_name``.
        operation_type (str):
            [Output Only] The type of operation, such as insert, update,
            or delete, and so on.

            This field is a member of `oneof`_ ``_operation_type``.
        progress (int):
            [Output Only] An optional progress indicator that ranges
            from 0 to 100. There is no requirement that this be linear
            or support any granularity of operations. This should not be
            used to guess when the operation will be complete. This
            number should monotonically increase as the operation
            progresses.

            This field is a member of `oneof`_ ``_progress``.
        region (str):
            [Output Only] The URL of the region where the operation
            resides. Only applicable when performing regional
            operations.

            This field is a member of `oneof`_ ``_region``.
        self_link (str):
            [Output Only] Server-defined URL for the resource.

            This field is a member of `oneof`_ ``_self_link``.
        start_time (str):
            [Output Only] The time that this operation was started by
            the server. This value is in RFC3339 text format.

            This field is a member of `oneof`_ ``_start_time``.
        status (google.cloud.compute_v1.types.Operation.Status):
            [Output Only] The status of the operation, which can be one
            of the following: PENDING, RUNNING, or DONE.

            This field is a member of `oneof`_ ``_status``.
        status_message (str):
            [Output Only] An optional textual description of the current
            status of the operation.

            This field is a member of `oneof`_ ``_status_message``.
        target_id (int):
            [Output Only] The unique target ID, which identifies a
            specific incarnation of the target resource.

            This field is a member of `oneof`_ ``_target_id``.
        target_link (str):
            [Output Only] The URL of the resource that the operation
            modifies. For operations related to creating a snapshot,
            this points to the persistent disk that the snapshot was
            created from.

            This field is a member of `oneof`_ ``_target_link``.
        user (str):
            [Output Only] User who requested the operation, for example:
            user@example.com.

            This field is a member of `oneof`_ ``_user``.
        warnings (Sequence[google.cloud.compute_v1.types.Warnings]):
            [Output Only] If warning messages are generated during
            processing of the operation, this field will be populated.
        zone (str):
            [Output Only] The URL of the zone where the operation
            resides. Only applicable when performing per-zone
            operations.

            This field is a member of `oneof`_ ``_zone``.
    """

    class Status(proto.Enum):
        r"""[Output Only] The status of the operation, which can be one of the
        following: PENDING, RUNNING, or DONE.
        """
        UNDEFINED_STATUS = 0
        DONE = 2104194
        PENDING = 35394935
        RUNNING = 121282975

    client_operation_id = proto.Field(proto.STRING, number=297240295, optional=True,)
    creation_timestamp = proto.Field(proto.STRING, number=30525366, optional=True,)
    description = proto.Field(proto.STRING, number=422937596, optional=True,)
    end_time = proto.Field(proto.STRING, number=114938801, optional=True,)
    error = proto.Field(proto.MESSAGE, number=96784904, optional=True, message="Error",)
    http_error_message = proto.Field(proto.STRING, number=202521945, optional=True,)
    http_error_status_code = proto.Field(proto.INT32, number=312345196, optional=True,)
    id = proto.Field(proto.UINT64, number=3355, optional=True,)
    insert_time = proto.Field(proto.STRING, number=433722515, optional=True,)
    kind = proto.Field(proto.STRING, number=3292052, optional=True,)
    name = proto.Field(proto.STRING, number=3373707, optional=True,)
    operation_type = proto.Field(proto.STRING, number=177650450, optional=True,)
    progress = proto.Field(proto.INT32, number=72663597, optional=True,)
    region = proto.Field(proto.STRING, number=138946292, optional=True,)
    self_link = proto.Field(proto.STRING, number=456214797, optional=True,)
    start_time = proto.Field(proto.STRING, number=37467274, optional=True,)
    status = proto.Field(proto.ENUM, number=181260274, optional=True, enum=Status,)
    status_message = proto.Field(proto.STRING, number=297428154, optional=True,)
    target_id = proto.Field(proto.UINT64, number=258165385, optional=True,)
    target_link = proto.Field(proto.STRING, number=62671336, optional=True,)
    user = proto.Field(proto.STRING, number=3599307, optional=True,)
    warnings = proto.RepeatedField(proto.MESSAGE, number=498091095, message="Warnings",)
    zone = proto.Field(proto.STRING, number=3744684, optional=True,)


class WaitRegionOperationRequest(proto.Message):
    r"""A request message for RegionOperations.Wait. See the method
    description for details.

    Attributes:
        operation (str):
            Name of the Operations resource to return.
        project (str):
            Project ID for this request.
        region (str):
            Name of the region for this request.
    """

    operation = proto.Field(proto.STRING, number=52090215,)
    project = proto.Field(proto.STRING, number=227560217,)
    region = proto.Field(proto.STRING, number=138946292,)


class Warning(proto.Message):
    r"""[Output Only] Informational warning message.

    Attributes:
        code (google.cloud.compute_v1.types.Warning.Code):
            [Output Only] A warning code, if applicable. For example,
            Compute Engine returns NO_RESULTS_ON_PAGE if there are no
            results in the response.

            This field is a member of `oneof`_ ``_code``.
        data (Sequence[google.cloud.compute_v1.types.Data]):
            [Output Only] Metadata about this warning in key: value
            format. For example: "data": [ { "key": "scope", "value":
            "zones/us-east1-d" }
        message (str):
            [Output Only] A human-readable description of the warning
            code.

            This field is a member of `oneof`_ ``_message``.
    """

    class Code(proto.Enum):
        r"""[Output Only] A warning code, if applicable. For example, Compute
        Engine returns NO_RESULTS_ON_PAGE if there are no results in the
        response.
        """
        UNDEFINED_CODE = 0
        CLEANUP_FAILED = 150308440
        DEPRECATED_RESOURCE_USED = 391835586
        DEPRECATED_TYPE_USED = 346526230
        DISK_SIZE_LARGER_THAN_IMAGE_SIZE = 369442967
        EXPERIMENTAL_TYPE_USED = 451954443
        EXTERNAL_API_WARNING = 175546307
        FIELD_VALUE_OVERRIDEN = 329669423
        INJECTED_KERNELS_DEPRECATED = 417377419
        MISSING_TYPE_DEPENDENCY = 344505463
        NEXT_HOP_ADDRESS_NOT_ASSIGNED = 324964999
        NEXT_HOP_CANNOT_IP_FORWARD = 383382887
        NEXT_HOP_INSTANCE_NOT_FOUND = 464250446
        NEXT_HOP_INSTANCE_NOT_ON_NETWORK = 243758146
        NEXT_HOP_NOT_RUNNING = 417081265
        NOT_CRITICAL_ERROR = 105763924
        NO_RESULTS_ON_PAGE = 30036744
        REQUIRED_TOS_AGREEMENT = 3745539
        RESOURCE_IN_USE_BY_OTHER_RESOURCE_WARNING = 496728641
        RESOURCE_NOT_DELETED = 168598460
        SCHEMA_VALIDATION_IGNORED = 275245642
        SINGLE_INSTANCE_PROPERTY_TEMPLATE = 268305617
        UNDECLARED_PROPERTIES = 390513439
        UNREACHABLE = 13328052

    code = proto.Field(proto.ENUM, number=3059181, optional=True, enum=Code,)
    data = proto.RepeatedField(proto.MESSAGE, number=3076010, message="Data",)
    message = proto.Field(proto.STRING, number=418054151, optional=True,)


class Warnings(proto.Message):
    r"""

    Attributes:
        code (google.cloud.compute_v1.types.Warnings.Code):
            [Output Only] A warning code, if applicable. For example,
            Compute Engine returns NO_RESULTS_ON_PAGE if there are no
            results in the response.

            This field is a member of `oneof`_ ``_code``.
        data (Sequence[google.cloud.compute_v1.types.Data]):
            [Output Only] Metadata about this warning in key: value
            format. For example: "data": [ { "key": "scope", "value":
            "zones/us-east1-d" }
        message (str):
            [Output Only] A human-readable description of the warning
            code.

            This field is a member of `oneof`_ ``_message``.
    """

    class Code(proto.Enum):
        r"""[Output Only] A warning code, if applicable. For example, Compute
        Engine returns NO_RESULTS_ON_PAGE if there are no results in the
        response.
        """
        UNDEFINED_CODE = 0
        CLEANUP_FAILED = 150308440
        DEPRECATED_RESOURCE_USED = 391835586
        DEPRECATED_TYPE_USED = 346526230
        DISK_SIZE_LARGER_THAN_IMAGE_SIZE = 369442967
        EXPERIMENTAL_TYPE_USED = 451954443
        EXTERNAL_API_WARNING = 175546307
        FIELD_VALUE_OVERRIDEN = 329669423
        INJECTED_KERNELS_DEPRECATED = 417377419
        MISSING_TYPE_DEPENDENCY = 344505463
        NEXT_HOP_ADDRESS_NOT_ASSIGNED = 324964999
        NEXT_HOP_CANNOT_IP_FORWARD = 383382887
        NEXT_HOP_INSTANCE_NOT_FOUND = 464250446
        NEXT_HOP_INSTANCE_NOT_ON_NETWORK = 243758146
        NEXT_HOP_NOT_RUNNING = 417081265
        NOT_CRITICAL_ERROR = 105763924
        NO_RESULTS_ON_PAGE = 30036744
        REQUIRED_TOS_AGREEMENT = 3745539
        RESOURCE_IN_USE_BY_OTHER_RESOURCE_WARNING = 496728641
        RESOURCE_NOT_DELETED = 168598460
        SCHEMA_VALIDATION_IGNORED = 275245642
        SINGLE_INSTANCE_PROPERTY_TEMPLATE = 268305617
        UNDECLARED_PROPERTIES = 390513439
        UNREACHABLE = 13328052

    code = proto.Field(proto.ENUM, number=3059181, optional=True, enum=Code,)
    data = proto.RepeatedField(proto.MESSAGE, number=3076010, message="Data",)
    message = proto.Field(proto.STRING, number=418054151, optional=True,)


__all__ = tuple(sorted(__protobuf__.manifest))
