# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2025 all rights reserved
#


class GSLError(Exception):
    """
    Base class for all GSL related errors
    """

    # meta-methods
    def __str__(self):
        # return the error description
        return self.description


# end of file
