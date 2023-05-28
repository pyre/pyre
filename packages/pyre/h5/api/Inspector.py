# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
from . import exceptions

# h5 object factories
from .Group import Group
from .Dataset import Dataset
from .Datatype import Datatype

# typing
import pyre
import typing
from .. import libh5
from .. import disktypes
from .. import memtypes
from .. import schema
from .Object import Object

# type aliases
H5Group = libh5.Group
H5DataSet = libh5.DataSet
H5DataType = libh5.datatypes.DataType
H5ObjectType = libh5.ObjectType


# libh5 bridge mixin
class Inspector:
    """
    A mixin that provides higher level access to {libh5} entities

    It can build h5 object hierarchies by inferring structure and type information
    using only on-disk information, or it can walk the hierarchy with a specification
    and extract a subset of the information
    """

    # convenient access
    def _pyre_inspect(
        self,
        h5id: typing.Union[H5DataSet, H5Group],
        path: pyre.primitives.path,
        query: typing.Optional[schema.descriptor] = None,
        depth: typing.Optional[int] = None,
    ) -> Object:
        """
        Build the hierarchy rooted at {path} that is contained within the given {h5id}

        The optional {query} can be used to constrain the traversal to its structure,
        while a non-trivial {depth} value will limit how far to look
        """
        # if this is a constrained traversal
        if query is not None:
            # visit only the specified file locations
            return self._pyre_queryObject(
                h5id=h5id, path=path, query=query, depth=depth
            )
        # otherwise, grab everything
        return self._pyre_inferObject(h5id=h5id, path=path, depth=depth)

    # support for querying the hierarchy by following a spec
    # object factories
    def _pyre_queryObject(
        self,
        h5id: typing.Union[H5DataSet, H5Group],
        path: pyre.primitives.path,
        query: schema.descriptor,
        depth: typing.Optional[int] = None,
    ) -> Object:
        """
        Build the hierarchy rooted at {path} that is contained within the given {h5id},
        using {query} as a constraint on the traversal
        """
        # get the type of the object at {h5id}
        h5type = h5id.objectType
        # build the tag
        tag = h5type.name.capitalize()
        # look up the object factory
        factory = getattr(self, f"_pyre_query{tag}")
        # invoke it
        h5object = factory(h5id=h5id, path=path, query=query, depth=depth)
        # and return what was built
        return h5object

    def _pyre_queryGroup(
        self,
        h5id: H5Group,
        path: pyre.primitives.path,
        query: schema.group,
        depth: typing.Optional[int] = None,
    ) -> Group:
        """
        Build a group at {path}
        """
        # build an empty spec
        spec = schema.group(name=path.name)
        # and attach it to an empty group
        group = Group(id=h5id, at=path, layout=spec)
        # check the depth limit
        if depth is not None:
            # if we have reached the bottom
            if depth <= 0:
                # go no further
                return group
            # otherwise, adjust it
            depth -= 1
        # go through the members in {query}
        for memberName, attributeName in query._pyre_aliases.items():
            # carefully
            try:
                # look up the member
                memberId = h5id.get(memberName)
            # if it's not there
            except RuntimeError:
                # ignore and move on
                continue
            # if it's there, build its location
            memberPath = path / memberName
            # extract its descriptor
            memberSpec = getattr(query, attributeName)
            # build it
            member = self._pyre_queryObject(
                h5id=memberId, path=memberPath, query=memberSpec, depth=depth
            )
            # add it to the group contents
            setattr(group, attributeName, member)
            # and its layout to the group spec
            setattr(spec, attributeName, member._pyre_layout)
        # all done
        return group

    def _pyre_queryDataset(
        self, h5id: H5DataSet, path: pyre.primitives.path, query: schema.dataset, **kwds
    ) -> Dataset:
        """
        Build the dataset at {path}
        """
        # {query} has the structure we expect to find here; load the actual one from disk
        actual = self._pyre_inferDatasetDescriptor(name=path.name, h5id=h5id)
        # consolidate the two pictures into a layout for the bew dataset
        spec = self._pyre_consolidateSchema(path=path, expected=query, actual=actual)
        # make a dataset
        dataset = Dataset(id=h5id, at=path, layout=spec)
        # and return it
        return dataset

    def _pyre_consolidateSchema(
        self,
        path: pyre.primitives.path,
        expected: schema.dataset,
        actual: schema.dataset,
    ):
        """
        Compare the {expected} and {actual} specifications of a dataset and build a specification
        that is guaranteed to work
        """
        # check the disk types for compatibility
        if expected.disktype.cell != actual.disktype.cell:
            # f they don't match, we have a problem
            problem = exceptions.TypeMismatchError(
                path=path, expected=expected, actual=actual
            )
            # make a channel
            channel = journal.warning("pyre.h5.api.inspector")
            # report
            channel.report(report=problem._pyre_report())
            # and flush
            channel.log()
            # prefer the actual, so pulling information from the file can succeed;
            # it will cause failures elsewhere, most likely, so this may better be an error
            return actual
        # in every other case, prefer the {expected} descriptor
        return expected

    # support for inferring hierarchies using nothing but on-disk information
    # object factories
    def _pyre_inferObject(
        self,
        h5id: typing.Union[H5DataSet, H5Group],
        path: pyre.primitives.path,
        depth: typing.Optional[int] = None,
    ) -> Object:
        """
        Build the hierarchy rooted at {path} that is contained within the given {h5id}

        The parameter {depth} places an upper bound on the search; if it is {None}, the
        full hierarchy is retrieved
        """
        # get the type of the object at {h5id}
        h5type = h5id.objectType
        # build the tag
        tag = h5type.name.capitalize()
        # lookup the object factory
        factory = getattr(self, f"_pyre_infer{tag}")
        # invoke it
        h5object = factory(h5id=h5id, path=path, depth=depth)
        # and return what was built
        return h5object

    def _pyre_inferGroup(
        self,
        h5id: H5Group,
        path: pyre.primitives.path,
        depth: typing.Optional[int] = None,
    ) -> Group:
        """
        Build a group at {path}
        """
        # build an empty spec
        spec = schema.group(name=path.name)
        # and attach it to an empty group
        group = Group(id=h5id, at=path, layout=spec)
        # check the depth limit
        if depth is not None:
            # if we have reached the bottom
            if depth <= 0:
                # go no further
                return group
            # otherwise, adjust it
            depth -= 1
        # infer my structure
        for memberName in h5id.members():
            # look up the member
            memberId = h5id.get(path=memberName)
            # build it
            member = self._pyre_inferObject(
                h5id=memberId, path=path / memberName, depth=depth
            )
            # add it to the group contents
            setattr(group, memberName, member)
            # and its layout to the group spec
            setattr(spec, memberName, member._pyre_layout)
        # all done
        return group

    def _pyre_inferDataset(
        self, h5id: H5DataSet, path: pyre.primitives.path, **kwds
    ) -> Dataset:
        """
        Build a dataset at {path}
        """
        # figure out my structure
        spec = self._pyre_inferDatasetDescriptor(name=path.name, h5id=h5id)
        # make an empty dataset
        dataset = Dataset(id=h5id, at=path, layout=spec)
        # and return it
        return dataset

    def _pyre_inferDatatype(
        self, h5id: H5DataType, path: pyre.primitives.path, **kwds
    ) -> Datatype:
        """
        Build a named data type at {path}
        """
        # make a named datatype
        datatype = Datatype(id=h5id, at=path)
        # and return it
        return datatype

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
        for memberName in h5id.members():
            # look up
            memberId = h5id.get(path=memberName)
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

    def _pyre_inferCompoundDescriptor(
        self, name: str, h5type: H5DataType
    ) -> schema.dataset:
        """
        Build a descriptor for a compound object

        Currently, only complex numbers are supported
        """
        # check for a complex number
        if h5type.members == 2 and (
            h5type.type(0).cell == h5type.type(1).cell == libh5.DataSetType.float
        ):
            # get the total bits
            bits = sum(h5type.type(n).precision for n in range(2))
            # get the in-memory type; don't let it drop below 64
            memtype = getattr(memtypes, f"complex{max(bits, 64)}")
            # build the descriptor
            complex = schema.complex(name=name, memtype=memtype, disktype=h5type)
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

    def _pyre_inferFloatDescriptor(
        self, name: str, h5type: H5DataType
    ) -> schema.dataset:
        """
        Build a {float} descriptor
        """
        # build the tag
        bits = h5type.precision
        # get the in-memory type; don't let it drop below 32 bits
        memtype = getattr(memtypes, f"float{max(bits, 32)}")
        # build the descriptor
        float = schema.float(name=name, memtype=memtype, disktype=h5type)
        # and return it
        return float

    def _pyre_inferIntDescriptor(self, name: str, h5type: H5DataType) -> schema.dataset:
        """
        Build an {int} descriptor
        """
        # build the tags
        sign = "u" if h5type.sign == libh5.Sign.unsigned else ""
        bits = h5type.precision
        # assemble the factory name
        factory = f"{sign}int{bits}"
        # get the in-memory type
        memtype = getattr(memtypes, factory)
        # build the descriptor
        int = schema.int(name=name, memtype=memtype, disktype=h5type)
        # and return it
        return int

    def _pyre_inferStrDescriptor(self, name: str, h5type: H5DataType) -> schema.dataset:
        """
        Build a {str} descriptor
        """
        # MGA: NYI: how does {h5type} affect the inference?
        # get the in-memory type
        memtype = memtypes.char
        # build the descriptor
        str = schema.str(name=name, memtype=memtype, disktype=h5type)
        # and return it
        return str


# end of file
