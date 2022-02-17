# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for SetIamPolicy
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-compute


# [START compute_generated_compute_v1_Disks_SetIamPolicy_sync]
from google.cloud import compute_v1


def sample_set_iam_policy():
    # Create a client
    client = compute_v1.DisksClient()

    # Initialize request argument(s)
    request = compute_v1.SetIamPolicyDiskRequest(
        project="project_value",
        resource="resource_value",
        zone="zone_value",
    )

    # Make the request
    response = client.set_iam_policy(request=request)

    # Handle the response
    print(response)

# [END compute_generated_compute_v1_Disks_SetIamPolicy_sync]
