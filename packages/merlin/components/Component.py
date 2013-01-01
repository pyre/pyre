# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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

        # prepare the journal
        # access the package
        import journal
        # build the channels
        self.info = journal.info(name)
        self.warning = journal.warning(name)
        self.error = journal.error(name)

        # activate everything, by default
        self.info.active = True
        self.warning.active = True
        self.error.active = True

        # all done
        return


# end of file 
