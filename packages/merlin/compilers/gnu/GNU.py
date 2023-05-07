# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import re
import subprocess

# framework
import merlin

# superclass
from ..base.Unix import Unix


# the base compiler for the GNU compiler suite
class GNU(Unix):
    """
    Common base for compilers from the GNU compiler suite
    """

    # constants
    suite = "gcc"
    language = None
    tag = None

    # configurable state
    driver = merlin.properties.path()
    driver.default = "gcc"
    driver.doc = "the path to the compiler executable"

    # implementation details
    _version_regex = re.compile(
        "".join(
            [
                r"(?P<tag>.+)",
                r"\s+(?P<build>\(.*\))\s+",
                r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<micro>\d+)",
            ]
        )
    )


# end of file
