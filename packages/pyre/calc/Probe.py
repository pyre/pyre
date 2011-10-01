# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Probe:
    """
    The base class for objects that observe the values of nodes in a calc graph
    """


    def flush(self, node):
        """
        The callback that gets invoked when one of the monitored nodes receives a new value
        """
        # if i am not supposed to stay quiet
        if not self._isSilent:
            # print the value of the node
            print("probe@{:#x}: node@{:#x}: value={}".format(id(self), id(node), node.value))
        # and return
        return


    def insert(self, node):
        """
        Monitor node
        """
        # add myself the pile of {node} observers
        node.addObserver(self)
        # add the node to the set of nodes i am monitoring
        self._nodes.add(node)
        # and return
        return


    def retract(self, node):
        """
        Stop monitoring node
        """
        # remove my callback from the pile of {node} obervers
        node.removeObserver(self)
        # remove node from my pile
        self._nodes.remove(node)

        return


    def __init__(self, isSilent=False, **kwds):
        super().__init__(**kwds)
        self._nodes = set()
        self._isSilent = isSilent
        return


    # data
    _nodes = None
    _isSilent = False


# end of file 
