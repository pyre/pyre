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
        # get the file category
        category = file.category
        # ask it to identify itself
        category.identify(authority=self, builder=builder, library=library, file=file)
        # all done
        return


    @merlin.export
    def header(self, builder, library, file):
        """
        Handle a {file} asset
        """
        # get the path to the header in the source directory
        origin = file.path
        # form the corresponding path in the prefix
        destination = merlin.primitives.path("/prefix/include") / library.name / origin

        # build the corresponding file based asset
        pub = merlin.assets.file(name=str(destination), path=destination)
        #  decorate it
        pub.category = file.category
        pub.language = file.language
        # index it
        builder.index[pub.pyre_name] = pub
        # and add it to the set of {headers} of the {library}
        library.headers.add(pub)

        # the parent directory of the destination
        parent = destination.parent
        # has a workflow that is guaranteed to exist
        dir = builder.index[str(parent)]

        # handling this header involves copying its contents
        cp = merlin.factories.cp()
        # from the source
        cp.source = file
        # to the destination
        cp.destination = pub
        # subject to the existence of the parent directory
        cp.within = dir

        # all done
        return


    @merlin.export
    def source(self, builder, library, file):
        """
        Handle a {file} asset
        """
        # all done
        return


    @merlin.export
    def template(self, builder, library, file):
        """
        Handle a {template} asset
        """
        # all done
        return


# end of file
