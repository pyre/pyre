# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin


# a builder of libraries
class LibFlow(merlin.component,
              family="merlin.builders.flow.lib", implements=merlin.protocols.libflow):
    """
    Workflow generator for building libraries
    """


    # interface
    # asset handlers
    @merlin.export
    def library(self, library, **kwds):
        """
        Generate the workflow that builds a {library}
        """
        # show me
        # go through the assets of the library
        for asset in library.assets():
            # and add each one to the build pile
            asset.identify(visitor=self, library=library, **kwds)
        # all done
        return


    @merlin.export
    def directory(self, builder, library, directory, **kwds):
        """
        Handle a source {directory}
        """
        # all headers go to the {include} directory in {prefix}
        include = merlin.primitives.path("/prefix/include")
        # get the special scope
        scope = library.scope
        # if one exists
        if scope:
            # place the headers in a subdirectory that includes this extra scope
            anchor = scope / library.name
        # otherwise
        else:
            # just the library name
            anchor = library.name
        # there may be headers to move, so build the corresponding directory in the prefix
        incpath = include / anchor / directory.path
        # ask the builder to assemble a workflow that creates this directory
        builder.mkdir(path=incpath)
        # all done
        return


    @merlin.export
    def file(self, file, **kwds):
        """
        Handle a {file} asset
        """
        # get the file category
        category = file.category
        # ask it to identify itself
        category.identify(visitor=self, file=file, **kwds)
        # all done
        return


    # asset category handlers
    @merlin.export
    def header(self, builder, library, file, **kwds):
        """
        Handle a {file} asset
        """
        # all headers are anchored at
        include = merlin.primitives.path("/prefix/include")
        # get my name
        name = library.name
        # the special scope, if any
        scope = library.scope
        # and the name of the gateway header
        gateway = library.gateway

        # get the path to the header in the source directory
        origin = file.path

        # if i've been asked to place my headers in a special scope
        if scope:
            # and this file is the gateway header
            if origin == gateway:
                # the destination is
                destination = include / scope / origin
            # everything else
            else:
                # is placed in a path that includes my name
                destination = include / scope / name / origin
        # if there is no special scope
        else:
            # form the corresponding path in the prefix
            destination = include / name / origin

        # build the corresponding file based asset
        dst = merlin.assets.file(name=str(destination), path=destination)
        #  decorate it using information from the source {file}
        dst.category = file.category
        dst.language = file.language
        # index it
        builder.index[dst.pyre_name] = dst
        # and add it to the set of {headers} of the {library}
        library.headers.add(dst)

        # the parent directory of the destination
        parent = destination.parent
        # has a workflow that is guaranteed to exist
        dir = builder.index[str(parent)]

        # handling this header involves copying its contents
        cp = merlin.factories.cp()
        # from the source
        cp.source = file
        # to the destination
        cp.destination = dst
        # subject to the existence of the parent directory
        cp.within = dir

        # all done
        return


    @merlin.export
    def source(self, file, **kwds):
        """
        Handle a {file} asset
        """
        # get the language
        language = file.language
        # and ask it to identify itself
        language.identify(visitor=self, file=file, **kwds)
        # all done
        return


    @merlin.export
    def template(self, **kwds):
        """
        Handle a {template} asset
        """
        # all done
        return


    @merlin.export
    def unrecognizable(self, **kwds):
        """
        Handle an {unrecognizable} asset
        """
        # all done
        return


    # source language handlers
    @merlin.export
    def language(self, file, language, **kwds):
        """
        Handle a source file from an unsupported language
        """
        print(f"  [{language.name}] {file.path}")
        # all done
        return


# end of file
