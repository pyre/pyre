#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Check that path hashes work as advertised
    """
    # access the class
    import pyre.primitives
    # build one
    pathhash = pyre.primitives.pathhash()
    # here is a couple of multi-level addresses
    separator = '.'
    moduleName = "pyre.primitives.PathHash".split(separator)
    clsName = moduleName + ["PathHash"]

    # now hash the matching nodes
    module = pathhash.hash(moduleName)
    cls = pathhash.hash(items=clsName)

    # check that i get the same node the second time i retrieve it
    assert module is pathhash.hash(items=moduleName)
    assert cls is pathhash.hash(items=clsName)
    # check that i can retrieve the class from within the module
    assert cls is module.hash(items=["PathHash"])

    # set up an alias for the module
    base = pathhash.hash(items=['pyre'])
    alias = "pathhash"
    original = pathhash.hash(items="pyre.primitives.PathHash".split(separator))
    # alias the two nodes
    base.alias(alias=alias, target=original)

    # check that the alias points where it should
    assert module is pathhash.hash(items="pyre.pathhash".split(separator))
    # and that both contain the same class
    assert cls is pathhash.hash(items="pyre.pathhash.PathHash".split(separator))

    # dump out the contents of the hash
    # pathhash.dump()

    # return the pathhash
    return pathhash


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
