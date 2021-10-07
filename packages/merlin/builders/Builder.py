# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# the manager of intermediate and final build products
class Builder(merlin.component, implements=merlin.protocols.builder):
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

    layout = merlin.protocols.prefix()
    layout.doc = "the layout of the installation area"


    # interface
    def add(self, assets):
        """
        Add the given {asset} to the build pile
        """
        # go through the assets
        for asset in assets:
            # ask each one to identify itself
            asset.identify(visitor=self)
        # all done
        return


    def build(self, assets):
        """
        Build the products
        """
        # go through the assets
        for asset in assets:
            # ask each one to  identify itself
            asset.build(builder=self)
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


    # implementation details
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


# end of file