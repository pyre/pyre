# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# schema
from .PrefixLayout import PrefixLayout


# the manager of intermediate and final build products
class Builder(merlin.protocol, family="merlin.builders"):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # required state
    tag = merlin.properties.str()
    tag.doc = "the name of this build"

    tagged = merlin.properties.bool()
    tagged.doc = "control whether to fold the compiler ABI into the installation prefix"

    type = merlin.properties.strings()
    type.doc = "the build type"

    stage = merlin.properties.path()
    stage.doc = "the location of the intermediate, disposable build products"

    prefix = merlin.properties.path()
    prefix.doc = "the installation location of the final build products"

    layout = PrefixLayout()
    layout.doc = "the layout of the installation area"


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # choose the default implementer
        return merlin.builders.flow


# end of file
