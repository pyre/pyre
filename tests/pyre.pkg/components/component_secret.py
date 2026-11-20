#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Check that the values of secret traits stay out of the displays of the configuration, and
    that a configuration whose components refer to each other is displayed without going around
    forever
    """
    # support
    import pyre

    # a protocol
    class peer(pyre.protocol):
        """
        A trivial protocol
        """

    # and a component that implements it
    class node(pyre.component, implements=peer):
        """
        A component with a secret, and a reference to a peer
        """

        # a secret
        password = pyre.properties.str()
        password.default = "hunter2"
        password.secret = True

        # something that is not
        user = pyre.properties.str()
        user.default = "guest"

        # and a peer
        partner = peer()
        partner.default = None

    # traits are not secret unless they say so: the one that does
    assert node.pyre_trait(alias="password").secret is True
    # the one that does not
    assert node.pyre_trait(alias="user").secret is False
    # and the facility
    assert node.pyre_trait(alias="partner").secret is False

    # make a node
    a = node(name="a")
    # and another
    b = node(name="b")
    # that refer to each other: the first to the second
    a.partner = b
    # and the second to the first
    b.partner = a
    # the secret is still there for whoever uses it
    assert a.password == "hunter2"

    # the display of the configuration
    display = "\n".join(a.pyre_showConfiguration(deep=True))
    # keeps the secret out
    assert "hunter2" not in display
    # says that there is one
    assert "value: (secret)" in display
    # shows the rest
    assert "value: guest" in display
    # shows the peer once
    assert display.count("\nb:") + display.count("  b:") == 1
    # and refers back to the node it started from
    assert "see a" in display

    # the json friendly rendering
    doc = a.pyre_renderConfiguration()
    # keeps the secret out of the value
    assert doc["properties"]["password"]["value"] is None
    # and the default
    assert doc["properties"]["password"]["default"] is None
    # and marks it
    assert doc["properties"]["password"]["secret"] is True
    # but not the rest, whose value is there
    assert doc["properties"]["user"]["value"] == "guest"
    # and which is not marked
    assert doc["properties"]["user"]["secret"] is False

    # a mill of configuration files
    mill = pyre.weaver.pfg()(name="mill")

    # the rendered configuration, which is written to files that are read back
    rendered = list(a.pyre_renderTraitValues(renderer=mill))
    # leaves the secret out altogether, since a placeholder would read back as its value
    assert not any("password" in line or "hunter2" in line for line in rendered), rendered
    # but not the rest
    assert "    user = guest" in rendered, rendered

    # all done
    return a, b


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
