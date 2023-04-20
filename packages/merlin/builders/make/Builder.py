# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import datetime

# support
import merlin

# superclasses
from ..Builder import Builder
from .Generator import Generator

# my parts
from .Layout import Layout
from .Librarian import Librarian
from .Preamble import Preamble


# the manager of intermediate and final build products
class Builder(Builder, Generator, family="merlin.builders.make"):
    """
    The manager of the all build products, both final and intermediate disposables
    """

    # configurable state
    makefile = merlin.properties.path()
    makefile.default = "makefile"
    makefile.doc = "the name of the generated makefile"

    marker = merlin.properties.str()
    marker.default = "the main makefile"
    marker.doc = "the comment marker that identifies this fragment"

    librarian = merlin.protocols.flow.librarian()
    librarian.default = Librarian
    librarian.doc = "the library workflow generator"

    # interface
    def add(self, plexus, **kwds):
        """
        Add the given assets to the build pile
        """
        # get the stage uri
        stage = plexus.vfs["/stage"].uri
        # build the makefile path
        makefile = stage / self.makefile
        # generate the makefiles
        self.generate(stage=stage, makefile=makefile, **kwds)
        # all done
        return

    # framework hooks
    def _merlin_initialized(self, plexus, **kwds):
        """
        Hook invoked after the {plexus} is fully initialized
        """
        # chain up
        super()._merlin_initialized(plexus=plexus, **kwds)
        # grab my abi
        abi = self.abi(plexus=plexus)
        # prep the stage area
        self._setupStage(plexus=plexus, abi=abi, **kwds)
        # and the prefix
        self._setupPrefix(plexus=plexus, abi=abi, **kwds)
        # all done
        return

    # implementation details
    def _setupStage(self, plexus, abi, **kwds):
        """
        Set up the staging area for build temporaries
        """
        # get the root of the virtual filesystem
        vfs = plexus.vfs
        # hash the workspace into a build tag
        wstag = self._workspaceHash(plexus=plexus)
        # build the stage path
        stage = self.stage / wstag / abi / self.tag
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

    def _setupPrefix(self, plexus, abi, **kwds):
        """
        Set up the installation area
        """
        # get the root of the virtual filesystem
        vfs = plexus.vfs
        # check whether the user wants the ABI folded into the prefix
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

    # asset visitors
    def project(self, **kwds):
        """
        Build a {project}
        """
        return []

    def library(self, **kwds):
        """
        Build a {library}
        """
        # delegate to the {librarian} generator
        return self.librarian.generate(**kwds)

    # makefile generation
    def _generate(self, stage, assets, **kwds):
        """
        Generate the main makefile
        """
        # chain up
        yield from super()._generate()
        # make some room
        yield ""

        # make a preamble generator
        preamble = Preamble(name=f"{self.pyre_name}.preamble")
        # and build the preamble
        yield from preamble.generate(stage=stage)

        # make a layout generator
        layout = Layout(name=f"{self.pyre_name}.dirs")
        # and record the layout
        yield from layout.generate(stage=stage, layout=self.layout)

        # go through the assets
        for asset in assets:
            # and generate makefiles for each one
            yield from asset.identify(visitor=self, stage=stage, **kwds)

        # all done
        return


# end of file
