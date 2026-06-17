# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from pyre.patterns.AttributeClassifier import AttributeClassifier

# parts
from .Descriptor import Descriptor
from .Dimension import Dimension
from .Inventory import Inventory

# typing
import typing


# the generator of group structure
class Schema(AttributeClassifier):
    """
    The metaclass that harvests descriptors from group declarations
    """

    # metamethods
    def __new__(
        cls,
        name: str,
        bases: typing.Sequence[type],
        attributes: dict,
        *,
        location: typing.Optional[str] = None,
        **kwds,
    ):
        """
        Build the class record of a new h5 group

        The optional {location} declares the absolute mount point of a root group, e.g.
        '/science/LSAR'. It is needed only at the root: the mount point of every other node
        is determined by the attribute name to which its descriptor is bound.
        """
        # build the record
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # resolve the group static structure
        record._pyre_resolve(attributes=attributes)
        # if this group declares an explicit mount point
        if location is not None:
            # record it; subclasses inherit it unless they declare their own
            record._pyre_location = location
        # all done
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

    def _pyre_resolve(self, attributes: dict):
        """
        Scan the {mro} of the class record in {self} and build the group static structure
        """
        # the set of member names from the declaration of this group
        localDescriptors = Inventory()
        # the set of member names from the entire class hierarchy
        classDescriptors = Inventory()
        # the set of dimension names from the declaration of this group
        localDimensions = Inventory()
        # the set of dimension names from the entire class hierarchy
        classDimensions = Inventory()
        # the map from h5 member names to attribute names
        aliases = {}
        # go through the local declarations
        for name, descriptor in self._pyre_identifyDescriptors(attributes=attributes):
            # dimensions are shape providers, not tree members; keep them apart
            if isinstance(descriptor, Dimension):
                # in their own pile
                localDimensions.add(name)
                # and out of the member machinery
                continue
            # add the name to the local pile
            localDescriptors.add(name)
            # and update the aliases
            aliases[descriptor._pyre_name] = name
        # update the static layout
        classDescriptors.update(localDescriptors)
        classDimensions.update(localDimensions)

        # now, go through my ancestors
        for base in self.mro()[1:]:
            # if this {base} class is not a group
            if not isinstance(base, Schema):
                # skip it
                continue
            # go through its locally declared members
            for name in base._pyre_localDescriptors:
                # look up my understanding of this name
                descriptor = getattr(self, name)
                # if some mixin did something different with this name
                if not isinstance(descriptor, Descriptor):
                    # move on
                    continue
                # otherwise, add it to the static layout
                classDescriptors.add(name)
                # get the descriptor name
                alias = descriptor._pyre_name
                # if it's not already among my aliases
                if alias not in aliases:
                    # add it
                    aliases[alias] = name
            # and through its locally declared dimensions
            for name in base._pyre_localDimensions:
                # look up my understanding of this name
                dimension = getattr(self, name)
                # if some mixin did something different with this name
                if not isinstance(dimension, Dimension):
                    # move on
                    continue
                # otherwise, add it to the dimension layout
                classDimensions.add(name)

        # attach the local members
        self._pyre_localDescriptors = localDescriptors
        # attach the class members
        self._pyre_classDescriptors = classDescriptors
        # attach the local dimensions
        self._pyre_localDimensions = localDimensions
        # attach the class dimensions
        self._pyre_classDimensions = classDimensions
        # and the translation map
        self._pyre_staticAliases = aliases
        # all done
        return


# end of file
