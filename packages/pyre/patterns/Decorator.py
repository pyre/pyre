# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the base class for pyre decorators
class Decorator:
    """
    A decorator that can be invoked with keyword arguments to collect metadata

    This class assumes it is at the base of any hierarchy that involves it. This is a departure
    from {pyre} norms, but it unavoidable in this case because of the double instantiation
    pattern in {__new__}

    Note that the signature of {__init__} is required to have {factory} as the first positional
    argument: python invokes the decorator with the callable as a positional argument when the
    decorator is invoked raw, i.e. without any arguments

    Subclasses should avoid overriding {__new__}; it should be possible to accomplish everything
    in {__init__}; please update this note with any exceptions
    """


    # public data
    pyre_factory = None # the callable i decorate


    # meta-methods
    def __new__(cls, factory=None, **kwds):
        """
        Trap the invocation with metadata and delay the decoration of the callable
        """
        # if the {factory} is known, it is because the constructor we build below was invoked
        if factory is not None:
            # check that the user gave us something we can decorate
            assert callable(factory), 'please invoke with keyword arguments'
            # and chain up to do the normal thing; swallow any extra arguments, but don't
            # worry, we'll see them again in {__init__}
            return super().__new__(cls)

        # if we don't know the factory, we were invoked with keyword arguments; the strategy
        # here is to return a {Decorator} constructor as the value of this invocation, which
        # accomplishes two things: it gives python something to call when the method
        # declaration is done, and prevents my {__init__} from getting invoked prematurely

        # here is the constructor closure
        def build(factory):
            """
            Convert a component factory into a foundry
            """
            # just build one of my instances
            return cls(factory=factory, **kwds)

        # to hand over
        return build


    def __init__(self, factory, **kwds):
        # swallow any extra arguments and chain up
        super().__init__()
        # appropriate the factory's docstring
        self.__doc__ = factory.__doc__
        # record the callable
        self.pyre_factory = factory
        # all done
        return


    def __call__(self, *args, **kwds):
        # invoke the factory
        value = self.pyre_factory(*args, **kwds)
        # and return the result
        return value


# end of file
