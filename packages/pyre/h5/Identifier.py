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
        # otherwise, get my value from {instance}
        value = instance.pyre_get(descriptor=self)
        # process it
        value = self.pyre_process(instance=instance, value=value)
        # and make it available
        return value


    def __set__(self, instance, value):
        """
        Write access to my value
        """
        # process {value}
        value = self.pyre_process(instance=instance, value=value)
        # and attach it to {instance}
        instance.pyre_set(descriptor=self, value=value)
        # all done
        return


    def __delete__(self, instance):
        """
        Delete my value
        """
        # remove my value from {instance}
        instance.pyre_delete(descriptor=self)
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


    def pyre_get(self, descriptor):
        """
        Read my value
        """
        # i don't know how to do that
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'pyre_get'")


    def pyre_set(self, descriptor, value):
        """
        Write my value
        """
        # i don't know how to do that
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'pyre_set'")


    def pyre_delete(self, descriptor):
        """
        Delete my value
        """
        # i don't know how to do that
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'pyre_delete'")


    def pyre_sync(self, **kwds):
        """
        Hook invoked when the {inventory} lookup fails and a value must be generated
        """
        # i know nothing, so...
        return None


    def pyre_process(self, value, **kwds):
        """
        Walk {value} through my transformations
        """
        # i know nothing, so...
        return value


    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an identifier
        """
        # invoke the hook
        return authority.pyre_onIdentifier(identifier=self, **kwds)


    def pyre_clone(self, name=None, **kwds):
        """
        Make as faithful a clone of mine as possible
        """
        # if the caller did not express any opinions
        if name is None:
            # use my name as the default
            name = self.pyre_name
        # invoke my constructor
        return type(self)(name=name, **kwds)


# end of file
