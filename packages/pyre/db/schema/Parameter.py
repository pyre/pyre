# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Parameter:
    """
    A slot for a value that is given when a prepared statement runs

    A slot stands wherever a value may stand: in a restriction, in the template of an update, or
    as a bound of a selection. In the template of an update, the column it fills gives it a type;
    everywhere else, its {schema} says what it holds, except for the bounds of a selection, which
    are always integers
    """

    # meta-methods
    def __init__(self, name: str, schema=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the name the value is given under
        self.name = name
        # and the type of the value, when no column says what it is
        self.schema = schema
        # all done
        return

    def __repr__(self) -> str:
        # my name says which value i stand for
        return f"pyre.db.parameter(name={self.name!r})"


# end of file
