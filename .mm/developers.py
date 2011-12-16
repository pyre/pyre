# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


def developer(builder):
    """
    Decorate the builder with developer specific choices
    """
    # get the developer name
    name = builder.user.name
    # print('developer:', name)

    # for Michael Aïvázis <michael.aivazis@orthologue.com>
    if name == 'aivazis' or name == 'mga':
        # set the default target
        builder.build.user = ['debug', 'shared', 'mpi']
        # all done
        return builder

    # for all others
    return builder


# end of file 
