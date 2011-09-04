#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that path hashes work as advertised
"""


def test():
    # access the class
    import pyre.patterns
    # build one
    pathhash = pyre.patterns.newPathHash()
    # here are a couple of multi-level addresses
    separator = '.'
    moduleName = "pyre.patterns.PathHash".split(separator)
    klassName = moduleName + ["PathHash"]

    # now hash the matching nodes
    module = pathhash.hash(key=moduleName)
    klass = pathhash.hash(key=klassName)
    # check that i get the same node the second time i retrieve it 
    assert module == pathhash.hash(key=moduleName)
    assert klass == pathhash.hash(key=klassName)
    # check that i can retrieve the class from within the module
    assert klass == module.hash(key=["PathHash"])

    # build an alias for the module
    alias = "pyre.pathhash".split(separator)
    original = "pyre.patterns.PathHash".split(separator)
    pathhash.alias(alias=alias, canonical=original)
    # check that the alias points where it should
    assert module == pathhash.hash(key=alias)
    # and that both contain the same class
    assert klass == pathhash.hash(key=alias+["PathHash"])

    # dump out the contents of the hash
    # pathhash.dump()

    # return the pathhash
    return pathhash


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
