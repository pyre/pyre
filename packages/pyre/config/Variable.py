# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..calc.Node import Node


class Variable(Node):
    """
    The object used to hold the values of all configurable items
    """


    # public data
    priority = (-1,-1)


    # interface
    def assimilate(self, other, alias):
        """
        Replace references to node {other} under the name {alias}, and steal its value if its
        priority is higher than mine
        """
        # print("      priorities: mine={0.priority!r}, hers={1.priority!r}".format(self, other))
        # if {other} has higher priority
        if self.priority < other.priority:
            # print("      overriding")
            # assume its value and priority
            self.value = other.value
            self.priority = other.priority
        # either way, she is redundant; so replace her
        return self.poseAs(node=other, name=alias)


    # meta methods
    def __init__(self, priority=priority, **kwds):
        super().__init__(**kwds)
        self.priority = priority
        return


# end of file 
