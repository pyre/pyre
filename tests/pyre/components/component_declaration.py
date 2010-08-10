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

    class sentry(Component, family="opal.authentication"):
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
      
     
    # check the basics
    assert sentry._pyre_name == "sentry"
    assert sentry._pyre_family == ["opal", "authentication"]
    assert sentry._pyre_configurables == (sentry, Component)
    assert sentry._pyre_implements == None

    # check the trait contents
    sentry_username = sentry.pyre_getTraitDescriptor("username")
    sentry_password = sentry.pyre_getTraitDescriptor("password")
    sentry_authenticate = sentry.pyre_getTraitDescriptor("authenticate")
    traits = [sentry_username, sentry_password, sentry_authenticate]
    assert traits == [trait for trait,source in sentry.pyre_traits()]
    # check the aliases
    assert sentry.pyre_normalizeName("username") == "username"
    assert sentry.pyre_normalizeName("όνομα") == "username"
    assert sentry.pyre_normalizeName("password") == "password"
    assert sentry.pyre_normalizeName("σύνθημα") == "password"

    # get access to the embedded inventory class
    inventory = sentry._pyre_Inventory
    assert inventory._pyre_categories["behaviors"] == (sentry_authenticate,)
    assert inventory._pyre_categories["properties"] == (sentry_username, sentry_password)

    return sentry


# main
if __name__ == "__main__":
    test()


# end of file 
