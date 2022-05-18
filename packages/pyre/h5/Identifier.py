#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# base class of all h5 objects
class Identifier:
    """
    A placeholder for h5 identifiers, a very very low level concept
    """


    # metamethods
    def __init__(self, name=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # my name
        self.pyre_name = name
        # all done
        return


    # descriptor support
    def __set_name__(self, cls, name):
        """
        Attach my name
        """
        # bind my to my name
        self.pyre_bind(name=name)
        # all done
        return


    def __get__(self, instance, cls):
        """
        Read access to my value
        """
        # when accessing through a class record
        if instance is None:
            # return the descriptor
            return self

        # otherwise, look up my value in the {inventory} of the {instance}
        value = instance.pyre_inventory[self]
        # and return it
        return value


    def __set__(self, instance, value):
        """
        Write access to my value
        """
        print(f"{self.pyre_name}.__set__: {instance=}, {value=}")


    def __delete__(self, instance):
        """
        Delete my value
        """
        # remove form the {instance} inventory
        del instance.pyre_inventory[self]
        # and done
        return


    # rep
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return "an identifier"


    # framework hooks
    def pyre_bind(self, name):
        """
        Bind me to my {name}
        """
        # save my name
        self.pyre_name = name
        # all done
        return


# end of file
