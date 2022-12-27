# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import itertools

# superclass
from pyre.patterns.AttributeClassifier import AttributeClassifier

# the base class for my descriptors
from .Identifier import Identifier


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

        # make a table with the known identifiers and add it to the pile of attributes
        attributes["pyre_localIdentifiers"] = {
            name: identifier
            for name, identifier in cls.pyre_harvestIdentifiers(attributes=attributes)
        }
        # make room for the identifier resolution table; we will fill it after the class record
        # is built
        pyre_identifiers = {}
        # and add it to the pile
        attributes["pyre_identifiers"] = pyre_identifiers

        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # resolve the visible identifiers
        pyre_identifiers.update(record.pyre_resolveIdentifiers())

        # all done
        return record

    def __call__(self, **kwds):
        """
        Build an instance of one of my classes
        """
        # build the instance
        location = super().__call__(**kwds)
        # and return the new instance
        return location

    def __setattr__(self, name, value):
        """
        Assign {name} to {value} in one of my instances
        """
        # check whether
        try:
            # {name} is one the identifiers in my {pyre_identifiers}
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

        # if {value} is an {Identifier} instance
        if isinstance(value, Identifier):
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
        yield from cls.pyre_harvest(attributes=attributes, descriptor=Identifier)
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
            # get their location
            location = identifier.pyre_location
            # if this location is being shadowed
            if location in seen:
                # move on
                continue
            # otherwise, add it to the pile of {known} locations
            seen.add(location)
            # and send off the {identifier} with its name as the key
            yield identifier.pyre_name, identifier
        # all done
        return


# end of file
