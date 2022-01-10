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


# <INGREDIENT create_custom_shared_core_instance>
def create_custom_shared_core_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    cpu_series: CustomMachineType.CPUSeries,
    memory: int,
):
    """
    Create a new VM instance with a custom type using shared CPUs.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        cpu_series: the type of CPU you want to use. Pick one value from the CustomMachineType.CPUSeries enum.
            For example: CustomMachineType.CPUSeries.E2_MICRO
        memory: the amount of memory for the VM instance, in megabytes.

    Return:
        Instance object.
    """
    assert cpu_series in (
        CustomMachineType.CPUSeries.E2_MICRO,
        CustomMachineType.CPUSeries.E2_SMALL,
        CustomMachineType.CPUSeries.E2_MEDIUM,
    )
    custom_type = CustomMachineType(zone, cpu_series, memory)
    return create_instance(project_id, zone, instance_name, str(custom_type))
# </INGREDIENT>
