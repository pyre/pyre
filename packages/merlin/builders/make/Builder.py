# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin

# superclasses
from ..Builder import Builder
from .Generator import Generator

# my parts
from .Layout import Layout
from .Library import Library
from .Preamble import Preamble
from .Project import Project
from .Workspace import Workspace


# the manager of intermediate and final build products
class Builder(Builder, Generator, family="merlin.builders.make"):
    """
    The manager of the all build products, both final and intermediate disposables
    """

    # configurable state
    makefile = merlin.properties.path()
    makefile.default = "Makefile"
    makefile.doc = "the name of the generated makefile"

    libFlow = merlin.protocols.flow.library()
    libFlow.default = Library
    libFlow.doc = "the library workflow generator"

    projFlow = merlin.protocols.flow.project()
    projFlow.default = Project
    projFlow.doc = "the project workflow generator"

    # interface
    def add(self, plexus, **kwds):
        """
        Add the given assets to the build pile
        """
        # get the workspace uri
        ws = plexus.vfs["/workspace"].uri
        # get the stage uri
        stage = plexus.vfs["/stage"].uri

        # make a channel
        channel = journal.info("merlin.builders.make")
        # sign on
        channel.line(f"{self}:")
        channel.line(f"generating makefiles for '{ws}'")
        # flush
        channel.log()

        # form the directory with the makefile fragments
        fragments = stage / "merlin"
        # make sure it exists
        fragments.mkdir(parents=True, exist_ok=True)
        # build the makefile path
        makefile = stage / self.makefile
        # generate the makefiles
        self.generate(plexus=plexus, stage=stage, makefile=makefile, **kwds)

        # and tell the users where the makefiles are
        channel.line(f"makefiles in '{stage}'")
        # flush
        channel.log()

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

    # asset visitors
    def project(self, plexus, project, **kwds):
        """
        Build a {project}
        """
        # make a channel
        channel = journal.help("merlin.builders.make")
        # grab the {plexus} color palette
        palette = plexus.palette
        # delegate to the {projFlow} generator
        yield from self.projFlow.generate(
            plexus=plexus, builder=self, project=project, **kwds
        )
        # go through my libraries
        for library in project.libraries:
            # and generate makefiles for each one
            yield from library.identify(plexus=plexus, visitor=self, **kwds)
        # mark
        channel.log(f"{palette.project}[proj]{palette.normal} {project.pyre_name}")
        # all done
        return

    def library(self, plexus, library, **kwds):
        """
        Build a {library}
        """
        # make a channel
        channel = journal.help("merlin.builders.make")
        # grab the {plexus} color palette
        palette = plexus.palette
        # N.B.:
        #  the {lib} command panel calls this entry point directly
        #  so don't be tempted to eliminate it as superfluous
        #  since libraries are handled as project assets
        # delegate to the {libFlow} generator
        yield from self.libFlow.generate(
            plexus=plexus, builder=self, library=library, **kwds
        )
        # mark
        channel.log(f"{palette.library}[lib]{palette.normal} {library.name}")
        # all done
        return

    # makefile generation
    def _generate(self, stage, assets, **kwds):
        """
        Generate the main makefile
        """
        # chain up
        yield from super()._generate()
        # make some room
        yield ""

        # get my name
        name = self.pyre_name

        # make a preamble generator
        preamble = Preamble(name=f"{name}.preamble")
        # and build the preamble
        yield from preamble.generate(stage=stage, **kwds)

        # make a layout generator
        layout = Layout(name=f"{name}.dirs")
        # and record the layout
        yield from layout.generate(stage=stage, layout=self.layout)

        # make a generator that extract the workspace info
        ws = Workspace(name=f"{name}.ws")
        # and build the makefile
        yield from ws.generate(stage=stage, **kwds)

        # go through the assets
        for asset in assets:
            # and generate makefiles for each one
            yield from asset.identify(visitor=self, stage=stage, **kwds)

        # all done
        return

    # directory layout
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


# end of file
