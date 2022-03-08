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
import time

from google.cloud import compute_v1


# <INGREDIENT delete_instance>
def delete_instance(project_id: str, zone: str, machine_name: str) -> None:
    """
    Send an instance deletion request to the Compute Engine API and wait for it to complete.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        machine_name: name of the machine you want to delete.
    """
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    print(f"Deleting {machine_name} from {zone}...")
    operation = instance_client.delete_unary(
        project=project_id, zone=zone, instance=machine_name
    )
    start = time.time()
    while operation.status != compute_v1.Operation.Status.DONE:
        operation = operation_client.wait(
            operation=operation.name, zone=zone, project=project_id
        )
        if time.time() - start >= 300:  # 5 minutes
            raise TimeoutError()
    if operation.error:
        print("Error during deletion:", operation.error, file=sys.stderr)
        return
    if operation.warnings:
        print("Warning during deletion:", operation.warnings, file=sys.stderr)
    print(f"Instance {machine_name} deleted.")
    return
# </INGREDIENT>
