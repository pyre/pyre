# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import pyre

# superclass
from .Descriptor import Descriptor


# the base class for all leaves
@pyre.schemata.typed
class Dataset(Descriptor):
    """
    The base class of all typed datasets
    """

    # types
    disktype = None
    memtype = None

    # my mixins
    from ..typed import array, bool, complex, float, int, str, timestamp, containers

    # metamethods
    # representation
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"dataset '{self._pyre_name}' of type '{self.type}'"

    # framework hooks
    # cloning
    # value syncing hooks by dataset subclasses
    def _pyre_pull(self, dataset):
        """
        Pull my on-disk value into my cache
        """
        # get my type
        cls = type(self)
        # my children must know how to do this
        raise NotImplementedError(
            f"class '{cls.__module__}.{cls.__name__}' must implement '_pyre_pull'"
        )

    def _pyre_push(self, dataset):
        """
        Push my cache value to disk
        """
        # get my type
        cls = type(self)
        # my children must know how to do this
        raise NotImplementedError(
            f"class '{cls.__module__}.{cls.__name__}' must implement '_pyre_push'"
        )

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dataset
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDataset
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)

    # decoration
    def _pyre_marker(self):
        """
        Generate an identifying mark for structural renderings
        """
        # easy
        return self.type

    # type resolution base on cell type and shape
    @classmethod
    def _pyre_deduce(cls, name, cell, info, shape):
        """
        Build a descriptor base on the given {type} and {shape}
        """
        # unpack
        cellname = cell.name
        # attempt to
        try:
            # figure out the cell type
            atom = getattr(cls, cellname)
        # if this fails
        except AttributeError:
            # we understand certain compound types, so give it a shot
            atom = cls._pyre_deduce_compound(name=name, cell=cell, info=info)
        # if the shape is empty
        if len(shape) == 0:
            # instantiate the atom and return it
            return atom(name=name)
        # if the shape is rank one
        if len(shape) == 1 and cellname == "str":
            # we have a special type for that
            from . import strings

            # make a list of strings
            return strings(name=name)
        # if the cell is a numeric type
        if atom.typename in ["complex", "float", "int", "identity"]:
            # make an array
            return cls.array(name=name, schema=atom(name="sentinel"))
        # anything else is generic
        return cls._pyre_deduce_generic(name=name, cell=cell, info=info, shape=shape)

    @classmethod
    def _pyre_deduce_compound(cls, name, cell, info):
        """
        Check whether this is a compound type we understand
        """
        # if the datatype is a compound with two members
        if cell == type(cell).compound and info.count == 2:
            # and both are floats
            if info.type(1).className == info.type(1).className == "FloatType":
                # call it complex and move on
                return cls.complex
        # anything else is generic
        return cls._pyre_deduce_generic(name=name, cell=cell, info=info, **kwds)

    @classmethod
    def _pyre_deduce_generic(cls, name, cell, shape, **kwds):
        """
        Build an undifferentiated dataset type when type deduction fails
        """
        # let me know, for now
        channel = journal.warning("pyre.h5.schema")
        # make a report
        channel.line(
            f"could not deduce the schema for a '{cell.name}' of shape '{shape}'"
        )
        channel.line(f"while attempting to resolve '{name}'")
        # complain
        channel.log()
        # and build an undifferentiated type
        return cls.identity


# end of file
