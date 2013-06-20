# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclasses
from .. import schemata
from .Slotted import Slotted


# declaration
class Facility(Slotted, schemata.component):
    """
    The descriptor for traits that are components
    """


    # Facility is faced with the following problem: the expected results of coercing are
    # different depending on whether the object whose trait is being processed is a component
    # class or a component instance. In the latter case, we want to cast the trait value into
    # an actual component instance that is compatible with the facility requirements; in the
    # former we are happy with either a compatible component declaration or an instance.


    # public data
    @property
    def default(self):
        """
        Access to my default value
        """
        # if the client provided one, use it; otherwise, ask my protocol
        return self._default or self.protocol.pyre_default()


    @property
    def macro(self):
        """
        Return the default strategy for handling expressions in slot values
        """
        # build expressions
        return self.pyre_nameserver.interpolation


    # interface
    def convert(self, value):
        """
        Perform the value conversion specified by my protocol
        """
        # ask my protocol to have ago
        value = self.protocol.pyre_convert(value)
        # and return it
        return value


    def instantiate(self, value, node, incognito=False, **kwds):
        """
        Coerce {value} into an instance of a component compatible with my protocol
        """
        # leave {None} alone
        if value is None: return None
        # run the value through my regular coercion
        value = self.process(value=value, node=node, **kwds)
        # if what I got back is a component instance, we are all done
        if isinstance(value, self.protocol.component): return value

        # get the key of the node
        key = node.key
        # if it has one
        if key:
            # get the nameserver
            nameserver = self.pyre_nameserver
            # decide what I am supposed to name the new component
            name = nameserver.getName(key) if not incognito else None
            # and get the locator from the key metadata
            locator = nameserver.getInfo(key).locator
        # otherwise
        else:
            # we have no name
            name = None
            # and no locator
            locator = None

        # instantiate and return
        return value(name=name, locator=locator)


    # meta-methods
    def __init__(self, protocol, **kwds):
        # chain up
        super().__init__(protocol=protocol, **kwds)
        # build my slot factories
        self.classSlot = self.factory(trait=self, processor=self.process)
        self.instanceSlot = self.factory(trait=self, processor=self.instantiate)
        # add the converter from my protocol to my pile
        self.converters.append(protocol.pyre_convert)
        # all done
        return


    def __str__(self):
        return "{0.name}: a facility with {0.protocol}".format(self)


# end of file 
