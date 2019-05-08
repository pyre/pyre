# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# my superclass
from .Status import Status


# declaration
class FactoryStatus(Status):
    """
    A helper that watches over the traits of factories and records value changes
    """


    # interface
    def bindInputs(self, factory):
        """
        Add the status monitors of the {factory} inputs to the pile of my {observables}
        """
        # add the associated status monitors to my pile
        self.observe(observables=factory.pyre_monitors(pile=factory.pyre_inputs))
        # all done
        return


    def replaceInput(self, new, old):
        """
        Replace the {old} input with a {new} one
        """
        # remove me from the list of {old} observers
        old.pyre_status.removeObserver(observer=self)
        # and add to the list of {new} observers
        new.pyre_status.addObserver(observer=self)
        # if the {new} product is stale
        if new.pyre_stale:
            # mark the downstream graph
            self.flush(observable=new.pyre_status)
        # all done
        return


    def replaceOutput(self, new, old):
        """
        Replace the {old} output with a {new} one
        """
        # remove the {old} product from the list of my observers
        self.removeObserver(observer=old.pyre_status)
        # add the new one
        self.addObserver(observer=new.pyre_status)
        # and mark it
        new.pyre_stale = True
        # all done
        return


# end of file
