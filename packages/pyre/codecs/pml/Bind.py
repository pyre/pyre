# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


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
        parent.createAssignment(key=[self.key], value="\n".join(self.text))
        return


    # meta methods
    def __init__(self, parent, attributes, locator):
        self.key = attributes['property']
        self.text = []
        return


# end of file
