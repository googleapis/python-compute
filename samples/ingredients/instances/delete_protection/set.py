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
from google.cloud import compute_v1


# <INGREDIENT set_delete_protection>
def set_delete_protection(
    project_id: str, zone: str, instance_name: str, delete_protection: bool
):
    """
    Updates the delete protection setting of given instance.
    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the virtual machine to update.
        delete_protection: boolean value indicating if the virtual machine should be
            protected against deletion or not.
    """
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    request = compute_v1.SetDeletionProtectionInstanceRequest()
    request.project = project_id
    request.zone = zone
    request.resource = instance_name
    request.deletion_protection = delete_protection

    operation = instance_client.set_deletion_protection_unary(request)
    operation_client.wait(project=project_id, zone=zone, operation=operation.name)
    return
# </INGREDIENT>
