#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# external
import pybind11
import skbuild
import sys

# get the python version
major, minor, *_ = sys.version_info
# tell cmake where to install pyre packages
packageDir = f"lib/python{major}.{minor}/site-packages"

# invoke
skbuild.setup(
    # for cmake
    cmake_args=[
        # pybind11
        f"-Dpybind11_DIR={pybind11.get_cmake_dir()}",
        # pyre version, in case the build happens outside the git repo
        f"-DPYRE_VERSION=1.11.2",
        # put packages in {site-packages}
        f"-DPYRE_DEST_PACKAGES={packageDir}",
    ]
)

# end of file
