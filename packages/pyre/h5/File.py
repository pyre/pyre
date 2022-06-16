#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# support
import pyre
# superclass
from .Group import Group


# a dataset container
class File(Group):
    """
    An h5 file
    """


    # interface
    def open(self, path, mode):
        """
        Access the h5 file at {path}
        """
        # open the file and attach my handle
        self.pyre_id = pyre.libh5.File(path=str(path), mode=mode)
        # all done
        return self


    # implementation details
    def schema(self):
        """
        Retrieve the schema of the data product
        """
        # i don't have one; force subclasses to define
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'schema'")


# end of file
