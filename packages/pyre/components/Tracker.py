# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import collections
# the framework
import pyre
# support
from .Revision import Revision
# superclass
from .Monitor import Monitor

# value tracker
class Tracker(Monitor):
    """
    A class that monitors the traits of a set of components and maintains a record of their values
    """


    # interface
    def track(self, component):
        """
        Add the {component} traits to the pile of observables
        """
        # watch the component's traits
        self.watch(component=component)

        # grab my history
        history = self.history
        # get the component inventory so that we can store the current value of its traits
        inventory = component.pyre_inventory
        # and its name server, so we can grab the value metadata
        nameserver = component.pyre_nameserver
        # go through the slots that store the value of its traits
        for slot in inventory.getSlots():
            # grab the key
            key = slot.key
            # if the key is trivial
            if key is None:
                # move on
                continue
            # ask the name server for the slot metadata
            info = nameserver.getInfo(key)
            # save the info
            revision = Revision(value=slot.value, locator=info.locator, priority=info.priority)
            # create a pile and record
            history[key] = [ revision ]

        # all done
        return self


    def playback(self, key):
        """
        Play back the history of a specific trait
        """
        # get the record associated with key and return each entry
        yield from self.history[key]
        # all done
        return


    # hooks
    def flush(self, observable=None, **kwds):
        """
        Handle the notification that the value of {observable} has changed
        """
        # if the observable is another monitor
        if isinstance(observable, pyre.executive.nameserver.node):
            # get the slot key
            key = observable.key
            # ask it for its value
            value = observable.value
            # and the metadata maintained by the name server
            info = observable.pyre_nameserver.getInfo(key)
            # save the info
            revision = Revision(value, locator=info.locator, priority=info.priority)
            # record
            self.history[key].append(revision)

        # chain up
        return super().flush(observable=observable, **kwds)


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my history; it's a dictionary that maps trait keys to a list of revisions
        self.history = collections.defaultdict(list)
        # all done
        return


# end of file
