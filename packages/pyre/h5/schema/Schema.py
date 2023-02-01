# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import itertools
import journal

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
        localDescriptors = dict(cls._pyre_identifyDescriptors(attributes=attributes))
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

    def __setattr__(self, name: str, value: typing.Any):
        """
        Assign {name} to {value} in the class record of one of my instances
        """
        # if the name is in the protected namespace
        if name.startswith("_"):
            # handle a normal assignment
            return super().__setattr__(name, value)
        # get my descriptors
        descriptors = self._pyre_descriptors
        # check whether
        try:
            # {name} is a known {descriptor}
            descriptor = descriptors[name]
        # if not
        except KeyError:
            # if {value} is a descriptor
            if isinstance(value, Descriptor):
                # add it to my pile
                descriptors[name] = value
                # and bind it
                value.__set_name__(cls=self, name=name)
            # in any case, chain up to handle a normal assignment
            return super().__setattr__(name, value)
        # the following cases are possible:
        # if {descriptor} is a {dataset} and {value} is not a descriptor
        if isinstance(descriptor, Dataset) and not isinstance(value, Descriptor):
            # interpret as setting a new default value
            descriptor.default = value
            # all done
            return
        # {value} is not a descriptor
        if not isinstance(value, Descriptor):
            # this is almost certainly a bug; make a channel
            channel = journal.firewall("pyre.h5.schema")
            # build a report
            channel.line(f"unsupported assignment '{self.__name__}.{name}' <- {value}")
            channel.line(f"in {self}")
            # flush
            channel.log()
            # and bail, just in case firewalls aren't fatal
            return
        # otherwise, replace my {descriptor} with {value}
        descriptors[name] = value
        # bind it
        value.__set_name__(cls=self, name=name)
        # and chain up to handle a normal assignment
        return super().__setattr__(name, value)

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
