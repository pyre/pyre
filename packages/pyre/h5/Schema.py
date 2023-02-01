# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import itertools

# superclass
from pyre.patterns.AttributeClassifier import AttributeClassifier

# the base class for my descriptors
from .Object import Object

# support
from .Inventory import Inventory


# dataset harvester
class Schema(AttributeClassifier):
    """
    Harvest dataset descriptors from h5 groups
    """

    # metamethods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build the class record of a new h5 group
        """
        # N.B.:
        #  if there are any additional class variables to be attached to the class record
        #  they must be added carefully to make sure {__setattr__} doesn't trigger
        #  here, for example, we modify {attributes} before chaining up in order to build and
        #  attach the {pyre_identifiers}

        # make room for the identifier resolution table; it will contain all the identifiers that
        # are visible to this class, i.e. not shadowed by superclasses; we will fill it
        # after the class record is built by traversing the {mro} and handling shadowing correctly
        # this table plays the role similar to the {__dict__} in a normal class
        identifiers = Inventory()
        # and add it to the class attributes
        attributes["pyre_identifiers"] = identifiers
        # make a table with the identifiers declated in this class and add it to the attributes
        attributes["pyre_localIdentifiers"] = {
            name: identifier
            for name, identifier in cls.pyre_harvestIdentifiers(attributes=attributes)
        }
        # build the class record and bind all static identifiers
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # resolve the visible identifiers
        identifiers.update(record.pyre_resolveIdentifiers())
        # all done
        return record

    def __setattr__(self, name, value):
        """
        Assign {name} to {value} in one of my instances
        """
        # check whether
        try:
            # {name} is one of the identifiers in my {pyre_identifiers}
            identifier = self.pyre_identifiers[name]
        # if not
        except KeyError:
            # move on
            pass
        # if it is
        else:
            # interpret this assignment as an attempt to set a new default value for it
            identifier.default = value
            # and done
            return
        # if {value} is an {Object} instance
        if isinstance(value, Object):
            # add it to {pyre_identifiers}
            self.pyre_identifiers[name] = value
            # and bind it
            value.__set_name__(cls=self, name=name)

        # chain up to handle normal assignment
        return super().__setattr__(name, value)

    # implementation details
    @classmethod
    def pyre_harvestIdentifiers(cls, attributes):
        """
        Scan {attributes} for identifiers
        """
        # examine the attributes and select the identifiers
        yield from cls.pyre_harvest(attributes=attributes, descriptor=Object)
        # all done
        return

    def pyre_resolveIdentifiers(self):
        """
        Scan the {mro} of the class record in {self} and build a table of visible
        identifiers
        """
        # make a pile of identifier locations that have been previously encountered
        # this helps us make sure that declarations for a given location in subclasses correctly
        # shadow declarations in ancestors
        seen = set()
        # get the full sequence of identifier providers visible to me
        identifiers = itertools.chain(
            # by getting the identifiers from my static structure
            *(
                base.pyre_localIdentifiers.values()
                for base in self.mro()
                if hasattr(base, "pyre_localIdentifiers")
            )
        )
        # go through them
        for identifier in identifiers:
            # get their name
            name = identifier.pyre_name
            # if this location is being shadowed
            if name in seen:
                # move on
                continue
            # otherwise, add it to the pile of {known} locations
            seen.add(name)
            # and send off the {identifier} with its name as the key
            yield identifier.pyre_name, identifier
        # all done
        return


# end of file
