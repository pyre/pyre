# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2014 all rights reserved
#


def developer(builder):
    """
    Decorate the builder with developer specific choices
    """
    # get the developer name
    name = builder.user.name
    # print('developer:', name)

    # return the builder
    return builder


# end of file 
