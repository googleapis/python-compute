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
from copy import copy

import pytest

import google.api_core.exceptions
from google.cloud import compute_v1
import uuid
import google.auth
from ..disks.delete import delete_disk
from ..disks.list import list_disks
from samples.snippets.instances.create_start_instance.create_windows_instance import get_image_from_family

PROJECT = google.auth.default()[1]
ZONE = 'europe-north1-c'


def test_request_id():
    disk = compute_v1.Disk()
    disk.size_gb = 20
    disk.name = "test-disk-" + uuid.uuid4().hex[:10]
    disk.zone = ZONE
    disk.type_ = f"zones/{ZONE}/diskTypes/pd-standard"
    disk.source_image = get_image_from_family('debian-cloud', 'debian-11').self_link

    disk2 = copy(disk)
    disk2.name = "test-disk-" + uuid.uuid4().hex[:10]

    request = compute_v1.InsertDiskRequest()
    request.request_id = str(uuid.uuid4())
    request.project = PROJECT
    request.zone = ZONE
    request.disk_resource = disk

    # Creating a different request, but with the same request_id
    # This should not be executed, because the previous request
    # has the same ID.
    request2 = copy(request)
    request2.disk_resource = disk2

    disk_client = compute_v1.DisksClient()
    try:
        operation = disk_client.insert(request)
        operation2 = disk_client.insert(request2)
        operation.result()
        operation2.result()
    except Exception as err:
        pytest.fail(f"There was an error: {err}")
    else:
        disks = list_disks(PROJECT, ZONE)
        print(disks)
        assert any(i_disk.name == disk.name for i_disk in disks)

        assert not any(i_disk.name == disk2.name for i_disk in disks)
    finally:
        delete_disk(PROJECT, ZONE, disk.name)
        try:
            delete_disk(PROJECT, ZONE, disk2.name)
        except google.api_core.exceptions.NotFound:
            pass
