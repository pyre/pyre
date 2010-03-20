# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Node(object):
    """
    The base class for parsing event handlers
    """


    # public data


    # interface
    def content(self, text, locator):
        """
        The handler for textual data within my body that is not associated with any of my children
        """
        # ignore such text by default
        # this handler may trigger multiple times as text is discovered surrounding the
        # processing of children nodes, or as whitespace is encountered
        return


    def newNode(self, *, name, attributes, locator):
        """
        The handler invoked when the opening tag for one of my children is encountered.

        The default implementation looks up the tag in my local dtd, retrieves the assoociate
        node factory, and invokes it to set up the context for handlingits content

        In typical use, there is no need to override this; but if you do you should make sure
        to return a Node descendant properly set up to handle the contents of the named tag
        """
        # get the handler factory
        factory = self._nodeIndex[name]
        # invoke it to get a new node for the parsingcontext
        node = factory(parent=self, attributes=attributes)
        # and return it
        return node


    def notify(self, *, parent, locator):
        """
        The handler that is invoked when the parser encounters my closing tag 
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'notify'".format(self))


    # private data


# end of file 
