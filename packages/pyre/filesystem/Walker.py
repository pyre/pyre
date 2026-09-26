# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# class declaration
class Walker:
    """
    Class that encapsulates listing the contents of a local directory
    """

    # exceptions
    from .exceptions import DirectoryListingError

    # interface
    @classmethod
    def walk(cls, path):
        """
        Assume {path} is a directory, get the names of its contents and iterate over them
        """
        # attempt
        try:
            # to get the contents, all at once, so a directory that cannot be read is reported
            # here rather than halfway through the iteration, where nobody can tell it apart
            # from any other failure
            return list(path.contents)
        # if this fails
        except OSError as error:
            # raise a package specific exception
            raise cls.DirectoryListingError(uri=path, error=str(error))


# end of file
