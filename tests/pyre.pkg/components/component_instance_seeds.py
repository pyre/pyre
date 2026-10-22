#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Building an instance does not process the defaults of its class: the default file of an output
stream is not opened, and so not emptied, unless the instance reads the trait (pyre#366), and
escaped braces in a default reach the instance as they reach the class (pyre#40), and the entries
set for a dict of the class still reach the instance; named and anonymous instances alike
"""


def test() -> None:
    """
    Build named and anonymous instances of a component whose defaults have side effects when they
    are processed, and check what they leave behind
    """
    # externals
    import os
    import tempfile

    # support
    import pyre

    # work in a folder of our own
    folder = tempfile.mkdtemp()
    # the default file of the stream
    default = os.path.join(folder, "default.txt")
    # and the file the instances are told to use instead
    other = os.path.join(folder, "other.txt")

    # the family of the component
    family = "pyre.tests.components.instance.seeds"
    # an entry set for a dict of the class, which its instances must see
    pyre.executive.nameserver[f"{family}.tags.color"] = "red"

    # a component with an output stream, a text with escaped braces, and a dict
    class Writer(pyre.component, family=family):
        """
        A component whose defaults have side effects when they are processed
        """

        # the stream, whose default names a file
        out = pyre.properties.ostream()
        out.default = default
        out.doc = "where to write"

        # text with escaped braces, which is not a macro
        label = pyre.properties.str()
        label.default = "{{not_a_macro}}"
        label.doc = "a label with braces in it"

        # a dict, whose entries for the class are gathered when its slot is processed
        tags = pyre.properties.kv()
        tags.doc = "a dict with an entry set for the class"

    # go through a named instance and an anonymous one
    for name in ("writer", None):
        # put something precious in the default file
        with open(default, "w") as stream:
            # that the instance must not erase
            stream.write("precious\n")
        # build the instance, told to write somewhere else
        writer = Writer(name=name, out=other)
        # the default file is untouched
        with open(default) as stream:
            # so it still holds what it held
            assert stream.read() == "precious\n", name
        # the braces reach the instance as they reach the class
        assert writer.label == Writer.label == "{not_a_macro}", (name, writer.label)
        # and the entry set for the class reaches the dict of the instance
        assert dict(writer.tags) == {"color": "red"}, (name, dict(writer.tags))

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
