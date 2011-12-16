# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


def host(builder):
    """
    Decorate the {builder} with host specific options
    """
    # get the host name
    name = builder.host.name
    # print('host:', name)

    # for all other hosts
    return builder


# end of file 
