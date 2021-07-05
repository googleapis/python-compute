#!/usr/bin/env python

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


import google.cloud.compute_v1 as compute_v1


def print_images_list(project: str) -> None:
    """
    Prints a list of all non-deprecated image names available in given project.

    Args:
        project: project ID or project number of the Cloud project you want to list images from.

    Returns:
        None
    """
    images_client = compute_v1.ImagesClient()
    # Listing only non-deprecated images to reduce the size of the reply.
    images_list_request = compute_v1.ListImagesRequest(project=project, max_results=3,
                                                       filter="deprecated.state != DEPRECATED")

    # Although the max_results parameter is specified as 3 in the request, the iterable returned
    # by the `list()` method hides the pagination mechanic and allows you to simply iterate over
    # all the images, while the library makes multiple requests to the API for you.
    for img in images_client.list(request=images_list_request):
        print(f" -  {img.name}")


def print_images_list_by_page(project: str, page_size: int = 10) -> None:
    """
    Prints a list of all non-deprecated image names available in given project,
    divided into pages, as returned by the GCE API.

    Args:
        project: project ID or project number of the Cloud project you want to list images from.
        page_size: size of the pages you want the API to return on each call.

    Returns:
        None
    """
    images_client = compute_v1.ImagesClient()
    # Listing only non-deprecated images to reduce the size of the reply.
    images_list_request = compute_v1.ListImagesRequest(project=project, max_results=page_size,
                                                       filter="deprecated.state != DEPRECATED")

    # By using the `pages` attribute of returned iterable, you can have more granular control over
    # the way you iterate over paginated results retrieved from the API. Each time you want to
    # access next page, the library retrieves it from the API.
    for page_num, page in enumerate(images_client.list(request=images_list_request).pages, start=1):
        print(f"Page {page_num}: ")
        for img in page.items:
            print(f" - {img.name}")


if __name__ == '__main__':
    print("=================== Flat list of images ===================")
    print_images_list('windows-sql-cloud')
    print("================= Paginated list of images ================")
    print_images_list_by_page('windows-sql-cloud', 5)
