# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import itertools
import pyre.calc
from .Record import Record


class DynamicRecord(Record):
    """
    The base class for representing data extracted from persistent stores

    {DynamicRecord} uses a tuple of {pyre.calc} nodes for the value storage. This provides
    support for fields whose value can be changed. Derivations are setup with evaluators from
    {pyre.calc}.
    """


    # types
    from .NodalFieldAccessor import NodalFieldAccessor as pyre_fieldAccessor
    from .NodalDerivationAccessor import NodalDerivationAccessor as pyre_derivationAccessor


    @classmethod
    def pyre_process(cls, raw, **kwds):
        """
        Form the tuple that holds my values by extracting information from either {raw} or
        {kwds} and walking it through casting, conversion and validation
        """
        # if were not given an explict tuple
        if raw is None:
            # extract the values from the {kwds}
            raw = tuple(kwds.pop(field.name, field.default) for field in cls.pyre_fields())
            # if any {kwds} remained, we got some unknown fields
            if kwds:
                raise ValueError("unexpected field names: {}".format(", ".join(kwds.keys())))

        # storage for my tuple
        data = []
        # cast, convert and validate my field data
        for value, field in zip(raw, cls.pyre_fields()):
            # get the descriptor to process the value
            value = field.process(value)
            # build a new node
            node = pyre.calc.newNode(value=value)
            # and store it
            data.append(node)

        # evaluate the derivations
        # print("processing derivations")
        for derivation in cls.pyre_derivations():
            # print("  {.name!r}".format(derivation))
            # print("    type: {!r}".format(derivation))
            # print("    expr: {}".format(derivation))
            # compute the value
            value = derivation.eval(values=data, index=cls.pyre_index)
            # print("    value: {!r}".format(value))
            # thanks to nodal algebra, this already a node; store it
            data.append(value)

        # form the tuple and return it
        return tuple(data)


    # meta methods
    def __getitem__(self, index):
        """
        Indexed read access: get the value of the associated node
        """
        return super().__getitem__(index).value


    def __setitem__(self, index, value):
        """
        Indexed write access: set the value of the associated node
        """
        super().__getitem__(index).value = value
        return


# end of file 
