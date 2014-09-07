#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# get the framework
import pyre


# declare a class
class application(pyre.application, family='defaults.application'):

    # the default value as a list of strings that should be expanded by the framework
    explicit = pyre.properties.strings(default=['{people.alec}'])
    # the default value as a string that evaluates to a list
    implicit = pyre.properties.strings(default='[{people.alec}]')


# the test
def test():
    # show me
    # print(application.explicit)
    # print(application.implicit)
    # check that the class defaults get evaluated correctly
    assert application.explicit == application.implicit

    # instantiate
    app = application(name='my-defaults')
    # show me
    # print(app.explicit)
    # print(app.implicit)
    # check again
    assert app.explicit == app.implicit

    # all done
    return app


# main
if __name__ == '__main__':
    test()


# end of file 
