# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# superclass
from .Descriptor import Descriptor


# a descriptor that defines how a tag is handled
class ElementDescriptor(Descriptor):
    """
    Descriptor class that gathers all the metadata about a document tag that was provided by
    the user during the DTD declaration. It is used by DTD derived classes to decorate the
    Document instance and the tag handlers with the information needed by the Reader so it can
    process XML documents
    """

    # element meta data
    handler = None  # the Node descendant that handles parsing events for this document element
    attributes = ()  # a list of the tag attribute descriptors that encode the document DTD

    # meta methods
    def __init__(self, *, tag, handler, root=False):
        # chain up; use my tag as my name
        super().__init__(name=tag)
        # save the handler
        self.handler = handler
        # and the root marker
        self.root = root
        # all done
        return


# end of file
