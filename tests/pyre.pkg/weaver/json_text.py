#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the JSON renderer writes the values JSON has no type for as the text of their schema,
and that the text reads back as the same value
"""


def test() -> None:
    """
    Render a value of each schema that travels as text, and read it back
    """
    # support
    import datetime
    import decimal
    import enum
    import fractions
    import json
    import uuid
    import pyre

    # an enumeration
    class Color(enum.Enum):
        """
        Some colors
        """

        # the members
        red = 1

    # make a renderer
    renderer = pyre.weaver.json()
    # the schemata
    schemata = pyre.schemata
    # a zone
    zone = datetime.timezone(datetime.timedelta(hours=-7))

    # each schema, and a value
    cases = [
        (schemata.decimal(), decimal.Decimal("1.25")),
        (schemata.fraction(), fractions.Fraction(1, 3)),
        (schemata.complex(), 1 + 2j),
        (schemata.enum(enum=Color), Color.red),
        (schemata.cell(), pyre.memory.cells.int32),
        (schemata.inet(), schemata.inet().coerce("localhost:5000")),
        (schemata.date(), datetime.date(2026, 11, 20)),
        (schemata.time(), datetime.time(3, 4, 5, 250000, tzinfo=zone)),
        (schemata.timestamp(), datetime.datetime(2026, 11, 20, 3, 4, 5, tzinfo=zone)),
        (schemata.path(), pyre.primitives.path("/a/b")),
        (schemata.uuid(), uuid.UUID(int=5)),
        (schemata.bytes(), b"\\x00A"),
        (schemata.dimensional(), schemata.dimensional().coerce("2*meter")),
    ]
    # go through them
    for schema, value in cases:
        # render the value
        rendered = renderer.render(schema=schema, value=value)
        # it is the text of its schema
        assert rendered == schema.string(value), (schema.typename, rendered)
        # it survives a JSON document
        text = json.loads(json.dumps(rendered))
        # and reads back as the same value, which writes the same text again
        assert schema.string(schema.coerce(value=text)) == rendered, (schema.typename, text)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
