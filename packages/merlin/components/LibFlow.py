# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import journal
import merlin


# the manager of intermediate and final build products
class LibFlow(merlin.component,
              family="merlin.builders.libflow", implements=merlin.protocols.libflow):
    """
    Workflow generator for building libraries
    """


    # interface
    @merlin.export
    def library(self, builder, library):
        """
        Generate the workflow that builds a {library}
        """
        # show me
        print(f"building '{library.name}', a library")
        # go through the assets of the library
        for asset in library.assets():
            # and add each one to the build pile
            asset.identify(authority=self, builder=builder, library=library)
        # all done
        return


    @merlin.export
    def directory(self, builder, library, directory):
        """
        Handle a source {directory}
        """
        # there may be headers to move, so build the corresponding directory in the prefix
        incpath = merlin.primitives.path("/prefix/include", library.name, directory.path)
        # ask the builder to assemble a workflow that creates this directory
        builder.mkdir(path=incpath)
        # all done
        return


    @merlin.export
    def file(self, builder, library, file):
        """
        Handle a {file} asset
        """
        # show me
        # print(f"building '{file.pyre_name}', a {file.category} file")
        # all done
        return


# end of file
