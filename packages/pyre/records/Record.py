# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import itertools
from .Templater import Templater


class Record(tuple, metaclass=Templater):
    """
    The base class for representing data extracted from persistent stores

    Records have field descriptors that provide the information necessary to convert data
    between the representation used by the persistent store and the native python object
    requred by the application

    Records are similar to named tuples: the underlying storage mechanism is a tuple, and the
    fields are descriptors that provide named access to the tuple entries. Thee are superior to
    named tuples since they enable the data model designer to specify types and constraints
    that must be satisfied by the data, and automate the conversion process to a large degree.

    Inheritance among {Record} subclasses is interpreted as composition: the set of fields that
    define a recors is built out of the descriptors declared both locally and by all of its
    ancestors. Descriptor composition is subject to name shadowing, a restriction that may be
    lifted in a future implementation.
    """


    # types
    from .ConstAccessor import ConstAccessor as pyre_accessor


    # public data
    pyre_localFields = () # the field descriptors found in my class declaratino
    pyre_inheritedFields = () # the field descriptors I inherited


    # interface
    @classmethod
    def pyre_fields(cls):
        return itertools.chain(cls.pyre_localFields, cls.pyre_inheritedFields)


    @classmethod
    def pyre_index(cls, descriptor):
        return tuple(cls.pyre_fields()).index(descriptor)


    @classmethod
    def pyre_raw(cls, data):
        """
        Bypass casting, conversions and validations for those special clients that know the
        data is good. Use with caution.
        """
        return super().__new__(cls, data)


    # meta methods
    def __new__(cls, raw=None, **kwds):
        """
        Initialize a record either from the tuple {raw}, or by extracting the data from {kwds}
        """
        # if were not goven an explict tuple
        if raw is None:
            # extract the values from the {kwds}
            raw = tuple(kwds.pop(field.name, field.default) for field in cls.pyre_fields())
            # if any {kwds} remained, we got some unknown fields
            if kwds:
                raise ValueError("unexpected field names: {}".format(", ".join(kwds.keys())))

        # cast, convert and validate
        data = []
        # iterate over my entire field set
        for value, field in zip(raw, cls.pyre_fields()):
            # cast the value
            value = field.type.pyre_cast(value)
            # convert it
            for converter in field.converters:
                value = converter(value)
            # validate it
            for validator in field.validators:
                value = validator(value)
            # and store it
            data.append(value)

        # form the tuple and build the instance
        return super().__new__(cls, tuple(data))


    # exceptions
    from ..constraints.exceptions import ConstraintViolationError


# end of file 
