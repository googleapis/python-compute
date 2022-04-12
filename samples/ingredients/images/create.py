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
import time

from google.cloud import compute_v1
import warnings

STOPPED_MACHINE_STATUS = (
    compute_v1.Instance.Status.TERMINATED.name,
    compute_v1.Instance.Status.STOPPED.name
)


def create_image(project_id: str, zone: str, source_disk_name: str, image_name: str, storage_location: str, force_create: bool=False) -> compute_v1.Image:
    """

    """
    image_client = compute_v1.ImagesClient()
    disk_client = compute_v1.DisksClient()
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.GlobalOperationsClient()

    # Get source disk
    disk = disk_client.get(project=project_id, zone=zone, disk=source_disk_name)

    for disk_user in disk.users:
        instance = instance_client.get(project=project_id, zone=zone, instance=disk_user)
        if instance.status in STOPPED_MACHINE_STATUS:
            continue
        if not force_create:
            raise RuntimeError(f"Instance {disk_user} should be stopped. Please stop the instance using "
                               f"GCESysprep command or set forceCreate parameter to true (not recommended). "
                               f"More information here: https://cloud.google.com/compute/docs/instances/windows/creating-windows-os-image#api.")
        else:
            warnings.warn(f"Warning: force_create option compromise the integrity of your image. "
                          f"Stop the {disk_user} instance before you create the image if possible.")

    # Create image
    image = compute_v1.Image()
    image.source_disk = disk.self_link
    image.name = image_name
    image.storage_locations = [storage_location]

    operation = image_client.insert_unary(project=project_id, image_resource=image)
    start = time.time()
    while operation.status != compute_v1.Operation.Status.DONE:
        operation = operation_client.wait(
            operation=operation.name, project=project_id
        )
        if time.time() - start >= 300:  # 5 minutes
            raise TimeoutError()