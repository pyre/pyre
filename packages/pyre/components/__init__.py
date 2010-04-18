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


# exceptions
from ..framework import FrameworkError


class ComponentError(FrameworkError):
    """
    Base class for component specification errors
    """

    def __init__(self, reason, **kwds):
        super().__init__(**kwds)
        self.reason = reason
        return

    def __str__(self):
        return self.reason


class CategoryMismatchError(ComponentError):
    """
    Exception raised when two configurables have traits by the same name but have different
    categories
    """

    def __init__(self, configurable, target, name, **kwds):
        reason = (
            "category mismatch in trait {0!r} between {1._pyre_name!r} and {2._pyre_name!r}"
            .format(name, configurable, target))
        super().__init__(reason, **kwds)

        self.configurable = configurable
        self.target = target
        self.name = name

        return


class ImplementationSpecificationError(ComponentError):
    """
    Exception raised when the {implements} specification of a component declaration contains
    errors, e.g. classes that don't derive from Interface
    """

    def __init__(self, name, component, errors, **kwds):
        reason = "component {0!r} has a poorly formed implementation specification".format(name)
        super().__init__(reason, **kwds)

        self.component = component
        self.errors = errors

        return


class InterfaceError(ComponentError):
    """
    Exception raised when a component does not implement correctly the interfaces in its
    implementation specification
    """

    def __init__(self, component, interface, report, **kwds):
        reason = (
            "component {0._pyre_family!r} does not implement "
            "interface {1._pyre_name!r} correctly".format(component, interface))
        super().__init__(reason, **kwds)
        
        self.component = component
        self.interface = interface
        self.report = report
        
        return


class TraitNotFoundError(ComponentError):
    """
    Exception raised when a request for a trait fails
    """

    def __init__(self, configurable, name, **kwds):
        reason = "{0._pyre_name!r} doesn't have a trait named {1!r}".format(configurable, name)
        super().__init__(reason, **kwds)

        self.configurable = configurable
        self.name = name

        return


# end of file 
