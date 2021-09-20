# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import journal
import merlin


# the manager of intermediate and final build products
class Builder(merlin.component,
              family="merlin.builders.builder", implements=merlin.protocols.builder):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # configurable state
    tag = merlin.properties.str()
    tag.default = None
    tag.doc = "the name of this build"

    type = merlin.properties.strings()
    type.default = "debug", "shared"
    type.doc = "the build type"

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

        # if the user didn't specify a tag
        if self.tag is None:
            # make a pile
            tag = []
            # grab the build type and add its parts to the tag
            tag.extend(sorted(self.type))
            # get the host and add its contribution
            tag.append(self.pyre_host.tag)
            # assemble the tag and store it
            self.tag = "-".join(tag)

        # all done
        return


    # framework hooks
    def merlin_initialized(self, plexus, **kwds):
        """
        Hook invoked after the {plexus} is fully initialized
        """
        # grab the root of the virtual filesystem
        vfs = self.pyre_fileserver

        # assemble the path to my prefix
        prefix = self.prefix
        # create it, if it doesn't already exist
        prefix.mkdir(parents=True, exist_ok=True)
        # anchor a filesystem
        prefix = vfs.retrieveFilesystem(root=prefix)
        # and mount it
        vfs["prefix"] = prefix

        # assemble the path to my staging area
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
