# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# the manager of intermediate and final build products
class PrefixLayout(merlin.protocol, family="merlin.layouts.prefix"):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # required state
    bin = merlin.properties.path()
    bin.doc = "the location of executables"

    config = merlin.properties.path()
    config.doc = "global package configuration files"

    doc = merlin.properties.path()
    doc.doc = "package documentation"

    etc = merlin.properties.path()
    etc.doc = "host specific files"

    include = merlin.properties.path()
    include.doc = "library header files"

    lib = merlin.properties.path()
    lib.doc = "libraries"

    libexec = merlin.properties.path()
    libexec.doc = "binaries that are meant to be used by other packages"

    share = merlin.properties.path()
    share.doc = "architecture independent package files"

    var = merlin.properties.path()
    var.doc = "runtime files"


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # choose the default implementer
        return merlin.components.fhs


# end of file
