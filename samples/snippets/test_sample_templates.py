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

import uuid

import google.auth

from sample_templates import (
    create_template,
    create_template_from_instance,
    create_template_with_subnet,
    delete_instance_template,
    list_instance_templates,
)

# Turning off F401 check because flake8 doesn't recognize using
# PyTest fixture as parameter as usage.
from test_sample_start_stop import compute_instance  # noqa: F401

PROJECT = google.auth.default()[1]

INSTANCE_ZONE = "europe-central2-b"


def test_create_instance():
    template_name = "i" + uuid.uuid4().hex[:10]
    template = create_template(PROJECT, template_name)

    try:
        assert template.name == template_name
        assert template.properties.disks[0].initialize_params.disk_size_gb == 250
        assert (
            "debian-11" in template.properties.disks[0].initialize_params.source_image
        )
        assert (
            template.properties.network_interfaces[0].name == "global/networks/default"
        )
        assert template.properties.machine_type == "e2-standard-4"
    finally:
        delete_instance_template(PROJECT, template_name)
    assert all(
        template.name != template_name for template in list_instance_templates(PROJECT)
    )


def test_create_from_instance(compute_instance):
    template_name = "i" + uuid.uuid4().hex[:10]
    template = create_template_from_instance(
        PROJECT, compute_instance.self_link, template_name
    )

    try:
        assert template.name == template_name
        assert template.properties.machine_type in compute_instance.machine_type
        assert (
            template.properties.disks[0].disk_size_gb
            == compute_instance.disks[0].disk_size_gb
        )
        assert (
            template.properties.disks[0].initialize_params.source_image
            == "projects/rocky-linux-cloud/global/images/family/rocky-linux-8"
        )
    finally:
        delete_instance_template(PROJECT, template_name)


def test_create_template_with_subnet():
    template_name = "i" + uuid.uuid4().hex[:10]
    template = create_template_with_subnet(
        PROJECT,
        "global/networks/default",
        "regions/asia-east1/subnetworks/default",
        template_name,
    )

    try:
        assert template.name == template_name
        assert (
            "global/networks/default"
            in template.properties.network_interfaces[0].network
        )
        assert (
            "regions/asia-east1/subnetworks/default"
            in template.properties.network_interfaces[0].subnetwork
        )
    finally:
        delete_instance_template(PROJECT, template_name)
