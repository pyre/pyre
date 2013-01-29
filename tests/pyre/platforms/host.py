#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Exercise host configuration
"""


def test():
    # externals
    import pyre

    # derive an application class
    class app(pyre.component):
        """sample application"""

        # my host
        host = pyre.platforms.platform()


    # instantiate
    one = app(name='one')
    # check i have a host
    assert one.host

    # print out some details
    # host = one.host
    # print('host: {}'.format(host))
    # print('  hostname: {.hostname}'.format(host))
    # print('  nickname: {.nickname}'.format(host))
    # print('  cpus: {.cpus}'.format(host))
    # print('  platform: {.platform}'.format(host))
    # print('  release: {.release}'.format(host))
    # print('  codename: {.codename}'.format(host))
    # print('  distribution: {.distribution}'.format(host))

    # and return
    return one


# main
if __name__ == "__main__":
    test()


# end of file 
