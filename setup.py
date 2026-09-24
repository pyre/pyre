#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# external
import os
import pybind11
import setuptools
import skbuild

from setuptools_scm import get_version


def version() -> str:
    """
    Resolve the package version from the git tag, falling back to the sdist
    metadata when the build happens outside a git checkout.
    """
    try:
        return get_version(root=".", relative_to=__file__, local_scheme="no-local-version")
    except LookupError:
        # no .git here: we are building from an sdist, where setuptools_scm has
        # already recorded the version in PKG-INFO
        info = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PKG-INFO")
        with open(info) as stream:
            for line in stream:
                if line.startswith("Version:"):
                    return line.split(":", 1)[1].strip()
        raise


# the full PEP 440 version for the python package metadata
pyreVersion = version()
# cmake's project(VERSION ...) wants a bare X.Y.Z, not 1.12.7.dev161+g0123abc
cmakeVersion = pyreVersion.split("+")[0].split(".dev")[0]

# where cmake installs the python packages, relative to its prefix: the same {packages}
# folder the sources live in and mm installs to. scikit-build matches what cmake installs
# against the source folder of each declared package, and merges a match into the package at
# the root of the wheel, which pip installs into {site-packages}; anything else goes to the
# wheel's data tree. the extension modules must be merged this way, because the wheel repair
# tools, {delocate} and {auditwheel}, compute the paths from the extensions to the shared
# libraries they bundle against the wheel's own layout: spelled as
# {lib/pythonX.Y/site-packages}, the packages sat seven levels down in the data tree, and the
# installed extensions looked for their libraries seven levels above {site-packages}
packageDir = "packages"

# the python packages, as the {[tool.setuptools.packages.find]} table in {pyproject.toml}
# declares them; scikit-build classifies what cmake installs by this list, not by the table:
# a cmake-installed file that falls inside one of these packages joins it at the root of the
# wheel, and anything else goes to the wheel's data tree
packages = setuptools.find_packages(
    where="packages", include=["pyre*", "journal*", "merlin*", "mpi*", "gsl*", "survey*", "cuda*"]
)

# invoke
skbuild.setup(
    # the version derived from the git tag
    version=pyreVersion,
    # the python packages, and where their sources are
    packages=packages,
    package_dir={"": "packages"},
    # for cmake
    cmake_args=[
        # pybind11
        f"-Dpybind11_DIR={pybind11.get_cmake_dir()}",
        # pyre version, in case the build happens outside the git repo
        f"-DPYRE_VERSION={cmakeVersion}",
        # put packages in {site-packages}
        f"-DPYRE_DEST_PACKAGES={packageDir}",
    ],
)

# end of file
