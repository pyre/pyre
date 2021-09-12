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
    prefix.default = "/tmp/{pyre.user.username}/products"
    prefix.doc = "the installation location of the final build products"

    stage = merlin.properties.path()
    stage.default = "/tmp/{pyre.user.username}/builds"
    stage.doc = "the location of the intermediate, disposable build products"

    prefixLayout = merlin.protocols.prefix()
    prefixLayout.doc = "the layout of the installation area"


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # grab the root of the virtual filesystem
        vfs = self.pyre_fileserver

        # get my prefix
        prefix = self.prefix
        # create it, if it doesn't already exist
        prefix.mkdir(parents=True, exist_ok=True)
        # anchor a filesystem
        prefix = vfs.retrieveFilesystem(root=prefix)
        # and mount it
        vfs["prefix"] = prefix

        # repeat for my staging area
        stage = self.stage
        # create it, if it doesn't already exist
        stage.mkdir(parents=True, exist_ok=True)
        # anchor a filesystem
        stage = vfs.retrieveFilesystem(root=stage)
        # and mount it
        vfs["stage"] = stage

        # all done
        return


# end of file
