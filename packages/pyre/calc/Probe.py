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

        if not self._isSilent:
            print("probe@0x{0:x}: node@0x{1:x}: value={2}".format(id(self), id(node), node.value))

        return


    def insert(self, node):
        """
        Monitor node
        """

        node.addObserver(self.activate)
        self._nodes.add(node)
        return


    def retract(self, node):
        """
        Stop monitoring node
        """

        node.removeObserver(self.activate)
        self._nodes.remove(node)

        return


    def replaceObservable(self, old, new):
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

        for node in self._nodes:
            node.removeObserver(self.activate)

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
