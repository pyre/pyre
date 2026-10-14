#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a schema tells a visitor what type it is: it asks for the handler of its own type, falls
back to the handlers of the types it derives from, most specific first, and ends at the handler of
schemata in general; something with no handler at all is not a visitor, and is told so
"""


def test() -> None:
    """
    Visit the schemata with authorities that know progressively more types
    """
    # support
    import pyre.schemata

    # an authority that knows only schemata in general
    class Schemata:
        """
        A visitor that sees every schema as a schema
        """

        # the handler of schemata in general
        def _pyre_onSchema(self, schema, **kwds):
            """
            Report a schema
            """
            # by the name of its handler
            return "schema"

    # one that also knows numbers
    class Numbers(Schemata):
        """
        A visitor that tells numbers apart from the other schemata
        """

        # the handler of numbers
        def _pyre_onNumber(self, schema, **kwds):
            """
            Report a number
            """
            # by the name of its handler
            return "number"

    # and one that also knows integers and containers
    class Integers(Numbers):
        """
        A visitor that tells integers apart from the other numbers, and knows containers
        """

        # the handler of integers
        def _pyre_onInteger(self, schema, **kwds):
            """
            Report an integer
            """
            # by the name of its handler
            return "integer"

        # the handler of containers
        def _pyre_onContainer(self, schema, **kwds):
            """
            Report a container
            """
            # by the name of its handler
            return "container"

    # every schema reaches the handler of schemata in general
    for schema in (pyre.schemata.str(), pyre.schemata.int(), pyre.schemata.path()):
        # when that is all there is
        assert schema._pyre_identify(authority=Schemata()) == "schema"
    # a number reaches the handler of numbers, the closest one there is
    for schema in (pyre.schemata.int(), pyre.schemata.float(), pyre.schemata.bool()):
        # when there is one
        assert schema._pyre_identify(authority=Numbers()) == "number"
    # while a string is still a schema
    assert pyre.schemata.str()._pyre_identify(authority=Numbers()) == "schema"
    # an integer reaches its own handler, ahead of the one of numbers
    assert pyre.schemata.int()._pyre_identify(authority=Integers()) == "integer"
    # while the other numbers do not
    assert pyre.schemata.float()._pyre_identify(authority=Integers()) == "number"
    # sequences and mappings are containers
    for schema in (pyre.schemata.list(), pyre.schemata.tuple(), pyre.schemata.mapping()):
        # by way of the types between them and containers
        assert schema._pyre_identify(authority=Integers()) == "container"

    # what the handler receives
    class Receiver:
        """
        A visitor that hands back what it was given
        """

        # the handler of schemata in general
        def _pyre_onSchema(self, schema, **kwds):
            """
            Hand back the schema and the extra arguments
            """
            # as they came
            return schema, kwds

    # a schema to visit
    schema = pyre.schemata.str()
    # hands itself to the handler, along with whatever the visit carried
    assert schema._pyre_identify(authority=Receiver(), depth=1) == (schema, {"depth": 1})

    # something that has no handlers at all
    try:
        # is no visitor
        pyre.schemata.str()._pyre_identify(authority=object())
        # so this is unreachable
        assert False, "an object with no handlers was accepted as a visitor"
    # and is told so
    except NotImplementedError as error:
        # by name
        assert "builtins.object" in str(error), str(error)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
