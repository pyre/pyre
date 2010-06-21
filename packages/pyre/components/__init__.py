# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Components are the fundamental building blocks of application behavior in pyre.

A pyre application is a collection of...

A component consists of the following:

  - public methods, its _interface_, that define its behavior
  - user-configurable properties that control this behavior
  - requirements that capture its dependencies on other components for the
    implementation of its behavior

The interface may be implemented inline as part of the component declaration, or it may be a
thin wrapper over a _core_, one or more instances of other classes whose collaborations form
the implementation of the interface. Which style is more appropriate for your application is
determined by a host of design factors. In typical designs, non-trivial components first show
up at the point where the focus shifts to interactions with the end-user.

The user-configurable properties...

Requirements are expressed in terms of facility traits. Facilities are abstract specifications
of required properties and interfaces. The component expects that by the time its interface is
actually invoked the framework will have bound a compatible component to each one of its
facilities. Default values of such components are typically provided as part of the facility
specification, and the end-user may specify alternatives through the application configuration
mechanisms.

Components go through the following life cycle stages

  - retrieval from a persistent store
  - instantiation
  - registration with the framework
  - configuration of public state with user-supplied values
  - binding of facilities to other components
  - core initialization
  - interface access
  - core finalization
  - disposal of the component instance
 
"""


from .. import schema


# property factories
def array():
    """
    Buld a property descriptor for an array of floats
    """
    from .Property import Property

    descriptor = Property()
    descriptor.type = schema.array
    descriptor.default = ()

    return descriptor


def facility(*, interface):
    """
    Build a facility descriptor
    """
    from .Facility import Facility
    facility = Facility()
    facility.type = interface

    return facility


def float():
    """
    Build a property descriptor for a float
    """
    from .Property import Property

    descriptor = Property()
    descriptor.type = schema.float
    descriptor.default = 0.0

    return descriptor


def int():
    """
    Build a property descriptor of type int
    """

    from .Property import Property

    descriptor = Property()
    descriptor.type = schema.int
    descriptor.default = 0

    return descriptor


def str():
    """
    Build a property descriptor of type str
    """

    from .Property import Property

    descriptor = Property()
    descriptor.type = schema.str
    descriptor.default = ""

    return descriptor


# function decorators
def export(func):
    """
    Function decorator that marks a method as public interface
    """
    from .Behavior import Behavior
    return Behavior(func)


def provides(func):
    """
    Function decorator that marks a method as public interface
    """
    return export(func)


# factories
def newRegistrar(**kwds):
    from .Registrar import Registrar
    return Registrar(**kwds)


# end of file 
