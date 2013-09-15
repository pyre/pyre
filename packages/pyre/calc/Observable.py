# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import weakref


# class declaration
class Observable:
    """
    Mix-in class that notifies its clients when the value of a node changes
    """

    # public data
    observers = None


    # interface
    def setValue(self, value):
        """
        Override the value setter to notify my observers that my value changed
        """
        # pass the value along
        super().setValue(value)
        # notify my observers
        return self.notifyObservers()


    # observer management
    def addObserver(self, observer):
        """
        Add {observer} to my pile
        """
        # build a weak reference to {observer} and add it to the pile
        self.observers.add(weakref.ref(observer))
        # all done
        return self


    def removeObserver(self, observer):
        """
        Remove {observer} from my pile
        """
        # build a weak reference to {observer} and remove it from the pile
        self.observers.remove(weakref.ref(observer))
        # all done
        return self


    def replace(self, obsolete):
        """
        Remove {obsolete} from its upstream graph and assume its responsibilities
        """
        # iterate over the observers of the {obsolete} node
        for oref in tuple(obsolete.observers):
            # get the actual node
            observer = oref()
            # skip dead nodes
            if observer is None: continue
            # ask the observer to replace {obsolete} with me
            observer.substitute(current=obsolete, replacement=self)
        # all done
        return super().replace(obsolete=obsolete)
        

    # signaling
    def notifyObservers(self):
        """
        Notify the nodes that depend on me that my value has changed
        """
        # initialize the list of dead references
        discard = []
        # for each registered observer reference
        for ref in self.observers:
            # unwrap the weak reference
            observer = ref()
            # if the observer is still alive
            if observer is not None:
                # notify it
                observer.flush(observable=self)
            # otherwise
            else:
                # put the reference on the discard pile
                discard.append(ref)
        # clean up
        for dead in discard: self.observers.remove(dead)
        # all done
        return self


    def flush(self, observable=None):
        """
        Handler of the notification event from one of my observables
        """
        # let my observer know
        return self.notifyObservers()


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the set of my observers
        self.observers = set() # should have been a weak set, but I can do better...
        # all done
        return


# end of file 
