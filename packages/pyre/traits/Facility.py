# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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

    # framework data
    category = "component"
    # predicate that indicates whether this trait is a facility
    isFacility = True

    # public data
    @property
    def default(self):
        """
        Access to my default value
        """
        # get my default value
        default = self._default
        # if it is still at its trivial value
        if default is schemata.component.default:
            # ask my protocol
            return self.protocol.pyre_default
        # otherwise, return it
        return default

    @default.setter
    def default(self, value):
        """
        Set my default value
        """
        # save {value} as the default
        self._default = value
        # all done
        return

    def macro(self, **kwds):
        """
        Return the default strategy for handling expressions in slot values
        """
        # build expressions
        return self.pyre_nameserver.expression(**kwds)

    def native(self, **kwds):
        """
        The strategy for building slots from more complex input values
        """
        # facility values are held in variables
        return self.pyre_nameserver.variable(**kwds)

    # framework hooks triggered by the construction of instances
    # interface
    def coerce(self, value, anonymous=False, **kwds):
        """
        Convert {value} into a component class or instance, honoring my {optional} marker; a
        component class becomes an instance with no name when {anonymous} is set, which is how
        the sequences that hold components coerce their entries
        """
        # get the marker of unsatisfiable protocol defaults
        from ..components.exceptions import DefaultError

        # get my protocol
        protocol = self.protocol
        # attempt to
        try:
            # convert {value} normally
            component = super().coerce(value=value, **kwds)
        # if my protocol could not compute a default
        except DefaultError:
            # facilities marked {optional} bind {None} when nobody has anything better to offer
            if self.optional:
                # and their clients are expected to cope
                return None
            # everybody else fails loudly
            raise
        # a sequence that meets a component class holds an instance of it, with no name, since
        # a user who wants one names it in the specification
        if anonymous and isinstance(component, protocol.actor):
            # so build one
            return protocol.pyre_instantiate(
                spec=value, component=component, name=None, locator=None
            )
        # if all goes well, return the {component}
        return component

    def instantiate(self, value, node, incognito=False, **kwds):
        """
        Coerce {value} into an instance of a component compatible with my protocol
        """
        # save the incoming value specification
        spec = value
        # grab my protocol
        protocol = self.protocol
        # run the value through my regular coercion
        value = self.process(value=value, node=node, **kwds)
        # if {value} results in {None} after initial processing
        if value is None:
            # leave it alone
            return None
        # if what I got back is a component instance
        if isinstance(value, protocol.component):
            # we are all done
            return value

        # get the key of the node
        key = node.key
        # if it has one
        if key:
            # get the name server
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
        return protocol.pyre_instantiate(spec=spec, component=value, name=name, locator=locator)

    def render(self, value, renderer, workload, incognito=False):
        """
        Render {value} using renderer
        """
        # get the name to use
        name = None if incognito else self.name
        # delegate to my protocol
        yield from self.protocol.pyre_render(
            renderer=renderer, name=name, component=value, workload=workload
        )
        # all done
        return

    # meta-methods
    def __init__(self, protocol, optional=False, **kwds):
        # chain up; facilities are required by default, overriding the dormant descriptor
        # setting: a facility that can't be satisfied complains when it is first accessed,
        # unless the client marks it {optional}, in which case it binds {None}
        super().__init__(protocol=protocol, optional=optional, **kwds)
        # build my slot factories
        self.classSlot = self.factory(trait=self, post=self.process)
        # and the factory of the slots of instances
        self.instanceSlot = self.factory(trait=self, post=self.instantiate)
        # add the converter from my protocol to my pile
        self.converters.append(protocol.pyre_convert)
        # repeat with the normalizer
        self.normalizers.append(protocol.pyre_normalize)
        # and the validator
        self.validators.append(protocol.pyre_validate)
        # all done
        return

    def __str__(self):
        # identify me
        return f"{self.name!r}: a facility with {self.protocol}"


# end of file
