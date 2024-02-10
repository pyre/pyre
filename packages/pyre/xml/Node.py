# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# pull in the locator converter
from . import newLocator


# the base class of all document nodes
class Node:
    """
    The base class for parsing event handlers
    """

    # public data
    tag = None
    elements = ()
    namespace = ""

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

        The default implementation looks up the tag in my local dtd, retrieves the associated
        node factory, and invokes it to set up the context for handling its content

        In typical use, there is no need to override this; but if you do, you should make sure
        to return a Node descendant that is properly set up to handle the contents of the named
        tag
        """
        # attempt to
        try:
            # get the handler factory
            factory = self._pyre_nodeIndex[name]
        # if it can't be found
        except KeyError as error:
            # build the report
            msg = f"unknown tag '{name}'"
            # complain
            raise self.DTDError(description=msg) from error

        # otherwise, attempt to
        try:
            # invoke it to get a new node for the parsing context
            node = factory(parent=self, attributes=attributes, locator=locator)
        # if the constructor fails
        except TypeError as error:
            # build the report
            msg = f"could not instantiate handler for node '{name}'; extra attributes?"
            # complain
            raise self.DTDError(description=msg) from error
        # if the tag lookup fails
        except KeyError as error:
            # build the report
            msg = f"node '{name}': unknown attribute '{error.args[0]}'"
            # complain
            raise self.DTDError(description=msg) from error

        # if all goes well, return the new node
        return node

    def newQNode(self, *, name, namespace, attributes, locator):
        """
        The handler invoked when the opening tag for one of my namespace qualified children is
        encountered.

        See Node.newNode for details
        """
        # attempt to
        try:
            # get the handler factory
            factory = self._pyre_nodeQIndex[(name, namespace)]
        # if it can't be found
        except KeyError as error:
            # build the report
            msg = f"unknown tag '{name}'"
            # complain
            raise self.DTDError(description=msg) from error

        # if we found it, attempt to
        try:
            # invoke it to get a new node for the parsing context
            node = factory(parent=self, attributes=attributes, locator=locator)
        # if the constructor fails
        except TypeError as error:
            # build the report
            msg = f"could not instantiate handler for node '{name}'; extra attributes?"
            # complain
            raise self.DTDError(description=msg) from error
        # if the tag lookup fails
        except KeyError as error:
            # build the report
            msg = f"node '{name}': unknown attribute '{error.args[0]}'"
            # complain
            raise self.DTDError(description=msg) from error

        # if all goes well, return the new node
        return node

    # metamethods
    def __init__(self, parent=None, attributes=None, locator=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # all done
        return

    def notify(self, *, parent, locator):
        """
        The handler that is invoked when the parser encounters my closing tag
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must override 'notify'"
        )

    # turn the locator factory into a method of mine
    newLocator = staticmethod(newLocator)

    # exceptions
    from .exceptions import DTDError

    # private data
    _pyre_nodeIndex = None
    _pyre_nodeQIndex = None


# end of file
