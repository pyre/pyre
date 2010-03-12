# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Observable(object):
    """
    Provide notification support for classes that maintain dynamic associations with multiple
    clients. 

    Observers, i.e. clients of the Observable, register event handlers that will be invoked to
    notify them whenever something interesting happens to the Observable. The nature of what is
    being observed is defined by Observable descendants and their managers. For example,
    instances of pyre.calc.Node are observable by other nodes whose value depends on them so
    that the dependents can be notified about value changes and forced to recopute their own
    value.

    The event handlers are callables that take the observable instance as their single
    argument.

    interface:
      addObserver: registers its callable argument with the list of handlers to invoke
      removeObserver: remove an event handler from the list of handlers to invoke
      notify: invoke the registered handlers in the order in which they were registered
    
    """


    def notify(self):
        """
        Notify all observers
        """
        # build a list before notification, just in case the observer's callback behavior
        # involves removing itself from our callback set
        for callable in tuple(self._observers):
            callable(self)

        return
            

    # callback management
    def addObserver(self, callable):
        """
        Add callable to the set of observers
        """
        self._observers.add(callable)
        return callable


    def removeObserver(self, callable):
        """
        Remove callable from the set of observers
        """
        self._observers.remove(callable)
        return callable


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._observers = set()
        return


    # private data
    _observers = None
    

# end of file 
