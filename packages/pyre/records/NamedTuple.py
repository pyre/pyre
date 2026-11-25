# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class NamedTuple(tuple):
    """
    Storage for and access to the values of record instances
    """

    # public data; patched by my metaclass
    pyre_layout = None  # the record that generates me
    pyre_extract = None  # the strategy for extracting values and storing them

    # exceptions
    from .exceptions import RowLengthError, UnknownFieldError, ComputedFieldError

    # meta-methods
    def __new__(cls, record, data=None, **kwds):
        """
        Initialize a new record instance by extracting values from either {data} or {kwds}
        """
        # when given a row
        if data is not None:
            # realize it
            row = tuple(data)
            # the strategy that extracts my values knows how many it takes
            arity = cls.pyre_extract.arity(record=record)
            # so a row of any other length
            if len(row) != arity:
                # is an error
                raise cls.RowLengthError(record=record, expected=arity, given=len(row))
            # otherwise, pull the values from it
            source = iter(row)
        # when given keywords
        else:
            # the names of the fields of the record
            names = {field.name for field in record.pyre_fields}
            # keywords that name none of them
            unknown = [name for name in kwds if name not in names]
            # are an error
            if unknown:
                # so complain
                raise cls.UnknownFieldError(record=record, names=unknown)
            # the names of the fields the record computes
            derived = {field.name for field in record.pyre_derivations}
            # keywords that name one of them
            computed = [name for name in kwds if name in derived]
            # are an error too
            if computed:
                # so complain
                raise cls.ComputedFieldError(record=record, names=computed)
            # otherwise, pull the value of each measure from them, or its default
            source = (kwds.get(measure.name, measure.default) for measure in record.pyre_measures)
        # extract the values
        values = cls.pyre_extract(record=record, source=source)
        # and build the tuple
        return super().__new__(cls, values)

    # private data
    __slots__ = ()


# end of file
