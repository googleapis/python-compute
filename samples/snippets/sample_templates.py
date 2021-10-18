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
from typing import Iterable

from google.cloud import compute_v1


def get_instance_template(project_id: str, template_name: str) -> compute_v1.InstanceTemplate:
    template_client = compute_v1.InstanceTemplatesClient()
    return template_client.get(project=project_id, instance_template=template_name)


def list_instance_templates(project_id: str) -> Iterable[compute_v1.InstanceTemplate]:
    template_client = compute_v1.InstanceTemplatesClient()
    return template_client.list(project=project_id)


def create_template(project_id: str, template_name: str) -> compute_v1.InstanceTemplate:

    # Describe the size and source image of the boot disk to attach to the instance.
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = 250
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    # Use the default network, without specifying a subnetwork.
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"

    # Let the instance have external IP
    network_interface.access_configs = [compute_v1.AccessConfig()]
    network_interface.access_configs[0].name = "External NAT"
    network_interface.access_configs[0].type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT
    network_interface.access_configs[0].network_tier = (
        compute_v1.AccessConfig.NetworkTier.PREMIUM
    )

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.properties.disks = [disk]
    template.properties.machine_type = "e2-standard-4"
    template.properties.network_interfaces = [network_interface]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert(project=project_id, instance_template_resource=template)
    operation_client.wait(project=project_id, operation=op.name)

    return template_client.get(project=project_id, instance_template=template_name)


def create_template_from_instance(
    project_id: str, instance_link: str, template_name: str
) -> compute_v1.InstanceTemplate:

    disk = compute_v1.DiskInstantiationConfig()
    # This name must match the name of a disk attached to the instance you are
    # basing your template on.
    disk.device_name = "disk-1"
    # Replace the original disk image used in your instance with a Rocky Linux image.
    disk.instantiate_from = (
        compute_v1.DiskInstantiationConfig.InstantiateFrom.CUSTOM_IMAGE
    )
    disk.custom_image = "projects/rocky-linux-cloud/global/images/family/rocky-linux-8"
    # You can override the auto_delete setting.
    disk.auto_delete = True

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.source_instance = instance_link
    template.source_instance_params = compute_v1.SourceInstanceParams()
    template.source_instance_params.disk_configs = [disk]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert(project=project_id, instance_template_resource=template)
    operation_client.wait(project=project_id, operation=op.name)

    return template_client.get(project=project_id, instance_template=template_name)


def create_template_with_subnet(
    project_id: str, network: str, subnetwork: str, template_name: str
) -> compute_v1.InstanceTemplate:
    """
    Create an instance template that will use a provided subnet.

    """
    # Describe the size and source image of the boot disk to attach to the instance.
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = 250
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.properties = compute_v1.InstanceProperties()
    template.properties.disks = [disk]
    template.properties.machine_type = "e2-standard-4"

    # Make this template use provided subnetwork.
    network_interface = compute_v1.NetworkInterface()
    network_interface.network = network
    network_interface.subnetwork = subnetwork
    template.properties.network_interfaces = [network_interface]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert(project=project_id, instance_template_resource=template)
    operation_client.wait(project=project_id, operation=op.name)

    return template_client.get(project=project_id, instance_template=template_name)


def delete_instance_template(project_id: str, template_name: str):
    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.delete(project=project_id, instance_template=template_name)
    operation_client.wait(project=project_id, operation=op.name)
    return
