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

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa
import sys
from typing import Literal

from google.cloud import compute_v1


# <INGREDIENT create_disk_from_image>
def create_disk_from_image(
    project_id: str, zone: str, disk_name: str, disk_type: str, disk_size_gb: int, source_image: str
) -> compute_v1.Disk:
    """
    Creates a new disk in a project in given zone using an image as base.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone in which you want to create the disk.
        disk_name: name of the disk you want to create.
        disk_type: the type of disk you want to create. This value uses the following format:
            "zones/{zone}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "zones/us-west3-b/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes
        source_image: source image to use when creating this disk. You must have read access to this disk. This
            can be one of the publicly available images or an image from one of your projects.
            This value uses the following format: "projects/{project_name}/global/images/{image_name}"

    Returns:
        An unattached Disk instance.
    """
    disk = compute_v1.Disk()
    disk.size_gb = disk_size_gb
    disk.name = disk_name
    disk.zone = zone
    disk.type_ = disk_type
    disk.source_image = source_image

    disk_client = compute_v1.DisksClient()
    operation = disk_client.insert_unary(project=project_id, zone=zone, disk_resource=disk)
    operation_client = compute_v1.ZoneOperationsClient()
    operation = operation_client.wait(project=project_id, zone=zone, operation=operation.name)

    if operation.error:
        print("Error during disk creation:", operation.error, file=sys.stderr)
        raise RuntimeError(operation.error)
    if operation.warnings:
        print("Warnings during disk creation:\n", file=sys.stderr)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr)

    return disk_client.get(project=project_id, zone=zone, disk=disk.name)
# </INGREDIENT>
