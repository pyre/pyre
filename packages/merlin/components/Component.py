# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import pyre


# declaration
class Component(pyre.component, hidden=True):
    """
    Minor merlin specific embellishment of the {pyre.Component} base class
    """


    # public data
    merlin = None # access to the merlin executive


    @property
    def vfs(self):
        """
        Convenient access to the application fileserver
        """
        # merlin knows
        return self.merlin.vfs


    # meta methods`
    def __init__(self, name, **kwds):
        super().__init__(name=name, **kwds)

        # if I have a name
        if name:
            # access the journal package
            import journal
            # build and activate my channels
            self.info = journal.info(name).activate()
            self.warning = journal.warning(name).activate()
            self.error = journal.error(name).activate()

        # all done
        return


# end of file 
