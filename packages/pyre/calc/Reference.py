# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


class Reference:
    """
    A node that refers to another node
    """

    # constants
    category = "reference"

    # classifiers
    @property
    def references(self):
        """
        Return a sequence over the nodes in my dependency graph that are references to other nodes
        """
        # i am one
        yield self
        # nothing further
        return

    # value management
    def getValue(self):
        """
        Compute and return my value
        """
        # get my referent
        (referent,) = self.operands
        # if i hand over what my referent holds, rather than what it makes of it
        if self.unprocessed:
            # skip its postprocessor
            return referent.getUnprocessedValue()
        # otherwise, ask him for his value
        return referent.value

    def detach(self):
        """
        Stop following my referent, and keep what i hold
        """
        # stop listening for changes to my referent
        self.ignore(observables=self.operands)
        # and stop following it
        self.keep = False
        # all done
        return self

    def setValue(self, value):
        """
        Set the value of the node i refer to
        """
        # get my referent
        (referent,) = self.operands
        # set its value
        referent.value = value
        # all done
        return self

    # support for graph traversals
    def identify(self, authority, **kwds):
        """
        Let {authority} know I am a reference
        """
        # invoke the callback
        return authority.onReference(reference=self, **kwds)

    # meta-methods
    def __init__(self, unprocessed=False, keep=False, **kwds):
        """
        Refer to my operand; with {unprocessed}, my value is what my referent holds before its
        postprocessor sees it, so that my own postprocessor is the only one it goes through; with
        {keep}, i follow my referent until my client reads my value and {detach}es me
        """
        # chain up
        super().__init__(**kwds)
        # remember what i hand over
        self.unprocessed = unprocessed
        # and whether i follow my referent only until i am read
        self.keep = keep
        # all done
        return


# end of file
