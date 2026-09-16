#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that settings read from a yaml file know where they came from: the file, the line, and
the column of their key, on top of the reason the file was read
"""


def test():
    # support
    import pyre

    # gain access to the nameserver
    ns = pyre.executive.nameserver
    # load a configuration file
    pyre.loadConfiguration("sample.yaml")
    # read it, to find the lines the settings sit on
    lines = open("sample.yaml", encoding="utf-8").read().splitlines()
    # go through a few settings and the text that introduces each in the file
    for name, text in (
        ("sample.user.name", "name:"),
        ("sample.user.email", "email:"),
        ("sample.user.affiliation", "affiliation:"),
    ):
        # get the provenance
        locator = ns.getInfo(ns.hash(name)).locator
        # the head of the chain says where in the file the setting sits
        where = locator.this
        # it is the sample file
        assert str(where.source).endswith("sample.yaml"), name
        # on the line that introduces the setting, counting from one
        assert lines[where.line - 1].strip().startswith(text), (name, where.line)
        # at the column of its key, counting from one
        assert lines[where.line - 1][where.column - 1 :].startswith(text), (name, where.column)
        # and the rest of the chain says why the file was read
        assert locator.next is not None, name
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
