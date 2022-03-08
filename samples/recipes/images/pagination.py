#!/usr/bin/env python

# Copyright 2022 Google LLC
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

# <REGION compute_images_list_page>
# <REGION compute_images_list>
import google.cloud.compute_v1 as compute_v1

# </REGION compute_images_list>
# </REGION compute_images_list_page>


# <REGION compute_images_list>
def print_images_list(project: str) -> str:
    """
    Prints a list of all non-deprecated image names available in given project.

    Args:
        project: project ID or project number of the Cloud project you want to list images from.

    Returns:
        The output as a string.
    """
    images_client = compute_v1.ImagesClient()
    # Listing only non-deprecated images to reduce the size of the reply.
    images_list_request = compute_v1.ListImagesRequest(
        project=project, max_results=100, filter="deprecated.state != DEPRECATED"
    )
    output = []

    # Although the `max_results` parameter is specified in the request, the iterable returned
    # by the `list()` method hides the pagination mechanic. The library makes multiple
    # requests to the API for you, so you can simply iterate over all the images.
    for img in images_client.list(request=images_list_request):
        print(f" -  {img.name}")
        output.append(f" -  {img.name}")
    return "\n".join(output)


# </REGION compute_images_list>


# <REGION compute_images_list_page>
def print_images_list_by_page(project: str, page_size: int = 10) -> str:
    """
    Prints a list of all non-deprecated image names available in a given project,
    divided into pages as returned by the Compute Engine API.

    Args:
        project: project ID or project number of the Cloud project you want to list images from.
        page_size: size of the pages you want the API to return on each call.

    Returns:
        Output as a string.
    """
    images_client = compute_v1.ImagesClient()
    # Listing only non-deprecated images to reduce the size of the reply.
    images_list_request = compute_v1.ListImagesRequest(
        project=project, max_results=page_size, filter="deprecated.state != DEPRECATED"
    )
    output = []

    # Use the `pages` attribute of returned iterable to have more granular control of
    # iteration over paginated results from the API. Each time you want to access the
    # next page, the library retrieves that page from the API.
    for page_num, page in enumerate(
        images_client.list(request=images_list_request).pages, start=1
    ):
        print(f"Page {page_num}: ")
        output.append(f"Page {page_num}: ")
        for img in page.items:
            print(f" - {img.name}")
            output.append(f" - {img.name}")
    return "\n".join(output)


# </REGION compute_images_list_page>


if __name__ == "__main__":
    print("=================== Flat list of images ===================")
    print_images_list("windows-sql-cloud")
    print("================= Paginated list of images ================")
    print_images_list_by_page("windows-sql-cloud", 5)
