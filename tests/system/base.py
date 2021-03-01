# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import unittest
import uuid
from google.cloud.compute_v1.services.zone_operations.client import ZoneOperationsClient
from google.cloud.compute_v1.services.region_operations.client import RegionOperationsClient
from google.cloud.compute_v1.services.global_operations.client import GlobalOperationsClient


class TestBase(unittest.TestCase):

    def setUp(self):
        self.DEFAULT_PROJECT = 'cloud-sdk-integration-testing' #os.getenv('GCLOUD_PROJECT')
        if not self.DEFAULT_PROJECT:
            self.fail('Need to set GCLOUD_PROJECT to run system tests')
        self.DEFAULT_ZONE = "us-central1-a"
        self.DEFAULT_REGION = "us-central1"
        self.MACHINE_TYPE = "https://www.googleapis.com/compute/v1/projects/{}/" \
                            "zones/us-central1-a/machineTypes/n1-standard-1".format(self.DEFAULT_PROJECT)
        self.DISK_IMAGE = "projects/debian-cloud/global/images/family/debian-10"

    @staticmethod
    def get_unique_name(placeholder=''):
        return "gapic" + placeholder + uuid.uuid4().hex

    def wait_for_zonal_operation(self, operation):
        client = ZoneOperationsClient()
        result = client.wait(operation=operation, zone=self.DEFAULT_ZONE, project=self.DEFAULT_PROJECT)
        if result.error:
            self.fail('Zonal operation {} has errors'.format(operation))

    def wait_for_regional_operation(self, operation):
        client = RegionOperationsClient()
        result = client.wait(operation=operation, region=self.DEFAULT_REGION, project=self.DEFAULT_PROJECT)
        if result.error:
            self.fail('Region operation {} has errors'.format(operation))

    def wait_for_global_operation(self, operation):
        client = GlobalOperationsClient()
        result = client.wait(operation=operation, project=self.DEFAULT_PROJECT)
        if result.error:
            self.fail('Global operation {} has errors'.format(operation))
