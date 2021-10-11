# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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
    def library(self, renderer, library, **kwds):
        """
        Generate the workflow that builds a {library}
        """
        # get the name of the library
        name = library.pyre_name

        # sign on
        yield ""
        yield renderer.commentLine(f"building {name}")

        # make the anchor rule
        yield f"{name}: {name}.headers {name}.archive"

        # all done
        return
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
    def language(self, **kwds):
        """
        Handle a source file from an unsupported language
        """
        # all done
        return


# end of file
