#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# flake8: noqa
"""
A sample script showing how to handle default values when communicating
with the Compute Engine API and how to configure usage reports using the API.
"""

# This file is automatically generated. Please do not modify it directly.
# Find the relevant recipe file in the samples/recipes or samples/ingredients
# directory and apply your changes there.


# [START compute_instances_verify_default_value]
# [START compute_usage_report_set]
# [START compute_usage_report_get]
# [START compute_usage_report_disable]
import sys
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


# [END compute_usage_report_disable]
# [END compute_usage_report_get]
# [END compute_usage_report_set]


# [START compute_usage_report_set]


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    This method will wait for the extended (long-running) operation to
    complete. If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
        )
        print(f"Operation ID: {operation.name}")
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr)

    return result


def set_usage_export_bucket(
    project_id: str, bucket_name: str, report_name_prefix: str = ""
) -> None:
    """
    Set Compute Engine usage export bucket for the Cloud project.
    This sample presents how to interpret the default value for the
    report name prefix parameter.

    Args:
        project_id: project ID or project number of the project to update.
        bucket_name: Google Cloud Storage bucket used to store Compute Engine
            usage reports. An existing Google Cloud Storage bucket is required.
        report_name_prefix: Prefix of the usage report name which defaults to an empty string
            to showcase default values behaviour.
    """
    usage_export_location = compute_v1.UsageExportLocation()
    usage_export_location.bucket_name = bucket_name
    usage_export_location.report_name_prefix = report_name_prefix

    if not report_name_prefix:
        # Sending an empty value for report_name_prefix results in the
        # next usage report being generated with the default prefix value
        # "usage_gce". (ref: https://cloud.google.com/compute/docs/reference/rest/v1/projects/setUsageExportBucket)
        print(
            "Setting report_name_prefix to empty value causes the report "
            "to have the default prefix of `usage_gce`."
        )

    projects_client = compute_v1.ProjectsClient()
    operation = projects_client.set_usage_export_bucket(
        project=project_id, usage_export_location_resource=usage_export_location
    )

    wait_for_extended_operation(operation, "setting GCE usage bucket")


# [END compute_usage_report_set]

# [START compute_usage_report_get]
def get_usage_export_bucket(project_id: str) -> compute_v1.UsageExportLocation:
    """
    Retrieve Compute Engine usage export bucket for the Cloud project.
    Replaces the empty value returned by the API with the default value used
    to generate report file names.

    Args:
        project_id: project ID or project number of the project to update.
    Returns:
        UsageExportLocation object describing the current usage export settings
        for project project_id.
    """
    projects_client = compute_v1.ProjectsClient()
    project_data = projects_client.get(project=project_id)

    uel = project_data.usage_export_location

    if not uel.bucket_name:
        # The usage reports are disabled.
        return uel

    if not uel.report_name_prefix:
        # Although the server sent the empty string value, the next usage report
        # generated with these settings still has the default prefix value
        # "usage_gce". (see https://cloud.google.com/compute/docs/reference/rest/v1/projects/get)
        print(
            "Report name prefix not set, replacing with default value of "
            "`usage_gce`."
        )
        uel.report_name_prefix = "usage_gce"
    return uel


# [END compute_usage_report_get]
# [END compute_instances_verify_default_value]


# [START compute_usage_report_disable]


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    This method will wait for the extended (long-running) operation to
    complete. If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
        )
        print(f"Operation ID: {operation.name}")
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr)

    return result


def disable_usage_export(project_id: str) -> None:
    """
    Disable Compute Engine usage export bucket for the Cloud Project.

    Args:
        project_id: project ID or project number of the project to update.
    """
    projects_client = compute_v1.ProjectsClient()

    # Setting `usage_export_location_resource` to an
    # empty object will disable the usage report generation.
    operation = projects_client.set_usage_export_bucket(
        project=project_id, usage_export_location_resource={}
    )

    wait_for_extended_operation(operation, "disabling GCE usage bucket")


# [END compute_usage_report_disable]
