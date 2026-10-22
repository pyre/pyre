#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The names of packages and the families of protocols and components belong to the framework: a
value at one of them fires a firewall, whether it is set before the name is registered or after,
and so does an instance built with one of those names
"""


def test() -> None:
    """
    Set values at the names of packages and families, before and after they are registered, and
    check that each one fires the firewall, naming the name
    """
    # support
    import journal
    import pyre

    # the firewall fires on purpose here; keep its report out of the way
    journal.firewall("pyre.configuration").device = journal.trash()
    # get the store
    nameserver = pyre.executive.nameserver

    def fires(what, step, expected):
        """
        Run {step} and check that it fires the firewall with {expected} in its report
        """
        # attempt to
        try:
            # take the step
            step()
        # if the firewall fires
        except journal.FirewallError as error:
            # its report must say what is wrong
            assert expected in "\n".join(error.page), (what, error.page)
        # otherwise
        else:
            # complain
            assert False, f"{what}: the firewall did not fire"
        # all done
        return

    # a protocol and a component, which register the package {fwn} and their families
    class Part(pyre.protocol, family="fwn.parts"):
        """
        A protocol
        """

    class Piece(pyre.component, family="fwn.parts.piece", implements=Part):
        """
        A component
        """

    # a value at the name of a package, after the package exists
    fires(
        what="a package, after",
        step=lambda: nameserver.__setitem__("fwn", "5"),
        expected="'fwn' names a package",
    )
    # which keeps its node
    assert isinstance(nameserver["fwn"], nameserver.Package)
    # a value at the family of a protocol, after the protocol is declared
    fires(
        what="a protocol, after",
        step=lambda: nameserver.__setitem__("fwn.parts", "5"),
        expected="'fwn.parts' names a family",
    )
    # which keeps its node
    assert nameserver["fwn.parts"] is Part
    # a value at the family of a component, after the component is declared
    fires(
        what="a component, after",
        step=lambda: nameserver.__setitem__("fwn.parts.piece", "5"),
        expected="'fwn.parts.piece' names a family",
    )
    # which keeps its node
    assert nameserver["fwn.parts.piece"] is Piece

    # a value at the name of a package, before the package exists
    nameserver["fwnb"] = "5"

    # then a component in that package
    def declarePackaged():
        """
        Declare a component in the package {fwnb}
        """

        # the component
        class Early(pyre.component, family="fwnb.early"):
            """
            A component in a package whose name holds a value
            """

    # fires the firewall
    fires(what="a package, before", step=declarePackaged, expected="'fwnb' names a package")

    # a value at the family of a component, before the component is declared
    nameserver["fwn.late"] = "5"

    # then the component
    def declareFamily():
        """
        Declare a component in the family {fwn.late}
        """

        # the component
        class Late(pyre.component, family="fwn.late"):
            """
            A component whose family holds a value
            """

    # fires the firewall
    fires(what="a component, before", step=declareFamily, expected="'fwn.late' names a family")

    # an instance named after a family
    fires(
        what="an instance",
        step=lambda: Piece(name="fwn.parts"),
        expected="'fwn.parts' names a family",
    )

    # declaring a component again in the same family is not a collision
    class Again(pyre.component, family="fwn.parts.piece", implements=Part):
        """
        A component declared again in a family that is taken
        """

    # the newer declaration holds the family
    assert nameserver["fwn.parts.piece"] is Again

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
