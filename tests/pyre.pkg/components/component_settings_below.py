#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Settings filed below a property that takes none, such as a str, an int or a list, are recorded
against the component class or instance when it is configured, and the property keeps its value;
the settings below a dict, a facility or an identity are theirs, and are left alone
"""


def test() -> None:
    """
    File settings below the traits of a class and of an instance, and check what is recorded
    """
    # support
    import journal
    import pyre

    # the errors are logged as they are recorded; keep the log out of the way
    journal.warning("pyre.configuration").device = journal.trash()
    # get the store
    nameserver = pyre.executive.nameserver

    # the family of the component
    family = "pyre.tests.components.below"
    # settings below the traits of the class, made before the class is declared
    nameserver[f"{family}.s.k"] = "class"
    nameserver[f"{family}.d.k"] = "class"

    # a protocol for the facility
    class Part(pyre.protocol, family=f"{family}.parts"):
        """
        The protocol of the facility
        """

    # and a component that implements it
    class Piece(pyre.component, family=f"{family}.parts.piece", implements=Part):
        """
        The component bound to the facility
        """

        # a trait the settings below the facility configure
        x = pyre.properties.int()
        x.default = 1
        x.doc = "an int"

    # a component with a trait of each kind
    class Probe(pyre.component, family=family):
        """
        A component with properties that take no settings below them, and traits that do
        """

        # properties that take no settings below them
        s = pyre.properties.str()
        s.default = "default"
        s.doc = "a str"

        i = pyre.properties.int()
        i.default = 1
        i.doc = "an int"

        l = pyre.properties.list(schema=pyre.properties.str())
        l.default = ["a"]
        l.doc = "a list"

        # traits whose settings below them are theirs
        d = pyre.properties.kv()
        d.doc = "a dict"

        o = pyre.properties.identity()
        o.doc = "an identity"

        part = Part()
        part.default = Piece
        part.doc = "a facility"

    # the class recorded the setting below its str
    names = [error.setting for error in Probe.pyre_classConfigurationErrors()]
    # and only that one
    assert names == [f"{family}.s.k"], names

    # settings below the traits of an instance
    nameserver["probe.s.k"] = "v"
    # including one level further down, with nothing set in between
    nameserver["probe.s.a.b"] = "v"
    nameserver["probe.i.k"] = "v"
    nameserver["probe.l.k"] = "v"
    nameserver["probe.d.k"] = "v"
    nameserver["probe.o.k"] = "v"
    nameserver["probe.part.x"] = "2"
    # and a value for one of them
    nameserver["probe.i"] = "2"

    # build the instance
    probe = Probe(name="probe")
    # the settings below the properties that take none are recorded against it
    recorded = probe.pyre_configurationErrors
    # by name
    names = sorted(error.setting for error in recorded)
    # each of them, once
    assert names == ["probe.i.k", "probe.l.k", "probe.s.a.b", "probe.s.k"], names
    # go through them
    for error in recorded:
        # each one is about the instance
        assert error.configurable is probe, error
        # names its setting, and says where it was made, which is this file
        assert error.setting in str(error) and "component_settings_below.py" in str(error), error

    # the properties keep their values
    assert probe.s == "default"
    assert probe.i == 2
    assert probe.l == ["a"]
    # the dict holds the setting below it as an entry
    assert dict(probe.d) == {"k": "v"}
    # and the facility's component is configured by the setting below it
    assert probe.part.x == 2

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
