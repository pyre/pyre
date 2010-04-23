#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
A more elaborate component declaration
"""


def test():
    import pyre.components
    from pyre.components.Component import Component
    from pyre.components.Property import Property

    class Sentry(Component, family="opal.authentication"):
        """a user authentication component"""

        # properties
        username = Property()
        username.default = "mga"
        username.aliases.add("όνομα")

        password = Property()
        password.default = None
        password.aliases.add("σύνθημα")
       
        # behaviors
        @pyre.components.export
        def authenticate(self):
            """grant access based on the supplied credentials"""
            return True
      
     
    # instantiate
    sentry = Sentry(name="naïve")

    # check the class variables
    assert sentry._pyre_name == "naïve"
    assert sentry._pyre_family == "opal.authentication"
    assert sentry._pyre_configurables == (Sentry, Component)
    assert sentry._pyre_implements == None

    # verify that the instance was recorded in the extent
    assert set(Sentry.pyre_getExtent()) == {sentry}

    # check the properties
    assert sentry.username == 'mga'
    assert sentry.password == None
    # set them to something else
    sentry.username = 'aivazis'
    sentry.password = 'deadbeef'
    # check again
    assert sentry.username == 'aivazis'
    assert sentry.password == 'deadbeef'
    # and make sure we didn't mess up the defaults
    another = Sentry(name="another")
    print("another: username={}, password={}".format(another.username, another.password))
    assert another.username == 'mga'
    assert another.password == None

    return sentry


# main
if __name__ == "__main__":
    test()


# end of file 
