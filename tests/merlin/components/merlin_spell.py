#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


"""
Verify that the spell book can locate spells
"""


def test():
    # access to the merlin executive
    from merlin import merlin
    # get the spellbook
    spellbook = merlin.spellbook

    # ask it to find a spell
    spell = spellbook.findSpell(name="sample")

    # and return
    return spell


# main
if __name__ == "__main__":
    test()


# end of file 
