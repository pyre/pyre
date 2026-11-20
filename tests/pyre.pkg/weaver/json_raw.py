#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the JSON renderer reduces values that no schema interprets to plain values
"""


def test() -> None:
    """
    Render a structure held by a trait that takes values as they are
    """
    # support
    import json
    import pyre

    # make a renderer
    renderer = pyre.weaver.json()
    # a schema that takes values as they are
    schema = pyre.schemata.identity()

    # a structure with tuples, a set, and a value JSON knows nothing about
    value = {"pairs": ((1, 2),), "tags": {"a"}, 3: 1 + 2j}
    # render it
    rendered = renderer.render(schema=schema, value=value)
    # sequences become lists, keys become strings, and the rest becomes its text
    assert rendered == {"pairs": [[1, 2]], "tags": ["a"], "3": "(1+2j)"}, rendered
    # so the whole of it fits in a JSON document
    json.dumps(rendered)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
