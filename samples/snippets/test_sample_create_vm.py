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
import time
import uuid
from collections import deque

from google.api_core.exceptions import NotFound
import google.auth
from google.cloud import compute_v1
import pytest


from quickstart import delete_instance, wait_for_operation
from sample_create_vm import (
    create_from_custom_image,
    create_from_public_image,
    create_from_snapshot,
    create_with_additional_disk,
    create_with_snapshotted_data_disk,
    create_with_subnet,
)

PROJECT = google.auth.default()[1]
REGION = 'us-central1'
INSTANCE_ZONE = "us-central1-b"


def get_active_debian():
    image_client = compute_v1.ImagesClient()

    return image_client.get_from_family(project="debian-cloud", family="debian-11")


@pytest.fixture(scope="class")
def src_disk(request):
    disk_client = compute_v1.DisksClient()

    disk = compute_v1.Disk()
    disk.source_image = get_active_debian().self_link
    disk.name = "test-disk-" + uuid.uuid4().hex[:10]
    op = disk_client.insert(project=PROJECT, zone=INSTANCE_ZONE, disk_resource=disk)

    wait_for_operation(op, PROJECT)
    try:
        disk = disk_client.get(project=PROJECT, zone=INSTANCE_ZONE, disk=disk.name)
        request.cls.disk = disk
        yield disk
    finally:
        op = disk_client.delete(project=PROJECT, zone=INSTANCE_ZONE, disk=disk.name)
        wait_for_operation(op, PROJECT)


@pytest.fixture(scope="class")
def snapshot(request, src_disk):
    snapshot_client = compute_v1.SnapshotsClient()
    snapshot = compute_v1.Snapshot()
    snapshot.name = "test-snap-" + uuid.uuid4().hex[:10]
    disk_client = compute_v1.DisksClient()
    op = disk_client.create_snapshot(
        project=PROJECT,
        zone=INSTANCE_ZONE,
        disk=src_disk.name,
        snapshot_resource=snapshot,
    )
    wait_for_operation(op, PROJECT)
    try:
        request.cls.snapshot = snapshot_client.get(
            project=PROJECT, snapshot=snapshot.name
        )
        snapshot = request.cls.snapshot

        yield snapshot
    finally:
        op = snapshot_client.delete(project=PROJECT, snapshot=snapshot.name)
        wait_for_operation(op, PROJECT)


@pytest.fixture(scope="class")
def image(request, src_disk):
    image_client = compute_v1.ImagesClient()
    image = compute_v1.Image()
    image.source_disk = src_disk.self_link
    image.name = "test-image-" + uuid.uuid4().hex[:10]
    op = image_client.insert(project=PROJECT, image_resource=image)

    wait_for_operation(op, PROJECT)
    try:
        image = image_client.get(project=PROJECT, image=image.name)
        request.cls.image = image
        yield image
    finally:
        op = image_client.delete(project=PROJECT, image=image.name)
        wait_for_operation(op, PROJECT)


@pytest.fixture()
def subnetwork():
    network_client = compute_v1.NetworksClient()
    network = compute_v1.Network()
    network.name = "test-network-" + uuid.uuid4().hex[:10]
    network.auto_create_subnetworks = True
    op = network_client.insert(project=PROJECT, network_resource=network)
    wait_for_operation(op, PROJECT)
    try:
        network = network_client.get(project=PROJECT, network=network.name)

        subnet = compute_v1.Subnetwork()
        subnet.name = "test-subnet-" + uuid.uuid4().hex[:10]
        subnet.network = network_client.get(project=PROJECT, network=network.name).self_link
        subnet.region = REGION
        subnet.ip_cidr_range = "10.0.0.0/20"
        subnet_client = compute_v1.SubnetworksClient()
        op = subnet_client.insert(
            project=PROJECT, region=REGION, subnetwork_resource=subnet
        )
        wait_for_operation(op, PROJECT)
        try:
            subnet = subnet_client.get(
                project=PROJECT, region=REGION, subnetwork=subnet.name
            )

            yield subnet
        finally:
            op = subnet_client.delete(
                project=PROJECT, region=REGION, subnetwork=subnet.name
            )
            wait_for_operation(op, PROJECT)
    finally:
        firewall_client = compute_v1.FirewallsClient()
        firewall_request = compute_v1.ListFirewallsRequest()
        firewall_request.project = PROJECT
        firewall_request.filter = f'network = "{network.self_link}"'
        network_request = compute_v1.ListNetworksRequest()
        network_request.project = PROJECT
        network_request.filter = f'name = "{network.name}"'
        networks = network_client.list(network_request)
        start_time = time.time()
        while networks:
            # Repeat until the test network is gone.
            ops = deque()
            # Get all firewall rules associated with the test network.
            firewalls = firewall_client.list(firewall_request)
            # while firewalls:
                # Repeat until all firewall rules are gone.
            for firewall in firewalls:
                # Start deleting all firewall rules for test network.
                ops.append(firewall_client.delete(project=PROJECT, firewall=firewall.name))
                # for op in ops:
                    # Wait for the delete operations to finish.
                    # wait_for_operation(op, PROJECT)
                # Update firewall rules list, to make sure they are all gone.
                # firewalls = firewall_client.list(firewall_request)
            # Attempt deleting the test network. Hopefully, the firewall
            # rules were not re-added by the enforcer.
            try:
                op = network_client.delete(project=PROJECT, network=network.name)
                wait_for_operation(op, PROJECT)
            except NotFound:
                pass
            # Update list of networks to make sure the network is gone.
            networks = network_client.list(network_request)
            if time.time() - start_time >= 300:
                # If we fail to remove the the network for 5 minutes
                # We fail with a bang!
                raise RuntimeError(f"Couldn't clean up network: {network.name}. "
                                   f"This will need manual clean-up!!!")


