# Copyright 2021 Google LLC
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

import sys
from typing import List

# [START compute_instances_create_with_subnet]
# [START compute_instances_create_from_image_plus_snapshot_disk]
# [START compute_instances_create_from_snapshot]
# [START compute_instances_create_from_image_plus_empty_disk]
# [START compute_instances_create_from_custom_image]
# [START compute_instances_create_from_image ]
from google.cloud import compute_v1


# [END compute_instances_create_from_image ]
# [END compute_instances_create_from_custom_image]
# [END compute_instances_create_from_image_plus_empty_disk]
# [END compute_instances_create_from_snapshot]
# [END compute_instances_create_from_image_plus_snapshot_disk]
# [END compute_instances_create_with_subnet]


# [START compute_instances_create_with_subnet]
# [START compute_instances_create_from_image_plus_snapshot_disk]
# [START compute_instances_create_from_image_plus_empty_disk]
# [START compute_instances_create_from_custom_image]
# [START compute_instances_create_from_image]
def disk_from_image(
    disk_type: str, disk_size_gb: int, boot: bool, source_image: str
) -> compute_v1.AttachedDisk:
    """
    Create an AttachedDisk object to be used in VM instance creation. Uses an Image as the
    source for the new disk.

    Args:
         disk_type: the type of disk you want to create. The value uses following format:
            "zones/{zone}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "zones/us-west3-b/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes
        boot: flag indicating if this disk should be used as a boot disk of an instance
        source_image: a link pointing to an image you have read access to. This can be one
            of the publicly available images or an image from one of your projects.
            This value uses following format: "projects/{project_name}/global/images/{image_name}"

    Returns:
        AttachedDisk object configured to be created as a copy of specified image.
    """
    boot_disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()

    initialize_params.source_image = source_image

    initialize_params.disk_size_gb = disk_size_gb
    initialize_params.disk_type = disk_type
    boot_disk.initialize_params = initialize_params
    boot_disk.auto_delete = True
    boot_disk.boot = boot
    return boot_disk


# [END compute_instances_create_from_image]
# [END compute_instances_create_from_custom_image]
# [END compute_instances_create_from_image_plus_empty_disk]
# [END compute_instances_create_from_image_plus_snapshot_disk]
# [END compute_instances_create_with_subnet]


# [START compute_instances_create_from_image_plus_empty_disk]
def empty_disk(disk_type: str, disk_size_gb: int) -> compute_v1.AttachedDisk():
    """
    Create an AttachedDisk object to be used in VM instance creation. The created disk will be
    empty and will require formatting before it can be used.

    Args:
         disk_type: the type of disk you want to create. The value uses following format:
            "zones/{zone}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "zones/us-west3-b/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes

    Returns:
        AttachedDisk object configured to be created as an empty disk.
    """
    disk = compute_v1.AttachedDisk()
    init_params = compute_v1.AttachedDiskInitializeParams()
    init_params.disk_type = disk_type
    init_params.disk_size_gb = disk_size_gb
    disk.initialize_params = init_params
    disk.auto_delete = True
    disk.boot = False
    return disk


# [END compute_instances_create_from_image_plus_empty_disk]


# [START compute_instances_create_from_image_plus_snapshot_disk]
# [START compute_instances_create_from_snapshot]
def disk_from_snapshot(
    disk_type: str, disk_size_gb: int, boot: bool, snapshot_url: str
) -> compute_v1.AttachedDisk():
    """
    Create an AttachedDisk object to be used in VM instance creation. Uses an Image as the
    source for the new disk.

    Args:
         disk_type: the type of disk you want to create. The value uses following format:
            "zones/{zone}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "zones/us-west3-b/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes
        boot: flag indicating if this disk should be used as a boot disk of an instance
        snapshot_url: a link pointing to a snapshot you have read access to.
            This value uses following format: "projects/{project_name}/global/snapshots/{snapshot_name}"

    Returns:
        AttachedDisk object configured to be created as a copy of specified snapshot.
    """
    disk = compute_v1.AttachedDisk()
    init_params = compute_v1.AttachedDiskInitializeParams()
    init_params.disk_type = disk_type
    init_params.disk_size_gb = disk_size_gb

    init_params.source_snapshot = snapshot_url

    disk.initialize_params = init_params
    disk.auto_delete = True
    disk.boot = boot
    return disk


