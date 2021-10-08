# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin

# my superclass
from ..Builder import Builder as BaseBuilder


# the manager of intermediate and final build products
class Builder(BaseBuilder, family="merlin.builders.make"):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # interface
    def add(self, plexus, **kwds):
        """
        Add the given {assets} to the build pile
        """
        # generate the makefile content
        content = self.generate(plexus=plexus, **kwds)

        # grab the stage uri
        stage = plexus.vfs["/stage"].uri
        # form the path to the makefile
        makefile = stage / "Makefile"
        # open the stream

        stream = open(makefile, "w")
        # and write
        print('\n'.join(content), file=stream)

        # all done
        return


    # framework hooks
    def merlin_initialized(self, plexus, **kwds):
        """
        Hook invoked after the {plexus} is fully initialized
        """
        # chain up
        super().merlin_initialized(plexus=plexus, **kwds)

        # grab my abi
        abi = self.abi(plexus=plexus)
        # and the root of the virtual filesystem
        vfs = plexus.vfs

        # prep the stage area
        self.setupStage(vfs=vfs, abi=abi)
        # and the prefix
        self.setupPrefix(vfs=vfs, abi=abi)

        # all done
        return


    # implementation details
    def setupStage(self, vfs, abi):
        """
        Set up the staging area for build temporaries
        """
        # get the user's home directory
        home = self.pyre_user.home
        # and the workspace path
        ws = vfs["/workspace"].uri
        # attempt to
        try:
            # project the workspace onto the user's home
            rel = ws.relativeTo(home)
        # if this fails
        except ValueError:
            # just use the trailing part of the workspace
            rel = [ws.name]

        # we will hash the workspace
        wshash = "~".join(rel)

        # build the stage path
        stage = self.stage / wshash / abi / self.tag
        # force the creation of the directory
        stage.mkdir(parents=True, exist_ok=True)
        # use it to anchor a local filesystem
        stageFS = vfs.retrieveFilesystem(root=stage)
        # build the canonical location for the stage in the virtual filesystem
        stagePath = merlin.primitives.path("/stage")
        # and mount it at its canonical location
        vfs[stagePath] = stageFS

        # all done
        return


    def setupPrefix(self, vfs, abi):
        """
        Set up the installation area
        """
        # check whether the users wants the ABI folded into the prefix
        prefix = self.prefix / abi / self.tag if self.tagged else self.prefix
        # force the creation of the actual directory
        prefix.mkdir(parents=True, exist_ok=True)
        # use it as an anchor for a local filesystem
        prefixFS = vfs.retrieveFilesystem(root=prefix)
        # build the canonical location for the prefix
        prefixPath = merlin.primitives.path("/prefix")
        # and mount the filesystem there
        vfs[prefixPath] = prefixFS

        # all done
        return


    # makefile generation
    def generate(self, **kwds):
        """
        Generate the makefile
        """
        # preamble
        yield from self.preamble(**kwds)
        # postamble
        yield from self.postamble(**kwds)
        # all done
        return


    def preamble(self, **kwds):
        """
        Generate the makefile preamble with all the boilerplate code
        """
        # sign on
        yield "# -*- Makefile -*-"
        # all done
        return


    def postamble(self, **kwds):
        """
        Generate the makefile preamble with all the boilerplate code
        """
        # close out the content
        yield ""
        yield "# end of file"
        # all done
        return


    # asset visitors
    def library(self, library):
        """
        Build a {library}
        """
        # do nothing, for now
        return


# end of file
