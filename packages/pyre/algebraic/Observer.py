# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# we build weak references to nodes
import weakref
# superclass
from .Observable import Observable


# class declaration
class Observer(Observable):
    """
    Mix-in class that enables a node to be notified when the value of its dependents change
    """


    # value access
    def setValue(self, value):
        """
        Set my value
        """
        # save my current operands
        operands = self.operands
        # stop observing them
        self.ignore(operands)

        # chain up to change the value; my super-classes may not implement
        super().setValue(value)

        # get the new operands
        operands = self.operands
        # start observing again
        self.observe(operands)
        # all done
        return self


    # interface
    def observe(self, observables):
        """
        Add me as an observer to all {observables}
        """
        # loop through {observables}
        for observable in observables:
            # skip the ones that are not observable
            if not isinstance(observable, Observable): continue
            # add me as an observer to the rest
            observable.addObserver(self)
        # all done
        return


    def ignore(self, observables):
        """
        Stop observing the {observables}
        """
        # loop through {observables}
        for observable in observables:
            # skip the ones that are not observable
            if not isinstance(observable, Observable): continue
            # drop me as an observer from the rest
            observable.removeObserver(self)
        # all done
        return


    # meta-methods
    def __init__(self, operands, **kwds):
        # assume i am a composite
        super().__init__(operands=operands, **kwds)
        # observe my operands
        self.observe(observables=operands)
        # all done
        return


    # implementation details
    def _substitute(self, index, current, replacement):
        """
        Adjust the operands by substituting {replacement} for {current} in the list of operands
        at position {index}
        """
        # flush my cache
        self.flush(observable=self)
        # make a weak reference to myself
        selfref = weakref.ref(self)
        # remove me as an observer of the old node
        # N.B: do it quietly because failure here is not an indication of a problem; i may have
        # been here before if i show up more than once in the list of operands of {current}
        current.observers.discard(selfref)
        # and add me to the list of observers of the replacement
        replacement.observers.add(selfref)
        # and ask my superclass to do the rest
        return super()._substitute(index, current, replacement)


# end of file
