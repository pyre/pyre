# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin


# the manager of intermediate and final build products
class Builder(merlin.component, implements=merlin.protocols.flow.builder):
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

    stage = merlin.properties.path()
    stage.default = "/tmp/{pyre.user.username}/builds"
    stage.doc = "the location of the intermediate, disposable build products"

    prefix = merlin.properties.path()
    prefix.default = "/tmp/{pyre.user.username}/products"
    prefix.doc = "the installation location of the final build products"

    layout = merlin.protocols.flow.prefix()
    layout.doc = "the layout of the installation area"

    # interface
    def add(self, assets, **kwds):
        """
        Add the given {assets} to the build pile
        """
        # go through the assets
        for asset in assets:
            # ask each one to identify itself
            asset.identify(visitor=self, **kwds)
        # all done
        return

    def build(self, **kwds):
        """
        Build the products
        """
        # nothing to do, by default
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

    # implementation details
    # merlin hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a generic builder
        """
        # attempt to
        try:
            # ask the {visitor} for a generic builder handler
            handler = visitor.builder
        # if it doesn't exist
        except AttributeError:
            # this is almost certainly a bug; make a channel
            channel = journal.firewall("merlin.builders.identify")
            # complain
            channel.line(f"unable to find builder support")
            channel.line(
                f"while looking through the interface of '{visitor.pyre_name}'"
            )
            # flush
            channel.log()
            # and fail, just in case firewalls aren't fatal
            return None
        # if it does, invoke it
        return handler(builder=self, **kwds)

    # framework hooks
    def _merlin_initialized(self, plexus, **kwds):
        """
        Hook invoked after the {plexus} is fully initialized
        """
        # nothing to do, by default
        return

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
        suite = determinant.suite
        # and its version
        major, _, _ = determinant.version
        # and fold them into the ABI
        abi = f"{suite}{major}"
        # all done
        return abi

    def _workspaceHash(self, plexus):
        """
        Hash the workspace location and the currently active branch into a build tag
        """
        # get the root of the virtual filesystem
        vfs = plexus.vfs
        # get the user's home directory
        home = self.pyre_user.home
        # and the workspace path
        ws = vfs["/workspace"].uri
        # attempt to
        try:
            # project the workspace onto the user's home and hash it
            hash = "~".join(ws.relativeTo(home))
        # if this fails
        except ValueError:
            # just use the trailing part of the workspace
            hash = ws.name
        # get the source control system
        scs = plexus.scs
        # if we are within a workspace and we support the source control system
        if scs:
            # get the active branch name
            branch = plexus.scs.branch()
            # fold it into the branch
            tag = f"{hash}@{branch}"
            # and return it
            return tag
        # otherwise, return the name hash
        return hash


# end of file
