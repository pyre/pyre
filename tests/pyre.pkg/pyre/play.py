#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access the framework
import pyre


class role(pyre.protocol, family="play.roles"):
    """A role"""

    @classmethod
    def pyre_default(cls):
        return actor


class actor(pyre.component, implements=role):
    """An actor"""


# protect this class declaration because the configuration file has an intentional error
def musical(**kwds):
    # build the embedded class record
    class musical(pyre.component, family="play.musicals"):
        """A play"""

        cast = pyre.properties.dict(schema=role())

    # return it
    return musical(**kwds)


# driver
def test():

    # attempt to
    try:
        # make a play
        musical(name="spamalot")
    # if this fails because the role could not be resolved
    except role.TraitValueError as error:
        # all good
        assert isinstance(error.error, role.ResolutionError), error
    # otherwise
    else:
        # oops
        assert False

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
