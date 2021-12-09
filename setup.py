#!/usr/bin/env python

import glob
import os

from setuptools import find_packages, setup
from setuptools.command.test import test as test_command


def read(fname):
    """Read the contents of a file."""
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


install_requires = read("requirements.txt").splitlines()

# Dynamically determine extra dependencies
extras_require = {}
extra_req_files = glob.glob("requirements-*.txt")
for extra_req_file in extra_req_files:
    name = os.path.splitext(extra_req_file)[0].replace("requirements-", "", 1)
    extras_require[name] = read(extra_req_file).splitlines()

# If there are any extras, add a catch-all case that includes everything.
# This assumes that entries in extras_require are lists (not single strings),
# and that there are no duplicated packages across the extras.
if extras_require:
    extras_require["all"] = sorted({x for v in extras_require.values() for x in v})


# Import meta data from __meta__.py
#
# We use exec for this because __meta__.py runs its __init__.py first,
# __init__.py may assume the requirements are already present, but this code
# is being run during the `python setup.py install` step, before requirements
# are installed.
# https://packaging.python.org/guides/single-sourcing-package-version/
meta = {}
exec(read("openapi_builder/__meta__.py"), meta)


readme = "README.rst"
long_description = read(readme)
long_description_content_type = "text/x-rst"


class PyTest(test_command):
    """Support setup.py test."""

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        pytest.main(self.test_args)


setup(
    # Essential details on the package and its dependencies
    name=meta["name"],
    version=meta["version"],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={meta["name"]: os.path.join(".", meta["path"])},
    include_package_data=True,
    package_data={meta["name"]: ["templates/*.html"]},
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require=extras_require,
    # Metadata to display on PyPI
    author=meta["author"],
    author_email=meta["author_email"],
    description=meta["description"],
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    license=meta["license"],
    url=meta["url"],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # Custom commands
    cmdclass={
        "test": PyTest,
    },
)
