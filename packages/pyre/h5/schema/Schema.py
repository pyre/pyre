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
            name
            for name, descriptor in cls._pyre_identifyDescriptors(attributes=attributes)
        )
        # and an empty one for all visible class descriptors that we will fill out later on
        classDescriptors = Inventory()
        # add them to the pile of {attributes} of {cls}
        attributes["_pyre_localDescriptors"] = localDescriptors
        attributes["_pyre_classDescriptors"] = classDescriptors
        # build the record
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # resolve the visible descriptors
        classDescriptors.update(record._pyre_resolve())
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
        # make a pile of descriptor names
        descriptors = itertools.chain(
            # by chaining together
            *(
                # all locally declared descriptors
                base._pyre_localDescriptors
                # from every base of {self}
                for base in self.mro()
                # that is a group
                if isinstance(base, Schema)
            )
        )
        # go through them
        yield from (
            # and filter those names
            name
            # from the pile
            for name in descriptors
            # that correspond to descriptors
            if isinstance(getattr(self, name), Descriptor)
        )
        # all done
        return


# end of file
