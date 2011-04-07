#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the merlin shell is accessible
"""


def test():
    # access to the merlin executive
    from merlin import merlin
    # get the spellbook
    spellbook = merlin.spellbook

    # ask it to find a spell
    spell = spellbook.findSpell(name="test")

    # and return
    return spell


# main
if __name__ == "__main__":
    test()


# end of file 
