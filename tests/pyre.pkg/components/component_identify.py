#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the traits of a component tell a visitor the type of what they hold, not how they hold
it: a typed property is identified by its schema, a component by the component schema, a dict as
a dict, or else as the mapping and the container it is, and a behavior as a behavior; each falls
back to schemata in general
"""


def test() -> None:
    """
    Visit the traits of a component
    """
    # support
    import pyre

    # a protocol for the component trait
    class Engine(pyre.protocol, family="pyre.tests.identify.engines"):
        """
        What a car is powered by
        """

    # a component with one trait of each kind
    class Car(pyre.component, family="pyre.tests.identify.car"):
        """
        A component with a typed property, a component, a dict, and a behavior
        """

        # a typed property
        color = pyre.properties.str()
        # a numeric one
        wheels = pyre.properties.int()
        # a component
        engine = Engine()
        # a dict
        options = pyre.properties.kv()

        # a behavior
        @pyre.export
        def drive(self) -> None:
            """
            Drive
            """
            # nowhere
            return

    # an authority that knows only schemata in general
    class Schemata:
        """
        A visitor that sees every trait as a schema
        """

        # the handler of schemata in general
        def _pyre_onSchema(self, schema, **kwds):
            """
            Report a schema
            """
            # by the name of its handler
            return "schema"

    # and one that knows the kinds of traits
    class Kinds(Schemata):
        """
        A visitor that tells the kinds of traits apart
        """

        # the handler of strings
        def _pyre_onString(self, schema, **kwds):
            """
            Report a string
            """
            # by the name of its handler
            return "string"

        # the handler of numbers
        def _pyre_onNumber(self, schema, **kwds):
            """
            Report a number
            """
            # by the name of its handler
            return "number"

        # the handler of components
        def _pyre_onComponent(self, schema, **kwds):
            """
            Report a component
            """
            # by the name of its handler
            return "component"

        # the handler of dicts
        def _pyre_onDict(self, schema, **kwds):
            """
            Report a dict
            """
            # by the name of its handler
            return "dict"

        # the handler of behaviors
        def _pyre_onBehavior(self, schema, **kwds):
            """
            Report a behavior
            """
            # by the name of its handler
            return "behavior"

    # the traits, by name
    traits = {trait.name: trait for trait in Car.pyre_traits()}
    # what each one is
    expected = {
        "color": "string",
        "wheels": "number",
        "engine": "component",
        "options": "dict",
        "drive": "behavior",
    }
    # go through them
    for name, kind in expected.items():
        # each one is identified by what it holds
        assert traits[name]._pyre_identify(authority=Kinds()) == kind, name
        # and every one of them is a schema
        assert traits[name]._pyre_identify(authority=Schemata()) == "schema", name

    # an authority that knows containers
    class Containers(Schemata):
        """
        A visitor that tells containers apart from the other schemata
        """

        # the handler of containers
        def _pyre_onContainer(self, schema, **kwds):
            """
            Report a container
            """
            # by the name of its handler
            return "container"

    # and one that also knows mappings
    class Mappings(Containers):
        """
        A visitor that tells mappings apart from the other containers
        """

        # the handler of mappings
        def _pyre_onMapping(self, schema, **kwds):
            """
            Report a mapping
            """
            # by the name of its handler
            return "mapping"

    # a dict is the mapping it is to an authority that doesn't know dicts
    assert traits["options"]._pyre_identify(authority=Mappings()) == "mapping"
    # and the container it is to one that knows only containers
    assert traits["options"]._pyre_identify(authority=Containers()) == "container"

    # the handler receives the trait itself
    class Receiver:
        """
        A visitor that hands back what it was given
        """

        # the handler of schemata in general
        def _pyre_onSchema(self, schema, **kwds):
            """
            Hand back the schema
            """
            # as it came
            return schema

    # so an authority can read its metadata
    assert traits["color"]._pyre_identify(authority=Receiver()) is traits["color"]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
