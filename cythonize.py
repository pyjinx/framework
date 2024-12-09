import os

from typing import List
from Cython.Build import cythonize
from setuptools import setup, Extension


def get_ext(package: str, package_path: str, file: str) -> Extension:
    # Create the extension name and file path
    name = f"{package}.{file}".replace(".py", "")
    file_path = os.path.join(package_path, file)
    return Extension(name=name, sources=[file_path], language="c++")


def find_extensions(
    base_package: str, base_path: str, included_directories: List[str]
) -> List[Extension]:
    ext_modules: List[Extension] = []

    for root, dirs, files in os.walk(base_path):
        # Convert the root path to package format
        rel_path = os.path.relpath(root, base_path)
        # Handle the base package case
        if rel_path == ".":
            package = base_package
        else:
            package = f"{base_package}.{rel_path.replace(os.path.sep, '.')}"

        # Ensure we only process directories specified in included_directories
        if any(
            package.startswith(included_package)
            for included_package in included_directories
        ):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    ext_modules.append(get_ext(package, root, file))

    return ext_modules


included_directories = ["Illuminate"]

base_package = "Illuminate"

base_path = os.path.join(os.path.dirname(__file__), base_package)

ext_modules = find_extensions(base_package, base_path, included_directories)

setup(
    name=base_package,
    ext_modules=cythonize(ext_modules, language_level=3),
)
