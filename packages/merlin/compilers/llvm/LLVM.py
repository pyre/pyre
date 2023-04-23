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


# the base compiler from the LLVM compiler suite
class LLVM(Unix):
    """
    Common base for compilers from the LLVM compiler suite
    """

    # constants
    suite = "llvm"
    language = None
    tag = None

    # configurable state
    driver = merlin.properties.path()
    driver.default = "clang"
    driver.doc = "the path to the compiler executable"

    # implementation details
    _version_regex = re.compile(
        "".join(
            [
                r"(?P<tag>.+)\s+version\s+",
                r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<micro>\d+)",
            ]
        )
    )


# end of file
