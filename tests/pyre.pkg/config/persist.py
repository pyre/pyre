#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a component persists its state in one call: the file it writes, loaded as plain
configuration, rebuilds the component and the part it owns; persisting again updates the
file in place, and several components share a file
"""

# support
import pyre


# a protocol
class Tool(pyre.protocol, family="persist.tools"):
    """
    Tools
    """

    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default tool
        """
        # a hammer
        return Hammer


# a part, meant to be owned
class Hammer(pyre.component, family="persist.tools.hammer", implements=Tool):
    """
    A hammer
    """

    weight = pyre.properties.float(default=1.0)
    worn = pyre.properties.bool(default=False)


# the owner
class Bench(pyre.component, family="persist.benches.bench"):
    """
    A work bench
    """

    label = pyre.properties.str(default="bench")
    jobs = pyre.properties.int(default=0)
    marks = pyre.properties.list(schema=pyre.properties.tuple(schema=pyre.properties.float()))
    marks.default = []
    home = pyre.properties.path(default="/tmp")
    tool = Tool()
    scratch = pyre.properties.list(schema=pyre.properties.str())
    scratch.default = []
    scratch.persistent = False


def test():
    # support
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # the file with the state; it does not exist yet
    uri = pyre.primitives.path("persist-state.yaml")
    # make sure
    if uri.exists():
        # by removing leftovers from an earlier run
        uri.unlink()

    # build a bench
    bench = Bench(name="persist.bench")
    # put it to work
    bench.jobs = 3
    bench.marks = [(1.0, 2.0), (3.0, 4.0)]
    bench.home = "/var/tmp"
    bench.scratch = ["a", "b"]
    # wear its tool
    bench.tool.worn = True
    # persist it
    bench.pyre_persist(uri=uri)

    # the file says what was configured and nothing else
    doc = pyre.config.newYamlEditor(uri=uri)
    assert list(doc.get("persist.bench")) == ["jobs", "marks", "home", "tool"]
    assert doc.get("persist.bench", "tool") == "persist.tools.hammer"
    assert dict(doc.get("persist.bench.tool")) == {"worn": True}

    # a second bench, configured by what the first one wrote: copy the sections under its name
    doc.set("persist.copy", value=doc.get("persist.bench"))
    doc.set("persist.copy.tool", value=doc.get("persist.bench.tool"))
    doc.save()
    # restoring is plain configuration
    pyre.loadConfiguration(str(uri))
    # build the copy
    copy = Bench(name="persist.copy")
    # and check that it came up in the state of the original
    assert copy.label == "bench"
    assert copy.jobs == 3
    assert list(copy.marks) == [(1.0, 2.0), (3.0, 4.0)]
    assert str(copy.home) == "/var/tmp"
    assert list(copy.scratch) == []
    assert isinstance(copy.tool, Hammer)
    assert copy.tool.worn is True
    assert copy.tool.weight == 1.0

    # more work
    copy.jobs += 1
    # persisted together with the original, in one call
    pyre.saveConfiguration(uri=uri, components=[bench, copy])
    # updates the file in place
    doc = pyre.config.newYamlEditor(uri=uri)
    assert doc.get("persist.copy", "jobs") == 4
    assert doc.get("persist.bench", "jobs") == 3
    # without growing new sections
    assert list(doc.document) == [
        "persist.bench",
        "persist.bench.tool",
        "persist.copy",
        "persist.copy.tool",
    ]

    # clean up
    uri.unlink()
    # all done
    return bench


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
