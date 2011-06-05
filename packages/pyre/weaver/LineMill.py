# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# my ancestors
from .Mill import Mill
from .LineComments import LineComments


# my declaration
class LineMill(Mill, LineComments):
    """
    A text generator for languages that have line oriented commenting
    """


# end of file 
