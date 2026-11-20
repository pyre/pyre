#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the YAML renderer leaves numbers alone and writes everything else as text whose braces
survive the interpolation of a configuration file
"""


def test() -> None:
    """
    Render text with braces, a path with braces, and numbers
    """
    # support
    import pyre

    # make a renderer
    renderer = pyre.weaver.yaml()
    # the schemata
    schemata = pyre.schemata

    # numbers stay numbers
    assert renderer.render(schema=schemata.float(), value=2.5) == 2.5
    # and so do truth values
    assert renderer.render(schema=schemata.bool(), value=False) is False
    # text has its braces doubled
    assert renderer.render(schema=schemata.str(), value="x{y}") == "x{{y}}"
    # and so does the text of any other schema
    path = renderer.render(schema=schemata.path(), value=pyre.primitives.path("/a/{b}"))
    # such as a path
    assert path == "/a/{{b}}", path

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
