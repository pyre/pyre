# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access to the framework
import pyre
# superclass
from .Package import Package


# my declaration
class Library(Package):
    """
    Base class for third party libraries
    """


    # user configurable state
    incdir = pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"


    # configuration validation
    @classmethod
    def checkIncdir(cls, package, filenames):
        """
        Verify that the {incdir} trait points to a good location
        """
        # chain up
        yield from cls.checkFolder(category='incdir', folder=package.incdir, filenames=filenames)
        # all done
        return


    @classmethod
    def checkLibdir(cls, package, filenames):
        """
        Verify that the {libdir} trait points to a good location
        """
        # chain up
        yield from cls.checkFolder(category='libdir', folder=package.libdir, filenames=filenames)
        # all done
        return


# end of file
