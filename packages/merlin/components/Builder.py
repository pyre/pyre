# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# the manager of intermediate and final build products
class Builder(merlin.component,
              family="merlin.builders.builder", implements=merlin.protocols.builder):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # required state
    prefix = merlin.properties.path()
    prefix.default = "./products"
    prefix.doc = "the installation location of the final build products"

    stage = merlin.properties.path()
    stage.default = "./builds"
    stage.doc = "the location of the intermediate, disposable build products"


# end of file
