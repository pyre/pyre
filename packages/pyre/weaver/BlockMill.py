# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# my ancestors
from .Mill import Mill
from .BlockComments import BlockComments


# my declaration
class BlockMill(Mill, BlockComments):
    """
    A text generator for languages that have block oriented commenting
    """


# end of file 
