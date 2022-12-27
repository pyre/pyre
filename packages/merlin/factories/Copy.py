# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
# framework
import merlin
# superclass
from .Factory import Factory


# creates a directory an a filesystem
class Copy(Factory, family="merlin.factories.cp"):
    """
    Copy a file from one location to another
    """


    # inputs
    source = merlin.protocols.file.input()
    source.default = None
    source.doc = "the source file"

    within = merlin.protocols.directory.input()
    within.default = None
    within.doc = "the containing directory at the destination"

    # output
    destination = merlin.protocols.file.output()
    destination.default = None
    destination.doc = "the destination file"


    # protocol obligations
    @merlin.export
    def pyre_make(self, **kwds):
        """
        Construct my products
        """
        # the trivial implementation here is just a place for a breakpoint while debugging
        # it will be removed at some point...
        # chain up
        return super().pyre_make(**kwds)


    # framework hooks
    def pyre_run(self, **kwds):
        """
        Make the subdirectory
        """
        # marker
        indent = " " * 2
        # sign on
        print(f"{indent*1}[cp] {self.destination.path}")

        # all done
        return


# end of file
