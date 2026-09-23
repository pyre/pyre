# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Splitter import Splitter

# the devices i assemble
from .Console import Console
from .File import File


# a splitter that writes every entry to the console and to a set of files
class Tee(Splitter):
    """
    Journal device that writes every entry to the console and to a file at each of a set of
    paths
    """

    # constants
    name = "tee"

    # metamethods
    def __init__(self, paths=(), name=name, **kwds):
        # the console comes first, then a file at each path, open for writing
        outputs = [Console()] + [File(path=path) for path in paths]
        # chain up
        super().__init__(outputs=outputs, name=name, **kwds)
        # all done
        return


# end of file
