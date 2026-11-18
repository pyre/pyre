#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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

    # its weight
    weight = pyre.properties.float()
    weight.default = 1.0

    # whether it is worn
    worn = pyre.properties.bool()
    worn.default = False


# the owner
class Bench(pyre.component, family="persist.benches.bench"):
    """
    A work bench
    """

    # its label
    label = pyre.properties.str()
    label.default = "bench"

    # the number of jobs done on it
    jobs = pyre.properties.int()
    jobs.default = 0

    # the marks on its surface
    marks = pyre.properties.list(schema=pyre.properties.tuple(schema=pyre.properties.float()))
    marks.default = []

    # where it lives
    home = pyre.properties.path()
    home.default = "/tmp"

    # the tool it owns
    tool = Tool()

    # notes that are not worth keeping
    scratch = pyre.properties.list(schema=pyre.properties.str())
    scratch.default = []
    scratch.persistent = False


def test():
    """
    Check that a component persists its state in one call: the file it writes, loaded as plain
    configuration, rebuilds the component and the part it owns; persisting again updates the file in
    place, and several components share a file
    """
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

    # open the file
    doc = pyre.config.newYamlEditor(uri=uri)
    # which says what was configured and nothing else
    assert list(doc.get("persist.bench")) == ["jobs", "marks", "home", "tool"]
    # binds the tool by its family
    assert doc.get("persist.bench", "tool") == "persist.tools.hammer"
    # and records the state of the tool in a section of its own
    assert dict(doc.get("persist.bench.tool")) == {"worn": True}

    # a second bench, configured by what the first one wrote: copy the section of the bench
    # under its name
    doc.set("persist.copy", value=doc.get("persist.bench"))
    # and the section of its tool
    doc.set("persist.copy.tool", value=doc.get("persist.bench.tool"))
    # save the file
    doc.save()
    # restoring is plain configuration
    pyre.loadConfiguration(str(uri))
    # build the copy
    copy = Bench(name="persist.copy")
    # and check that it came up in the state of the original: the label it never changed
    assert copy.label == "bench"
    # the jobs
    assert copy.jobs == 3
    # the marks
    assert list(copy.marks) == [(1.0, 2.0), (3.0, 4.0)]
    # the home
    assert str(copy.home) == "/var/tmp"
    # but not the notes, which were never written down
    assert list(copy.scratch) == []
    # its tool is a hammer
    assert isinstance(copy.tool, Hammer)
    # that is worn
    assert copy.tool.worn is True
    # and still weighs the same
    assert copy.tool.weight == 1.0

    # more work
    copy.jobs += 1
    # persisted together with the original, in one call
    pyre.saveConfiguration(uri=uri, components=[bench, copy])
    # updates the file in place
    doc = pyre.config.newYamlEditor(uri=uri)
    # with the new count of the copy
    assert doc.get("persist.copy", "jobs") == 4
    # next to the old count of the original
    assert doc.get("persist.bench", "jobs") == 3
    # without growing new sections
    assert list(doc.document) == [
        "persist.bench",
        "persist.bench.tool",
        "persist.copy",
        "persist.copy.tool",
    ]

    # all done
    return bench


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
