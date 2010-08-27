# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref


class Observable:
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
        for instance, funcs in tuple(self._observers.items()):
            for func in funcs:
                # invoke the callable
                func(instance, self)
        # all done
        return
            

    # callback management
    def addObservers(self, observable):
        """
        Add the observers of {observable} to my pile
        """
        self._observers.update(observable._observers)
        return


    def addObserver(self, callback):
        """
        Add callable to the set of observers
        """
        # extract the caller information from the method
        instance = callback.__self__
        function = callback.__func__
        # get the registered callbacks for this instance
        funcs = self._observers.setdefault(instance, set())
        # add this callback
        funcs.add(function)
        # and return it back to the caller
        return callback


    def removeObserver(self, callback):
        """
        Remove callable from the set of observers
        """
        # extract the caller information from the method
        instance = callback.__self__
        function = callback.__func__
        # attempt to get the regitered callbacks
        try:
            funcs = self._observers[instance]
        except KeyError:
            return callback
        # remove this callable from the set
        funcs.discard(function)
        # and return the callback
        return callback


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._observers = weakref.WeakKeyDictionary()
        return


    # private data
    _observers = None
    

# end of file 
