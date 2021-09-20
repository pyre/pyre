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

    prefixABI = merlin.properties.bool()
    prefixABI.default = True
    prefixABI.doc = "control whether to fold the compiler ABI into the installation prefix"

    prefixLayout = merlin.protocols.prefix()
    prefixLayout.doc = "the layout of the installation area"


    # interface
    def add(self, asset):
        """
        Add the given {asset} to the build pile
        """
        # ask the asset to identify itself
        flow = asset.identify(authority=self)
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
            abi = ""
        # otherwise
        else:
            # get the compiler family
            suite = compiler.suite
            # and its version
            major, _, _ = compiler.version()
            # and fold them into the ABI
            abi = f"{suite}{major}"

        # grab the root of the virtual filesystem
        vfs = self.pyre_fileserver

        # if the user want the ABI folded into the prefix
        if self.prefixABI:
            # assemble the path to my prefix
            prefix = self.prefix / abi / self.tag
        # otherwise
        else:
            # assemble the path to my prefix
            prefix = self.prefix
        # create it, if it doesn't already exist
        prefix.mkdir(parents=True, exist_ok=True)
        # anchor a filesystem
        prefix = vfs.retrieveFilesystem(root=prefix)
        # and mount it
        vfs["prefix"] = prefix

        # assemble the path to my staging area
        stage = self.stage / abi /self.tag
        # create it, if it doesn't already exist
        stage.mkdir(parents=True, exist_ok=True)
        # anchor a filesystem
        stage = vfs.retrieveFilesystem(root=stage)
        # and mount it
        vfs["stage"] = stage

        # all done
        return


    # implementation details
    def directory(self, directory):
        """
        Build a {directory}
        """
        # show me
        print(f"building '{directory.pyre_name}', a directory")
        # all done
        return


    def file(self, file):
        """
        Build a {file} base asset
        """
        # show me
        print(f"building '{file.pyre_name}', a {file.category} file")
        # all done
        return


    def library(self, library):
        """
        Build a {library}
        """
        # show me
        print(f"building '{library.name}', a library")
        # go through the assets of the library
        for asset in library.assets():
            # and add each one to the build pile
            asset.identify(authority=self)
        # all done
        return


# end of file
