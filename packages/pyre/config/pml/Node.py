# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from pyre.xml.Node import Node as Base


class Node(Base):
    """
    Base class for the handlers of the pml reader
    """


    # types
    from ..events import Assignment, ConditionalAssignment, Source


    # constants
    separator = '.'
    namespace = "http://pyre.caltech.edu/releases/1.0/schema/fs.html"


# end of file