# [END compute_instances_create_from_snapshot]
# [END compute_instances_create_from_image_plus_snapshot_disk]


# [START compute_instances_create_with_subnet]
# [START compute_instances_create_from_image_plus_snapshot_disk]
# [START compute_instances_create_from_snapshot]
# [START compute_instances_create_from_image_plus_empty_disk]
# [START compute_instances_create_from_custom_image]
# [START compute_instances_create_from_image]
def create_with_disks(
    project_id: str,
    zone: str,
    instance_name: str,
    disks: List[compute_v1.AttachedDisk],
    machine_type: str = "n1-standard-1",
    # source_image: str = "projects/debian-cloud/global/images/family/debian-10",
    network_link: str = "global/networks/default",
    subnetwork_link: str = None,
) -> compute_v1.Instance:
    """
    Send an instance creation request to the Compute Engine API and wait for it to complete.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.
        machine_type: machine type of the VM being created. This value uses the
            following format: "zones/{zone}/machineTypes/{type_name}".
            For example: "zones/europe-west3-c/machineTypes/f1-micro"
        disks: a list of compute_v1.AttachedDisk objects describing the disks
            you want to attach to your new instance.
        network_link: name of the network you want the new instance to use.
            For example: "global/networks/default" represents the `default`
            network interface, which is created automatically for each project.
        subnetwork_link: name of the subnetwork you want the new instance to use.
            Format used: "regions/{region}/subnetworks/{subnetwork_name}"
    Returns:
        Instance object.
    """
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    # Use the network interface provided in the network_link argument.
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = network_link
    if subnetwork_link:
        network_interface.subnetwork = subnetwork_link

    # Collect information into the Instance object.
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.disks = disks
    full_machine_type_name = f"zones/{zone}/machineTypes/{machine_type}"
    instance.machine_type = full_machine_type_name
    instance.network_interfaces = [network_interface]

    # Shielded Instance settings
    instance.shielded_instance_config = compute_v1.ShieldedInstanceConfig()
    instance.shielded_instance_config.enable_secure_boot = False
    instance.shielded_instance_config.enable_vtpm = False
    instance.shielded_instance_config.enable_integrity_monitoring = False

    # Prepare the request to insert an instance.
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance

    # Wait for the create operation to complete.
    print(f"Creating the {instance_name} instance in {zone}...")

    operation = instance_client.insert(request=request)
    while operation.status != compute_v1.Operation.Status.DONE:
        operation = operation_client.wait(
            operation=operation.name, zone=zone, project=project_id
        )
    if operation.error:
        print("Error during creation:", operation.error, file=sys.stderr)
    if operation.warnings:
        print("Warning during creation:", operation.warnings, file=sys.stderr)
    print(f"Instance {instance_name} created.")
    return instance


# [END compute_instances_create_from_image]
# [END compute_instances_create_from_custom_image]
# [END compute_instances_create_from_image_plus_empty_disk]
# [END compute_instances_create_from_snapshot]
# [END compute_instances_create_from_image_plus_snapshot_disk]
# [END compute_instances_create_with_subnet]


# [START compute_instances_create_from_image]
def create_from_public_image(project_id: str, zone: str, instance_name: str):
    """
    Create a new VM instance with Debian 10 operating system.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.

    Returns:
        Instance object.
    """
    image_client = compute_v1.ImagesClient()
    # List of image families: https://cloud.google.com/compute/docs/images/os-details
    newest_debian = image_client.get_from_family(
        project="debian-cloud", family="debian-10"
    )
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link)]
    instance = create_with_disks(project_id, zone, instance_name, disks)
    return instance


