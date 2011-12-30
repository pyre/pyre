# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from .Role import Role
from .Actor import Actor
from .Configurable import Configurable


class Interface(Configurable, metaclass=Role, hidden=True):
    """
    The base class for requirement specifications
    """


    # framework data; inherited from Configurable and repeated here for clarity
    pyre_name = None # the instance name
    pyre_family = () # the user-visible name of my class
    pyre_namemap = None # a map of descriptor aliases to their canonical names
    pyre_localTraits = None # a tuple of all the traits in my declaration
    pyre_inheritedTraits = None # a tuple of all the traits inherited from my superclasses
    pyre_pedigree = None # a tuple of ancestors that are themselves configurables


    @classmethod
    def default(cls):
        """
        The preferred implementation of this interface, in case the user has not provided an
        alternative
        """
        # actual interfaces should override
        return None


    # interface
    @classmethod
    def pyre_cast(cls, value):
        """
        Convert {value} into a component factory that is assignment compatible with me
        """
        # if the value is a string, resolve it
        if isinstance(value, str):
            # get the executive to convert the string in {value} into a {Component} subclass
            value = cls.pyre_executive.retrieveComponentDescriptor(
                uri=value, context=cls, locator=None)
        # if value is not a {Component}, attempt to interpret it as a factory
        if not isinstance(value, Actor):
            # invoke it
            try:
                value = value()
            # if that failed in any way, raise an exception
            except Exception as error:
                msg = "could not convert {!r} into a component".format(value)
                raise cls.CastingError(value=value, description=msg) from error
        # if the value is still not a {Component} raise an error
        if not isinstance(value, Actor):
            msg = "could not convert {!r} into a component".format(value)
            raise cls.CastingError(value=value, description=msg)
        # build a compatibility report
        report = value.pyre_isCompatible(cls)
        # if they are incompatible
        if not report:
            # raise an error
            raise cls.InterfaceError(component=value, interface=cls, report=report)
        # otherwise return it
        return value


    # exceptions
    from .exceptions  import InterfaceError
    from ..schema.exceptions import CastingError


# end of file 
