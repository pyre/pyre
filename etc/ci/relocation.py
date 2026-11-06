#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import argparse
import ctypes
import importlib
import os
import sys

# the description of the program, for the help screen
DESCRIPTION = """
Check that an installed prefix still works after it has been moved: import every extension module
under its python packages, and confirm that the libraries the loader picked for them are the ones
in the moved prefix
"""

# the libraries of ours the extension modules load
LIBRARIES = ("libpyre", "libjournal")


def extensions(packages: str) -> list[str]:
    """
    Collect the dotted names of the extension modules under {packages}
    """
    # the extension modules are the shared objects in the package tree
    names = []
    # visit every folder in the tree
    for folder, _, files in os.walk(packages):
        # and every shared object in it
        for filename in files:
            # skip anything that is not an extension module
            if not filename.endswith(".so"):
                # by moving on to the next one
                continue
            # the module name is the part of the filename before its platform tag
            module = filename.split(".")[0]
            # and its package is the path of its folder relative to the root of the tree
            package = os.path.relpath(folder, packages).replace(os.sep, ".")
            # put them together
            names.append(f"{package}.{module}")
    # sort them, so the report is stable
    names.sort()
    # and hand them off
    return names


def loaded() -> list[str]:
    """
    Collect the paths of the shared libraries loaded in this process
    """
    # on macOS, the dynamic loader enumerates its images
    if sys.platform == "darwin":
        # get the loader
        dyld = ctypes.CDLL(None)
        # its image names are c strings
        dyld._dyld_get_image_name.restype = ctypes.c_char_p
        # collect them
        images = [
            dyld._dyld_get_image_name(index).decode() for index in range(dyld._dyld_image_count())
        ]
        # and hand them off
        return images
    # elsewhere, the memory map of the process names every file mapped into it
    with open("/proc/self/maps") as stream:
        # the path, when there is one, is the sixth field of each line
        images = {fields[5] for fields in map(str.split, stream) if len(fields) > 5}
    # hand them off
    return sorted(images)


def main() -> int:
    """
    Import the extension modules of a moved prefix and check where their libraries came from
    """
    # build the parser
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    # the moved prefix
    parser.add_argument("prefix", help="the prefix, at its new location")
    # parse the command line
    arguments = parser.parse_args()
    # the prefix, in the spelling the loader reports
    prefix = os.path.realpath(arguments.prefix)
    # its python packages
    packages = os.path.join(prefix, "packages")
    # make them importable
    sys.path.insert(0, packages)

    # collect the failures
    failures = []
    # find the extension modules
    names = extensions(packages)
    # an installation without any is broken in a way this check cannot judge
    if not names:
        # so say so
        failures.append(f"no extension modules under '{packages}'")
    # import each one
    for name in names:
        # attempt to load it
        try:
            # by name
            importlib.import_module(name)
        # a module whose libraries cannot be found does not load
        except ImportError as error:
            # record it
            failures.append(f"{name}: {error}")

    # go through the libraries of ours that the loader picked
    for image in loaded():
        # skip the ones that are not ours
        if not os.path.basename(image).startswith(LIBRARIES):
            # by moving on to the next one
            continue
        # ours must come from the moved prefix
        if not os.path.realpath(image).startswith(prefix + os.sep):
            # record the ones that do not
            failures.append(f"{image}: loaded from outside '{prefix}'")

    # report the failures
    for failure in failures:
        # one per line
        print(failure)
    # and turn them into the exit status
    return 1 if failures else 0


# bootstrap
if __name__ == "__main__":
    # run the check
    status = main()
    # and report its outcome
    raise SystemExit(status)


# end of file