# [END compute_instances_create_from_image]


# [START compute_instances_create_from_custom_image]
def create_from_custom_image(
    project_id: str, zone: str, instance_name: str, custom_image_link: str
):
    """
    Create a new VM instance with custom image used as its boot disk.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.
        custom_image_link: link to the custom image you want to use in the form of:
            "projects/{project_name}/global/images/{image_name}"

    Returns:
        Instance object.
    """
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, custom_image_link)]
    instance = create_with_disks(project_id, zone, instance_name, disks)
    return instance


# [END compute_instances_create_from_custom_image]


# [START compute_instances_create_from_image_plus_empty_disk]
def create_with_additional_disk(project_id: str, zone: str, instance_name: str):
    """
    Create a new VM instance with Debian 10 operating system and a 11Gb additional
    empty disk.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.

    Returns:
        Instance object.
    """
    image_client = compute_v1.ImagesClient()
    # List of image families: https://cloud.google.com/compute/docs/images/os-details
    newest_debian = image_client.get_from_family(
        project="debian-cloud", family="debian-10"
    )
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [
        disk_from_image(disk_type, 10, True, newest_debian.self_link),
        empty_disk(disk_type, 11),
    ]
    instance = create_with_disks(project_id, zone, instance_name, disks)
    return instance


# [END compute_instances_create_from_image_plus_empty_disk]


# [START compute_instances_create_from_snapshot]
def create_from_snapshot(
    project_id: str, zone: str, instance_name: str, snapshot_link: str
):
    """
    Create a new VM instance with Debian 10 operating system.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.
        snapshot_link: link to the snapshot you want to use as the source of your
            boot disk in the form of: "projects/{project_name}/global/snapshots/{snapshot_name}"

    Returns:
        Instance object.
    """
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_snapshot(disk_type, 11, True, snapshot_link)]
    instance = create_with_disks(project_id, zone, instance_name, disks)
    return instance


# [END compute_instances_create_from_snapshot]


# [START compute_instances_create_from_image_plus_snapshot_disk]
def create_with_snapshotted_data_disk(
    project_id: str, zone: str, instance_name: str, snapshot_link: str
):
    """
    Create a new VM instance with Debian 10 operating system.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.
        snapshot_link: link to the snapshot you want to use as the source of your
            data disk in the form of: "projects/{project_name}/global/snapshots/{snapshot_name}"

    Returns:
        Instance object.
    """
    image_client = compute_v1.ImagesClient()
    # List of image families: https://cloud.google.com/compute/docs/images/os-details
    newest_debian = image_client.get_from_family(
        project="debian-cloud", family="debian-10"
    )
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [
        disk_from_image(disk_type, 10, True, newest_debian.self_link),
        disk_from_snapshot(disk_type, 11, False, snapshot_link),
    ]
    instance = create_with_disks(project_id, zone, instance_name, disks)
    return instance


# [END compute_instances_create_from_image_plus_snapshot_disk]


# [START compute_instances_create_with_subnet]
def create_with_subnet(
    project_id: str, zone: str, instance_name: str, network_link: str, subnet_link: str
):
    """
    Create a new VM instance with Debian 10 operating system in specified network and subnetwork.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.
        network_link: name of the network you want the new instance to use.
            For example: "global/networks/default" represents the `default`
            network interface, which is created automatically for each project.
        subnetwork_link: name of the subnetwork you want the new instance to use.
            Format used: "regions/{region}/subnetworks/{subnetwork_name}"

    Returns:
        Instance object.
    """
    image_client = compute_v1.ImagesClient()
    # List of image families: https://cloud.google.com/compute/docs/images/os-details
    newest_debian = image_client.get_from_family(
        project="debian-cloud", family="debian-10"
    )
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link)]
    instance = create_with_disks(
        project_id,
        zone,
        instance_name,
        disks,
        network_link=network_link,
        subnetwork_link=subnet_link,
    )
    return instance


# [END compute_instances_create_with_subnet]