@pytest.mark.usefixtures("image", "snapshot")
class TestCreation:
    # def test_create_from_custom_image(self):
    #     instance_name = "i" + uuid.uuid4().hex[:10]
    #     instance = create_from_custom_image(
    #         PROJECT, INSTANCE_ZONE, instance_name, self.image.self_link
    #     )
    #     try:
    #         assert (
    #             instance.disks[0].initialize_params.source_image == self.image.self_link
    #         )
    #     finally:
    #         delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
    #
    # def test_create_from_public_image(self):
    #     instance_name = "i" + uuid.uuid4().hex[:10]
    #     instance = create_from_public_image(
    #         PROJECT,
    #         INSTANCE_ZONE,
    #         instance_name,
    #     )
    #     try:
    #         assert "debian-cloud" in instance.disks[0].initialize_params.source_image
    #         assert "debian-10" in instance.disks[0].initialize_params.source_image
    #     finally:
    #         delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
    #
    # def test_create_from_snapshot(self):
    #     instance_name = "i" + uuid.uuid4().hex[:10]
    #     instance = create_from_snapshot(
    #         PROJECT, INSTANCE_ZONE, instance_name, self.snapshot.self_link
    #     )
    #     try:
    #         assert (
    #             instance.disks[0].initialize_params.source_snapshot
    #             == self.snapshot.self_link
    #         )
    #     finally:
    #         delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
    #
    # def test_create_with_additional_disk(self):
    #     instance_name = "i" + uuid.uuid4().hex[:10]
    #     instance = create_with_additional_disk(PROJECT, INSTANCE_ZONE, instance_name)
    #     try:
    #         assert any(
    #             disk.initialize_params.disk_size_gb == 11 for disk in instance.disks
    #         )
    #         assert any(
    #             disk.initialize_params.disk_size_gb == 10 for disk in instance.disks
    #         )
    #         assert len(instance.disks) == 2
    #     finally:
    #         delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
    #
    # def test_create_with_snapshotted_data_disk(self):
    #     instance_name = "i" + uuid.uuid4().hex[:10]
    #     instance = create_with_snapshotted_data_disk(
    #         PROJECT, INSTANCE_ZONE, instance_name, self.snapshot.self_link
    #     )
    #     try:
    #         assert any(
    #             disk.initialize_params.disk_size_gb == 11 for disk in instance.disks
    #         )
    #         assert any(
    #             disk.initialize_params.disk_size_gb == 10 for disk in instance.disks
    #         )
    #         assert len(instance.disks) == 2
    #     finally:
    #         delete_instance(PROJECT, INSTANCE_ZONE, instance_name)

    def test_create_with_subnet(self, subnetwork):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_with_subnet(
            PROJECT,
            INSTANCE_ZONE,
            instance_name,
            subnetwork.network,
            subnetwork.self_link,
        )
        time.sleep(120)
        try:
            assert instance.network_interfaces[0].name == subnetwork.network
            assert instance.network_interfaces[0].subnetwork == subnetwork.self_link
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
