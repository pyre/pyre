#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the values of secret traits stay out of the displays of the configuration, and that
a configuration whose components refer to each other is displayed without going around forever
"""


def test():
    import pyre

    class peer(pyre.protocol):
        """a trivial protocol"""

    class node(pyre.component, implements=peer):
        """a component with a secret, and a reference to a peer"""

        # a secret
        password = pyre.properties.str(default="hunter2")
        password.secret = True
        # something that is not
        user = pyre.properties.str(default="guest")
        # and a peer
        partner = peer(default=None)

    # traits are not secret unless they say so
    assert node.pyre_trait(alias="password").secret is True
    assert node.pyre_trait(alias="user").secret is False
    assert node.pyre_trait(alias="partner").secret is False

    # two nodes that refer to each other
    a = node(name="a")
    b = node(name="b")
    a.partner = b
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
    # shows the peer once, and refers back to the node it started from
    assert display.count("\nb:") + display.count("  b:") == 1
    assert "see a" in display

    # the json friendly rendering
    doc = a.pyre_renderConfiguration()
    # keeps the secret out
    assert doc["properties"]["password"]["value"] is None
    assert doc["properties"]["password"]["default"] is None
    # and marks it
    assert doc["properties"]["password"]["secret"] is True
    # but not the rest
    assert doc["properties"]["user"]["value"] == "guest"
    assert doc["properties"]["user"]["secret"] is False

    # a renderer that writes traits as assignments
    class renderer:
        """a stand-in for the renderers of the weaver"""

        # the start of a component
        def componentStart(self, component):
            # as a section
            yield f"{component.pyre_name}:"

        # the end of a component
        def componentEnd(self, component):
            # with a blank line
            yield ""

        # a trait and its value
        def trait(self, name, value):
            # as an assignment
            return f"{name} = {value}"

        # a value on a line of its own
        def value(self, value):
            # as it is
            return f"{value}"

    # the rendered configuration, which is written to files that are read back
    rendered = list(a.pyre_renderTraitValues(renderer=renderer()))
    # leaves the secret out altogether, since a placeholder would read back as its value
    assert not any("password" in line or "hunter2" in line for line in rendered), rendered
    # but not the rest
    assert "user = guest" in rendered, rendered

    # all done
    return a, b


# main
if __name__ == "__main__":
    test()


# end of file
