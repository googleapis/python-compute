#  Copyright 2021 Google LLC
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
"""
This script is used to generate the full code samples inside the `snippets`
directory, to be then used in Google Compute Engine public documentation.
"""
import argparse
from pathlib import Path
import os
import re
import warnings


TEMPLATE_START = re.compile(r"#\s+<TEMPLATE (\w\d_-+)>")
TEMPLATE_END = re.compile(r"#\s+</TEMPLATE>")


IGNORED_OUTPUT_FILES = {
    Path('noxfile.py'),
    Path('noxfile_config.py'),
    Path('README.md'),
    Path('requirements.txt'),
    Path('requirements-test.txt'),
}


def load_template(path: Path) -> (str, str):
    template_lines = []
    in_template = False
    template_name = ""
    with path.open() as file:
        for line in file.readlines():
            if in_template and TEMPLATE_END.match(line):
                return template_name, "".join(template_lines)
            elif in_template:
                template_lines.append(line)
            elif match := TEMPLATE_START.match(line):
                template_name = match.group(1)
                in_template = True
    warnings.warn(f"The template in {path} has no closing tag.", SyntaxWarning)
    return template_name, "".join(template_lines)


def load_templates(path: Path) -> dict:
    templates = {}
    for ipath in path.iterdir():
        if ipath.is_dir():
            templates.update(load_templates(ipath))
        elif ipath.is_file():
            name, template = load_template(ipath)
            templates[name] = template
    return templates


def load_recipe(path: Path) -> str:
    with path.open() as file:
        return file.read()


def load_recipes(path: Path) -> dict:
    recipes = {}
    for ipath in path.iterdir():
        if ipath.is_dir():
            recipes.update(load_recipes(ipath))
        elif ipath.is_file():
            recipes[ipath] = load_recipe(ipath)
    return recipes


def generate():
    print(load_templates(Path('templates')))


def verify():
    pass


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generates full code snippets from their recipes.')
    subparsers = parser.add_subparsers()

    gen_parser = subparsers.add_parser("generate", help="Generates the code samples.")
    gen_parser.set_defaults(func=generate)

    verify_parser = subparsers.add_parser("verify", help="Verify if the generated samples match the sources.")
    verify_parser.set_defaults(func=verify)

    return parser.parse_args()


def main():
    args = parse_arguments()
    args.func()


if __name__ == '__main__':
    main()