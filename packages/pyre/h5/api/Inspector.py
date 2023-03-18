# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
from . import exceptions

# typing
import pyre
import typing
from .. import disktypes
from .. import memtypes
from .. import schema

# type aliases
H5Group = pyre.libh5.Group
H5DataSet = pyre.libh5.DataSet
H5DataType = pyre.libh5.datatypes.DataType
H5ObjectType = pyre.libh5.ObjectType


# libh5 bridge mixin
class Inspector:
    """
    A mixin that provides higher level access to {libh5} entities
    """

    # group accessors
    # descriptor factories
    def _pyre_inferDescriptor(
        self,
        name: str,
        h5id: typing.Union[H5Group, H5DataSet],
        depth: typing.Optional[int] = None,
    ) -> schema.descriptor:
        """
        Build a specification for {h5id} given its {h5type}
        """
        # extract the object type
        h5type = h5id.objectType
        # get the object type name
        tag = h5type.name.capitalize()
        # look up the recognizer
        recognizer = getattr(self, f"_pyre_infer{tag}Descriptor")
        # invoke it and return the generated descriptor
        return recognizer(name=name, h5id=h5id, depth=depth)

    # group structure
    def _pyre_inferGroupDescriptor(
        self, name: str, h5id: H5Group, depth: typing.Optional[int] = None
    ) -> schema.group:
        """
        Build a group
        """
        # make a descriptor
        descriptor = schema.group(name=name)
        # check the depth limit
        if depth is not None:
            # if we have reached the bottom
            if depth <= 0:
                # go no further
                return descriptor
            # otherwise, adjust it
            depth -= 1
        # go through the group contents
        for memberName, *_ in h5id.members():
            # look up
            memberId, *_ = h5id.get(path=memberName)
            # identify it
            member = self._pyre_inferDescriptor(
                name=memberName, h5id=memberId, depth=depth
            )
            # and add it to the descriptor
            setattr(descriptor, memberName, member)
        # return the group descriptor
        return descriptor

    # dataset structure
    def _pyre_inferDatasetDescriptor(
        self, name: str, h5id: H5DataSet, **kwds
    ) -> schema.dataset:
        """
        Build a typed dataset descriptor by inspecting {h5id}
        """
        # get the type
        cell = h5id.cell.name.capitalize()
        # attempt to
        try:
            # look up the type recognizer
            recognizer = getattr(self, f"_pyre_infer{cell}Descriptor")
        # if one couldn't be located
        except AttributeError:
            # we have bumped into an unsupported type; set up the problem
            problem = exceptions.UnsupportedTypeError(dataset=name, h5type=h5id.cell)
            # call it a bug
            channel = journal.firewall("pyre.h5.api.inspector")
            # report
            channel.report(report=problem._pyre_report())
            # flush
            channel.log()
            # and raise the exception, in case firewalls aren't fatal
            raise problem
        # deduce the schema
        descriptor = recognizer(name=name, h5type=h5id.type)
        # get the dataset space
        space = h5id.space
        # ask it for the rank
        rank = space.rank
        # if this is a scalar
        if rank == 0:
            # we are done
            return descriptor
        # lists of strings
        if rank == 1 and isinstance(descriptor, schema.str):
            # are a special type
            return schema.strings(name=name)
        # everything else is an array; get the shape
        shape = space.shape
        # build a descriptor
        array = schema.array(name=name, schema=descriptor, rank=rank, shape=shape)
        # and return it
        return array

    def _pyre_inferStrDescriptor(self, name: str, h5type: H5DataType) -> schema.dataset:
        """
        Build a {str} descriptor
        """
        # MGA: NYI: how does {h5type} affect the inference?
        # get the on-disk type
        disktype = disktypes.char
        # get the in-memory type
        memtype = memtypes.char
        # build the descriptor
        str = schema.str(name=name, memtype=memtype, disktype=disktype)
        # and return it
        return str

    def _pyre_inferIntDescriptor(self, name: str, h5type: H5DataType) -> schema.dataset:
        """
        Build an {int} descriptor
        """
        # build the tags
        sign = "u" if h5type.sign == pyre.libh5.Sign.unsigned else ""
        bits = h5type.precision
        # assemble the factory name
        factory = f"{sign}int{bits}"
        # get the on-disk type
        disktype = getattr(disktypes, factory)
        # get the in-memory type
        memtype = getattr(memtypes, factory)
        # build the descriptor
        int = schema.int(name=name, memtype=memtype, disktype=disktype)
        # and return it
        return int

    def _pyre_inferFloatDescriptor(
        self, name: str, h5type: H5DataType
    ) -> schema.dataset:
        """
        Build a {float} descriptor
        """
        # build the tag
        bits = h5type.precision
        # get the on-disk type
        disktype = getattr(disktypes, f"float{bits}")
        # get the in-memory type; don't let it drop below 32 bits
        memtype = getattr(memtypes, f"float{max(bits, 32)}")
        # build the descriptor
        float = schema.float(name=name, memtype=memtype, disktype=disktype)
        # and return it
        return float

    def _pyre_inferCompoundDescriptor(
        self, name: str, h5type: H5DataType
    ) -> schema.dataset:
        """
        Build a descriptor for a compound object

        Currently, only complex numbers are supported
        """
        # check for a complex number
        if h5type.members == 2 and (
            h5type.type(0).cell == h5type.type(1).cell == pyre.libh5.DataSetType.float
        ):
            # get the total bits
            bits = sum(h5type.type(n).precision for n in range(2))
            # get the on-disk type
            disktype = getattr(disktypes, f"complex{bits}")
            # get the in-memory type; don't let it drop below 64
            memtype = getattr(memtypes, f"complex{max(bits, 64)}")
            # build the descriptor
            complex = schema.complex(name=name, memtype=memtype, disktype=disktype)
            # and return it
            return complex
        # nothing else is supported, for now; build a problem description
        problem = exceptions.UnsupportedCompoundTypeError(dataset=name, h5type=h5type)
        # make a channel
        channel = journal.firewall("pyre.h5.api.inspector")
        # generate a report
        channel.report(report=problem._pyre_report())
        # flush
        channel.log()
        # and raise the exception, just in case firewalls aren't fatal
        raise problem


# end of file
