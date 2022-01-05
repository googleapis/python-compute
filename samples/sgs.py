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
from collections import defaultdict
from pathlib import Path
import ast
import re
import warnings
from dataclasses import dataclass, field
from typing import List, Tuple

INGREDIENTS_START = re.compile(r"\s*#\s*<INGREDIENT ([\w\d_-]+)>")
INGREDIENTS_END = re.compile(r"\s*#\s*</INGREDIENT>")

IMPORTS_FILL = re.compile(r"\s*##\s*IMPORTS")
INGREDIENT_FILL = re.compile(r"\s*##\s*INGREDIENT ([\s\w_-]+)")


@dataclass
class ImportItem:
    """
    Represents a single import item in a script, created either by
    `import something as something_else` or
    `from module import something as something_else`.
    """
    name: str
    asname: str


@dataclass
class Ingredient:
    """
    This class represents a piece of code that can be used as part of a code snippet.
    Each ingredient has a name. It is made of a list of imports that it'll require and
    text that will be pasted into the snippet.
    """
    simple_imports: List[ImportItem] = field(default_factory=list)
    imports_from: List[Tuple[str, ImportItem]] = field(default_factory=list)
    text: str = ""
    name: str = ""



IGNORED_OUTPUT_FILES = {
    Path('noxfile.py'),
    Path('noxfile_config.py'),
    Path('README.md'),
    Path('requirements.txt'),
    Path('requirements-test.txt'),
}


def parse_imports(script: str) -> Tuple[List[ImportItem], List[Tuple[str, ImportItem]]]:
    """
    Reads a Python script file and analyzes it to extract information
    about the various things it imports. Returns a pair of lists containing
    information about the "simple imports" (`import abc as xyz`) and "imports from"
    (`from collections import deque as ...`).
    """
    parsed_script = ast.parse(script)
    simple_imports = []
    imports_from = []
    for node in parsed_script.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                simple_imports.append(ImportItem(name=alias.name, asname=alias.asname))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports_from.append((node.module, ImportItem(name=alias.name, asname=alias.asname)))
    return simple_imports, imports_from


def load_ingredient(path: Path) -> Ingredient:
    template_lines = []
    in_template = False
    template_name = ""
    with path.open() as file:
        file_content = file.read()
    # Read imports
    simple_imports, imports_from = parse_imports(file_content)
    # Read the script
    for line in file_content.splitlines():
        if in_template and INGREDIENTS_END.match(line):
            break
        elif in_template:
            template_lines.append(line)
        elif match := INGREDIENTS_START.match(line):
            template_name = match.group(1)
            in_template = True
    else:
        warnings.warn(f"The template in {path} has no closing tag.", SyntaxWarning)
    return Ingredient(name=template_name, text="".join(template_lines), simple_imports=simple_imports, imports_from=imports_from)


def load_ingredients(path: Path) -> dict:
    ingredients = {}
    for ipath in path.iterdir():
        if ipath.is_dir():
            ingredients.update(load_ingredients(ipath))
        elif ipath.is_file():
            ingredient = load_ingredient(ipath)
            ingredients[ingredient.name] = ingredient
    return ingredients


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


def render_recipe(recipe: str, ingredients: dict) -> str:
    """
    Replace all `##IMPORTS` and `##INGREDIENT <name>` occurrences in
    the provided recipe, producing a script ready to be saved to a file.
    """
    ingredients_used = []
    file_lines = recipe.splitlines()

    # Scan the file to used ingredients
    for line in file_lines:
        if match := INGREDIENT_FILL.match(line):
            ingredients_used.append(ingredients[match.group(1)])

    simple_imports_used = {ingredient.simple_imports for ingredient in ingredients_used}

    from_imports_used = defaultdict(set)
    for ingredient in ingredients_used:
        for import_from in ingredient.imports_from:
            from_imports_used[import_from[0]] = import_from[1]

    import_lines = set()
    for simple_import in simple_imports_used:
        if simple_import.asname:
            import_lines.add(f"import {simple_import.name} as {simple_import.asname}")
        else:
            import_lines.add(f"import {simple_import.name}")

    for module, from_imports in from_imports_used.items():
        names = set()
        for from_import in from_imports:
            if from_import.asname:
                names.add(f"{from_import.name} as {from_import.asname}")
            else:
                names.add(from_import.name)
        names = ", ".join(names)
        import_lines.add(f"from {module} import ({names})")

    output_file = []
    for line in file_lines:
        if match := IMPORTS_FILL.match(line):
            output_file.extend(import_lines)
        elif match := INGREDIENT_FILL.match(line):
            output_file.append(ingredients[match.group(1).text])


def generate():
    print(load_ingredients(Path('ingredients')))


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
