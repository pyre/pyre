#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check that path hashes work as advertised
"""


def test():
    # access the class
    from pyre.patterns.PathHash import PathHash
    # build one
    pathhash = PathHash()
    # here are a couple of multi-level addresses
    moduleName = "pyre.patterns.PathHash"
    klassName = moduleName + ".PathHash"

    # now hash the matching nodes
    module = pathhash.hash(name=moduleName, separator='.')
    klass = pathhash.hash(name=klassName, separator='.')
    # check that i get the same node the second time i retrieve it 
    assert module == pathhash.hash(name=moduleName, separator='.')
    assert klass == pathhash.hash(name=klassName, separator='.')
    # check that i can retrieve the class from within the module
    assert klass == module.hash(name="PathHash", separator=".")

    # build an alias for the module
    pathhash.alias(alias="pyre.pathhash", original="pyre.patterns.PathHash", separator='.')
    # check that the alias points where it should
    assert module == pathhash.hash(name="pyre.pathhash", separator='.')
    # and that both contain the same class
    assert klass == pathhash.hash(name="pyre.pathhash.PathHash", separator='.')
    # return the pathhash
    return pathhash


# main
if __name__ == "__main__":
    test()


# end of file 
