# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
from .. import tracking
# superclass
from .Requirement import Requirement


# class declaration
class Role(Requirement):
    """
    The metaclass for protocols
    """


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new protocol record

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a descendant of {Actor}
            {name}, {bases}, {attributes}: the usual class specification
            {implements}: the tuple of protocols that this component is known to implement
        """
        # save the location of the component declaration
        # N.B.: the locator might be incorrect if the metaclass hierarchy gets deeper
        attributes["pyre_locator"] = tracking.here(1)

        # build and return the record
        return super().__new__(cls, name, bases, attributes, **kwds)


    def __init__(self, name, bases, attributes, *, family=None, **kwds):
        """
        Initialize a new protocol class record
        """
        super().__init__(name, bases, attributes, **kwds)
        # if this protocol is not user visible, there is nothing else to do
        if self.pyre_internal: return

        # if the protocol author specified a family name
        if family:
            # register with the executive
            self.pyre_key = self.pyre_executive.registerProtocolClass(
                family=family, protocol=self, locator=self.pyre_locator)
        # otherwise
        else:
            # i have no registration key
            self.pyre_key = None

        # register with the protocol registrar
        self.pyre_executive.registrar.registerProtocolClass(protocol=self)

        # invoke the registration hook
        self.pyre_classRegistered()

        # invoke the configuration hook
        self.pyre_classConfigured()

        # invoke the initialization hook
        self.pyre_classInitialized()

        # all done
        return


    def __call__(self, **kwds):
        """
        The instantiation of protocol objects creates facility descriptors
        """
        # get the facility factory
        from ..traits.Facility import Facility
        # make one and return it
        return Facility(protocol=self, **kwds)


    def __str__(self):
        # get my family name
        family = self.pyre_family()
        # if i gave one, use it
        if family: return 'protocol {!r}'.format(family)
        # otherwise, use my class name
        return 'protocol {.__name__!r}'.format(self)


# end of file
