#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre

class ifac(pyre.interface, family="sample.ifac"):
    """sample interface"""

class comp(pyre.component, family="sample.ifac.comp", implements=ifac):
    """an implementation"""
    tag = pyre.properties.str()

class container(pyre.component, family="sample.container"):
    """a component container"""
    catalog = pyre.catalog(interface=ifac)


def test():
    # build the shell
    s = container(name="catalog_container")
    # verify that the catalog has three members
    assert len(s.catalog) == 3
    # and that the contents were configured properly
    for name, instance in s.catalog.items():
        assert instance.tag == name

    return s
    

# main
if __name__ == "__main__":
    test()


# end of file 
