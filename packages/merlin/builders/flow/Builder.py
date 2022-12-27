# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin

# my superclass
from ..Builder import Builder as BaseBuilder
# my parts
from .LibFlow import LibFlow


# the manager of intermediate and final build products
class Builder(BaseBuilder, family="merlin.builders.flow"):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # configurable state
    libflow = merlin.protocols.libflow()
    libflow.default = LibFlow
    libflow.doc = "the library workflow generator"


    # interface
    def mkdir(self, path):
        """
        Build a workflow that creates a directory at {path}
        """
        # N.B.: this algorithm assumes that {path} has an ancestor for which a fully formed asset
        # already exists and is indexed correctly. the builder currently guarantees that
        # {/prefix} and {/stage} exist, as they are the most common roots for generated assets

        # grab my index
        index = self.index
        # make a pile for the intermediate directories that must be created
        pile = []
        # traverse the {path} upwards towards its root, looking for an anchor
        for crumb in path.crumbs:
            # form the name of the directory asset
            name = str(crumb)
            # look in the {index}
            anchor = index.get(name)
            # if it's there
            if anchor:
                # got it; no need to look further
                break
            # if not, we will have to build this directory, so add its name to the {pile}
            pile.append(crumb.name)
        # if we have reached the root of the filesystem without bumping into an {anchor}
        else:
            # there is something wrong, most likely a bug
            channel = journal.firewall("merlin.builder.mkdir")
            # complain
            channel.line(f"could not anchor '{path}'")
            channel.line(f"crumbs: {', '.join(reversed(pile))}")
            channel.line(f"note: this workflow is compromised; please file an issue on github")
            # and flush
            channel.log()
            # just in case firewalls aren't fatal, bail
            return

        # at this point, we have an {anchor} and a {pile} of intermediate directories that must
        # be constructed; we will index them and store them in my list of flow {products}
        products = self.flow.products
        # go through them in reverse order
        for child in reversed(pile):
            # build the path to this child
            childPath = anchor.path / child
            # use it to form the asset name
            childName = str(childPath)
            # and use these two to form the directory; note that we don't have a filesystem node
            # for this asset, an indication that it doesn't exist yet
            childDir = merlin.assets.directory(name=childName, path=childPath)
            # index it
            index[childName] = childDir
            # and add it to my flow
            products.add(childDir)
            # this directory gets realized using a directory factory
            mkdir = merlin.factories.mkdir()
            # that builds this child
            mkdir.name = child
            # with its parent
            mkdir.parent = anchor
            # to form the subdirectory
            mkdir.child = childDir
            # adjust the cursor for the next level
            anchor = childDir
            # and move on; if this is the last iteration, we get out of here with {anchor}
            # holding the terminal node that corresponds to this subdirectory

        # whether there was a {pile} of intermediate directories or not, {anchor} has the answer
        # and we are all done
        return anchor


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # make a container for my products and factories
        self.flow = merlin.flow.dynamic()
        # and an index for my named assets
        self.index = {}

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

        # prep the stage area
        self.setupStage(plexus=plexus, abi=abi)
        # and the prefix
        self.setupPrefix(plexus=plexus, abi=abi)

        # all done
        return


    # implementation details
    def library(self, **kwds):
        """
        Build a {library}
        """
        # delegate to the {libflow} generator
        return self.libflow.library(builder=self, **kwds)


    # helpers
    def setupPrefix(self, plexus, abi, **kwds):
        """
        Build a workflow that assembles my prefix layout
        """
        # there are three things to do
        # - force the creation of the prefix directory in the local filesystem
        # - build and index a flow product to serve as an anchor for elaborating the directory
        #   structure under prefix
        # - traverse the prefix layout and build/index flows that create the subdirectories
        #   when needed

        # get the root of the virtual filesystem
        vfs = plexus.vfs

        # first, modify the physical filesystem and mount it at its canonical location
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

        # second, the workflows that build the prefix directory structure need an anchor
        # get my flow
        flow = self.flow
        # and my index
        index = self.index
        # build the directory asset
        prefixDir = merlin.assets.directory(name=str(prefixPath), node=prefixFS, path=prefixPath)
        # add it to the flow
        flow.products.add(prefixDir)
        # and index it
        index[prefixDir.pyre_name] = prefixDir

        # finally, build a flow that assembles the directory layout on demand
        # grab the layout
        layout = self.layout
        # its entire configurable state is supposed to be subdirectories of prefix
        # so go through it
        for trait in layout.pyre_configurables():
            # the trait name specifies the mount point in the virtual filesystem
            name = trait.name
            # and its value is the path under {prefix} in the physical filesystem
            relpath, locator = layout.pyre_getTrait(alias=name)
            # project it to its canonical location
            path = prefixPath / relpath
            # create it and all intermediate directories up to {/prefix}, which we created
            # and indexed above
            dir = self.mkdir(path=path)
            # when {mkdir} fails, it raises a firewall; but when the firewall is disabled
            # it returns with a trivial node; in order to assist in debugging
            if not dir:
                # make a channel
                channel = journal.error("merlin.builder.mkdir")
                # complain
                channel.line(f"could not anchor '{path}'")
                channel.line(f"while building a workflow for '{name}' in the prefix layout")
                channel.line(f"with value '{relpath}' from {locator}")
                channel.line(f"when a directory asset for '/prefix' should have been found")
                channel.line(f"note: this workflow is compromised; please file an issue on github")
                # and flush
                channel.log()

            # by now, we have a complete workflow for priming the directory structure under
            # {/prefix}; what is missing is making sure that the target directory nodes are
            # accessible via their canonical name using the name of the trait
            canonicalPath = str(prefixPath / name)
            # most likely, the name of the trait and its canonical path match, so there is already
            # a flow node under that name; try to look for it
            target = index.get(canonicalPath)
            # but if it's not there
            if not target:
                # index the {childDir} node from above under its canonical name
                index[canonicalPath] = dir

        # all done
        return


    def setupStage(self, plexus, abi, **kwds):
        """
        Build a workflow that creates the staging are for the intermediate build products
        """
        # get the root of the virtual filesystem
        vfs = plexus.vfs
        # hash the workspace into a build tag
        wstag = self.workspaceHash(plexus=plexus)

        # first, we have to create the stage area in the physical filesystem and mount it
        # at its canonical location in the virtual filesystem
        # start by assembling the path to the staging area
        stage = self.stage / wstag / abi / self.tag
        # force the creation of the directory
        stage.mkdir(parents=True, exist_ok=True)
        # use it to anchor a local filesystem
        stageFS = vfs.retrieveFilesystem(root=stage)
        # build the canonical location for the stage in the virtual filesystem
        stagePath = merlin.primitives.path("/stage")
        # and mount it at its canonical location
        vfs[stagePath] = stageFS

        # next, we have to adjust the workflow; grab it
        flow = self.flow
        # and my product index
        index = self.index
        # make a directory flow node that refers to this location
        stageDir = merlin.assets.directory(name=str(stagePath), node=stageFS, path=stagePath)
        # add it to the flow
        flow.products.add(stageDir)
        # and index it
        index[stageDir.pyre_name] = stageDir

        # all done
        return


# end of file
