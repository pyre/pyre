# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# a builder of libraries
class LibFlow(merlin.protocol, family="merlin.builders.libflow"):
    """
    Workflow generator for libraries
    """


    # required interface
    @merlin.provides
    def library(self, builder, library):
        """
        Generate the workflow that builds a {library}
        """


    @merlin.provides
    def directory(self, builder, library, directory):
        """
        Handle a source {directory}
        """


    @merlin.provides
    def file(self, builder, library, file):
        """
        Handle a {file} asset
        """


    @merlin.provides
    def header(self, builder, library, file):
        """
        Handle a {header} file
        """


    @merlin.provides
    def source(self, builder, library, file):
        """
        Handle a {source} file
        """


    @merlin.provides
    def template(self, builder, library, file):
        """
        Handle a {template} file
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # choose the default implementer
        return merlin.builders.flow.libflow


# end of file
