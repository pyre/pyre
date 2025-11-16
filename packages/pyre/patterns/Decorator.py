# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import functools
import types


# the base class for pyre decorators
class Decorator:
    """
    The base for decorators that accept arbitrary optional metadata
    """

    # public data
    pyre_method = None  # the method i decorate

    # meta-methods
    def __new__(cls, method=None, **kwds):
        """
        Trap the instantiation of the decorator so we can detect how it was invoked
        """
        # if the {method} being wrapped is known, i was invoked with no extra arguments
        if method is not None:
            # there's nothing special to do here; proceed with building the decorator instance
            return super().__new__(cls)

        # if we don't know {method}, we were invoked with keyword arguments; the strategy here is
        # to return a closure over my constructor as the value of this invocation, which
        # accomplishes two things: it gives python something to call when the method declaration is
        # done, and prevents my {__init__} from getting invoked prematurely

        # build the constructor closure
        def closure(method):
            """
            Decorate {method}
            """
            # just build one of my instances
            return cls(method=method, **kwds)

        # and hand it over
        return closure

    def __init__(self, method, **kwds):
        # chain up
        super().__init__(**kwds)
        # record the method
        self.pyre_method = method
        # appropriate its metadata; but careful not to destroy the __dict__
        # not sure whether this is a python bug, yet. gotta find some time to explore
        functools.update_wrapper(wrapper=self, wrapped=method, updated=())
        # all done
        return

    def __get__(self, instance, cls):
        """
        Bind my {__call__} method to {instance}, if available
        """
        # if the {instance} is trivial
        if instance is None:
            # someone is asking questions of my {cls}; hand me off for inspection
            return self
        # otherwise, rebind {self} to {instance} and return it
        return types.MethodType(self.__call__, instance)

    def __call__(self, *args, **kwds):
        """
        By default, invoke the wrapped {method}
        """
        # invoke the wrapped {method} and return the result
        return self.pyre_method(*args, **kwds)


# end of file
