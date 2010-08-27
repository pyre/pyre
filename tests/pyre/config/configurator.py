#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the configurator factory is accessible
"""


def test():
    import pyre
    import pyre.config
    return pyre.config.newConfigurator(executive=pyre.executive)


# main
if __name__ == "__main__":
    test()


# end of file 
