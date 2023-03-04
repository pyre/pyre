# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import itertools

# superclass
from pyre.patterns.AttributeClassifier import AttributeClassifier

# parts
from .Descriptor import Descriptor
from .Dataset import Dataset
from .Inventory import Inventory

# typing
import typing


# the generator of group structure
class Schema(AttributeClassifier):
    """
    The metaclass that harvests descriptors from group declarations
    """

    # metamethods
    def __new__(cls, name: str, bases: typing.Sequence[type], attributes: dict, **kwds):
        """
        Build the class record of a new h5 group
        """
        # make a table for the locally declared descriptors
        localDescriptors = Inventory(
            cls._pyre_identifyDescriptors(attributes=attributes)
        )
        # and an empty one for all visible descriptors that we will fill out later on
        descriptors = Inventory()
        # add them to the pile of {attributes} of {cls}
        attributes["_pyre_descriptors"] = descriptors
        attributes["_pyre_localDescriptors"] = localDescriptors
        # build the record
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # resolve the visible descriptors
        descriptors.update(record._pyre_resolve())
        # all dons
        return record

    # implementation details
    @classmethod
    def _pyre_identifyDescriptors(cls, attributes: dict):
        """
        Identify all descriptors in the class {attributes}
        """
        # examine {attributes} and select the descriptors
        yield from cls.pyre_harvest(attributes=attributes, descriptor=Descriptor)
        # all done
        return

    def _pyre_resolve(self):
        """
        Scan the {mro} of the class record in {self} and return all visible descriptors
        """
        # make a pile of descriptors
        descriptors = itertools.chain(
            # by chaining together
            *(
                # all locally declared descriptors
                base._pyre_localDescriptors.values()
                # from every base of {self}
                for base in self.mro()
                # that is a descriptor
                if issubclass(base, Descriptor)
            )
        )
        # make a pile of descriptors that have been encountered previously so i can ensure
        # that descriptors in ancestors are shadowed correctly
        seen = set()
        # go through the descriptors
        for descriptor in descriptors:
            # get the name
            name = descriptor._pyre_name
            # if we've bumped into this {name} before
            if name in seen:
                # skip it
                continue
            # otherwise, add it to known pile
            seen.add(name)
            # and send off the descriptor
            yield descriptor._pyre_name, descriptor
        # all done
        return


# end of file
