# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Probe:
    """
    The base class for objects that observe the values of nodes in a calc graph
    """


    def activate(self, node):
        """
        The callback that gets invoked when one of the monitored nodes receives a new value
        """
        # if i am not supposed to stay quiet
        if not self._isSilent:
            print("probe@{:#x}: node@{:#x}: value={2}".format(id(self), id(node), node.value))
        return


    def insert(self, node):
        """
        Monitor node
        """
        # add myself the pile of {node} observers
        node.addObserver(self.activate)
        # add the node to the set of nodes i am monitoring
        self._nodes.add(node)
        # and return
        return


    def retract(self, node):
        """
        Stop monitoring node
        """
        # remove my callback from the pile of {node} obervers
        node.removeObserver(self.activate)
        # remove node from my pile
        self._nodes.remove(node)

        return


    def patch(self, old, new):
        """
        Stop watching {old} and start monitoring {new}
        """
        # drop the {old} observable
        self._nodes.discard(old)
        # add the {new} one
        self._nodes.add(new)
        # and return
        return self


    def finalize(self):
        """
        Stop monitoring all nodes and prepare for shutdown
        """
        # extract me from all the nodes i monitor
        for node in self._nodes:
            node.removeObserver(self.activate)
        # and clear out my node pile    
        self._nodes = None

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
