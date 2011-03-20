# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import collections
from .Node import Node


class Bind(Node):
    """
    Handler for the bind tag in pml documents
    """

    # constants
    elements = ()


    # interface
    def content(self, text, locator):
        """
        Store the value of the key
        """
        text = text.strip()
        if text:
            self.text.append(text)
        return


    def notify(self, parent, locator):
        """
        Let {parent} now that processing this bind tag is complete
        """
        # make an assignment event
        event = self.Assignment(
            key=self.key, value="\n".join(self.text), locator=self.newLocator(locator))
        # and pass it on to my parent
        parent.assignment(event)
        # all done
        return


    # meta methods
    def __init__(self, parent, attributes, locator):
        self.key = attributes['property'].split(self.separator)
        self.text = []
        return


# end of file
