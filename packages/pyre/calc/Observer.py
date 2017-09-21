# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# the complement
from .Observable import Observable


# class declaration
class Observer:
    """
    Mix-in class that enables a node to be notified when the value of its dependents change
    """


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


    # implementation details
    def _substitute(self, current, replacement):
        """
        Adjust the operands by substituting {replacement} for {current} in the set of operands
        """
        # flush my cache
        self.flush(observable=self)

        # attempt to
        try:
            # remove me as an observer of the old node
            current.removeObserver(self)
        # if this fails
        except KeyError:
            # it is not an indication of a problem; i may have been here before if i show up
            # more than once in the list of operands of {current}; just move on
            pass

        # add me to the list of observers of the replacement
        replacement.addObserver(self)

        # and ask my superclass to do the rest
        return super()._substitute(current, replacement)


# end of file
