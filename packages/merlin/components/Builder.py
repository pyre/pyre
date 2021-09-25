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

    tagged = merlin.properties.bool()
    tagged.default = True
    tagged.doc = "control whether to fold the compiler ABI into the installation prefix"

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

    libflow = merlin.protocols.libflow()
    libflow.doc = "the library workflow generator"


    # interface
    def add(self, asset):
        """
        Add the given {asset} to the build pile
        """
        # ask the asset to identify itself
        asset.identify(authority=self)
        # all done
        return


    def build(self):
        """
        Build the products
        """
        # all done
        return


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # make a container for my products and factories
        self.flow = merlin.flow.dynamic()
        # and an index for my named assets
        self.index = {}

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
        # grab my abi
        abi = self.abi(plexus=plexus)
        # and the root of the virtual filesystem
        vfs = self.pyre_fileserver

        # prep the stage area
        self.setupStage(vfs=vfs, abi=abi)
        # and the prefix
        self.setupPrefix(vfs=vfs, abi=abi)
        # all done
        return

    # implementation details
    def library(self, library):
        """
        Build a {library}
        """
        # delegate to the {libflow} generator
        return self.libflow.library(builder=self, library=library)


    # helpers
    def abi(self, plexus):
        """
        Make a tag that reflects the platform and compiler choice
        """
        # we are looking to tag the build using information about the compilers in use
        # this is really a poorly stated problem with many possible variables that could
        # affect the binary compatibility of the build products; we punt and use the c++ or c
        # compiler as the dominant factor
        # so
        determinant = None
        # get the set of compilers and go through them
        for compiler in plexus.compilers:
            # if this is the c++ compiler
            if compiler.language == "c++":
                # mark it as the determining compiler
                determinant = compiler
                # we are done
                break
            # the c compiler
            if compiler.language == "c":
                # is a fallback
                determinant = compiler
        # if we didn't manage to find anything useful
        if determinant is None:
            # we won't add abi information to the products
            return ""
        # otherwise, get the compiler family
        suite = compiler.suite
        # and its version
        major, _, _ = compiler.version()
        # and fold them into the ABI
        abi = f"{suite}{major}"
        # all done
        return abi


    def setupPrefix(self, vfs, abi):
        """
        Build a workflow that assembles my prefix layout
        """
        # there are three things to do
        # - force the creation of the prefix directory in the local filesystem
        # - build and index a flow product to serve as an anchor for elaborating the directory
        #   structure under prefix
        # - traverse the prefix layout and build/index flows that create the subdirectories
        #   when needed

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
        layout = self.prefixLayout
        # its entire configurable state is supposed to be subdirectories of prefix
        # so go through it
        for trait in layout.pyre_configurables():
            # the trait name specifies the mount point in the virtual filesystem
            name = trait.name
            # and its value is the path under {prefix} in the physical filesystem
            relpath, locator = layout.pyre_getTrait(alias=name)
            # project it to its canonical location
            path = prefixPath / relpath
            # make a pile of the intermediate directories that don't exist and must be created
            pile = []
            # find the closest ancestor that is a known flow product by going through
            # the path breadcrumbs
            for parent in path.crumbs:
                # form the asset name
                parentName = str(parent)
                # attempt to look it up in the asset index
                parentDir = index.get(parentName)
                # if its there
                if parentDir:
                    # got it; look no further
                    break
                # if not, add the directory name to the pile of intermediate directories
                # we have to build
                pile.append(parent.name)
            # if we reached the root for the virtual filesystem without bumping into an
            # existing directory
            else:
                # there is something wrong, since we should have run into {/prefix}, which
                # we just built in the previous step; most likely this is a bug, so make a channel
                channel = journal.firewall("merlin.builder")
                # and complain
                channel.line(f"could not anchor '{path}'")
                channel.line(f"while building a workflow for '{name}' in the prefix layout")
                channel.line(f"with value '{relpath}' from {locator}")
                channel.line(f"when a directory asset for '/prefix' should have been found")
                channel.line(f"crumbs: {', '.join(reversed(pile))}")
                channel.line(f"note: this workflow is compromised; please file an issue on github")
                # flush
                channel.log()
                # bail, just in case this firewall is not fatal
                return
            # if we get this far, we have {parentDir} with a flow directory product that
            # already exists, and a {pile} of intermediate directories for which we must
            # build nodes and attach them to the workflow; go through the pile
            for dir in reversed(pile):
                # build the path to this child
                childPath = parentDir.path / dir
                # which becomes the asset name
                childName = str(childPath)
                # create the flow node for this child
                childDir = merlin.assets.directory(name=childName, node=None, path=childPath)
                # add it to my flow products
                flow.products.add(childDir)
                # and index it so it is a retrievable asset
                index[childDir.pyre_name] = childDir
                # this node gets realized by a factory
                mkdir = merlin.factories.mkdir()
                # that builds the intermediate directory
                mkdir.name = dir
                # as a child of the parent product
                mkdir.parent = parentDir
                # to form the child product
                mkdir.child = childDir
                # adjust the cursor for the next go around
                parentDir = childDir
                # move on; if this is the last iteration, we get out of here with
                # {childDir} holding the terminal node that corresponds to this subdirectory

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
                index[canonicalPath] = childDir

        # all done
        return


    def setupStage(self, vfs, abi):
        """
        Build a workflow that creates the staging are for the intermediate build products
        """
        # first, we have to create the stage area in the physical filesystem and mount it
        # at its canonical location in the virtual filesystem
        # start by assembling the path to the staging area
        stage = self.stage / abi / self.tag
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
