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


from google.cloud import compute_v1


# <INGREDIENT create_disk_from_snapshot>
def create_disk_from_snapshot(project_id: str, zone: str, disk_name: str, snapshot_link: str) -> compute_v1.Disk:
    """
    Creates a new disk in a project in given zone.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone in which you want to create the disk.
        disk_name: name of the disk you want to create.
        snapshot_link: a link to the snapshot you want to use as a source for the new disk.
            This value uses the following format: "projects/{project_name}/global/snapshots/{snapshot_name}"

    Returns:
        An unattached Disk instance.
    """
    disk_client = compute_v1.DisksClient()
    disk = compute_v1.Disk()
    disk.zone = zone
    disk.source_snapshot = snapshot_link
    disk.name = disk_name
    operation = disk_client.insert_unary(project=project_id, zone=zone, disk_resource=disk)
    operation_client = compute_v1.ZoneOperationsClient()
    operation = operation_client.wait(project=project_id, zone=zone, operation=operation.name)

    if operation.error:
        print("Error during disk creation:", operation.error, file=sys.stderr)
        raise RuntimeError(operation.error)
    if operation.warnings:
        print("Warnings during disk creation:\n", "\n".join(operation.warnings), file=sys.stderr)

    return disk_client.get(project=project_id, zone=zone, disk=disk_name)
# </INGREDIENT>
