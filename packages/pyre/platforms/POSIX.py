# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
# superclass
from .Host import Host


# declaration
class POSIX(Host, family='pyre.platforms.posix'):
    """
    Encapsulation of a POSIX host
    """


    # public data
    platform = 'posix'
    distribution = 'unknown'


    # interface
    @classmethod
    def systemdirs(cls):
        """
        Generate a sequence of directories with system wide package installations
        """
        # the default u*ix locations
        yield '/usr'
        # and nothing else
        return


    @classmethod
    def which(cls, filename):
        """
        Search for {filename} through the list of path prefixes in the {PATH} environment variable
        """
        # trivial after python 3.3...
        import shutil
        return shutil.which(filename)


    # feature support
    @classmethod
    def dynamicLibraries(cls, stems):
        """
        Convert the sequence of stems into likely filenames for shared objects
        """
        # go through each one
        return (cls.template_dynamicLibrary.format(cls, stem) for stem in stems)


    @classmethod
    def staticLibraries(cls, stems):
        """
        Convert the sequence of stems into likely filenames for shared objects
        """
        # go through each one
        return (cls.template_staticLibrary.format(cls, stem) for stem in stems)


# end of file
