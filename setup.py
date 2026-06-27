#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# external
import os
import pybind11
import skbuild
import sys

from setuptools_scm import get_version


def version() -> str:
    """
    Resolve the package version from the git tag, falling back to the sdist
    metadata when the build happens outside a git checkout.
    """
    try:
        return get_version(root=".", relative_to=__file__)
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

# get the python version
major, minor, *_ = sys.version_info
# tell cmake where to install pyre packages
packageDir = f"lib/python{major}.{minor}/site-packages"

# invoke
skbuild.setup(
    # the version derived from the git tag
    version=pyreVersion,
    # for cmake
    cmake_args=[
        # pybind11
        f"-Dpybind11_DIR={pybind11.get_cmake_dir()}",
        # pyre version, in case the build happens outside the git repo
        f"-DPYRE_VERSION={cmakeVersion}",
        # put packages in {site-packages}
        f"-DPYRE_DEST_PACKAGES={packageDir}",
    ]
)

# end of file
