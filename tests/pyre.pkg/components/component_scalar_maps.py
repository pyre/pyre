#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A scalar property refuses a non-empty map with an error that names the trait (R4); maps, the
identity, and the empty map given to a str are still accepted (R2)
"""


def test() -> None:
    """
    Give every kind of property a map, and check which ones refuse it
    """
    # support
    import journal
    import pyre
    from pyre.components.exceptions import TraitValueError
    from pyre.schemata.exceptions import CastingError

    # a component with a property of every scalar kind, and a few that take maps
    class Probe(pyre.component, family="pyre.tests.components.maps.probe"):
        """
        The component under study
        """

        # the scalars
        s = pyre.properties.str()
        i = pyre.properties.int()
        x = pyre.properties.float()
        b = pyre.properties.bool()
        d = pyre.properties.decimal()
        c = pyre.properties.complex()
        p = pyre.properties.path()
        u = pyre.properties.uri()
        t = pyre.properties.date()
        a = pyre.properties.inet()
        # the sequences, which are scalars too, as far as maps go
        names = pyre.properties.list()
        tags = pyre.properties.set()
        pair = pyre.properties.tuple()
        # the traits that take maps
        kv = pyre.properties.kv()
        ints = pyre.properties.dict(schema=pyre.properties.int())
        anything = pyre.properties.identity()

    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.maps")
    # the map
    value = {"k": "v"}
    # build the component
    probe = Probe(name="probe")

    # go through the scalars
    for trait in ["s", "i", "x", "b", "d", "c", "p", "u", "t", "a", "names", "tags", "pair"]:
        # give one the map
        setattr(probe, trait, value)
        # carefully
        try:
            # read it
            held = getattr(probe, trait)
        # it must be refused
        except TraitValueError as error:
            # get the complaint
            complaint = str(error)
            # if it does not name the trait, or was not refused as a cast
            if f"probe.{trait}:" not in complaint or not isinstance(error.error, CastingError):
                # say what went wrong
                channel.line(f"'{trait}' refused the map, but its error is wrong")
                # and the details
                channel.indent()
                channel.line(f"error: {complaint}")
                channel.line(f"refused by: {type(error.error).__name__}")
                channel.line(f"look in: the coerce of the schema of {trait!r}")
                channel.outdent()
        # if it is accepted
        else:
            # say so
            channel.line(f"'{trait}' accepted the map as {held!r}")

    # the traits that must accept it, and what they must hold
    accepted = [
        ("kv", value, {"k": "v"}),
        ("ints", {"k": 1}, {"k": 1}),
        ("anything", value, {"k": "v"}),
        ("s", {}, "{}"),
    ]
    # go through them
    for trait, given, expected in accepted:
        # give one its value
        setattr(probe, trait, given)
        # carefully
        try:
            # read it
            held = getattr(probe, trait)
        # if it is refused
        except pyre.PyreError as error:
            # say so
            channel.line(f"'{trait}' refused {given!r}: {error}")
            # and move on
            continue
        # maps are compared by their entries
        held = dict(held) if isinstance(expected, dict) else held
        # if it holds something else
        if held != expected:
            # say so
            channel.line(f"'{trait}' holds {held!r}, not {expected!r}")

    # if anything went wrong
    if channel.page:
        # complain
        channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
