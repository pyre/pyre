#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre

class ifac(pyre.interface, family="deferred.ifac"):
    """sample interface"""

class comp(pyre.component, family="deferred.ifac.comp", implements=ifac):
    """an implementation"""
    tag = pyre.properties.str()

class user(pyre.component, family="deferred.user"):
    """a component user"""
    comp = pyre.facility(interface=ifac)

class container(pyre.component, family="deferred.container"):
    """a component container"""
    name = pyre.properties.str(default=None)
    comp = pyre.facility(interface=ifac)
    catalog = pyre.catalog(interface=ifac)


def test():
    # build the individual user
    u = user(name="user")
    # verify that its {comp} is configured correctly
    assert u.comp.tag == "user"
    # build the shell
    s = container(name="tagger")
    # verify that the catalog has three members
    assert len(s.catalog) == 3
    # and that the contents were configured properly
    for name, instance in s.catalog.items():
        # print("tag: {!r}, name: {!r}".format(instance.tag, name))
        assert instance.tag == name

    return s
    

# main
if __name__ == "__main__":
    test()


# end of file 
