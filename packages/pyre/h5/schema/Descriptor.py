# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import typing

# the base node
class Descriptor:
    """
    The base structural element
    """

    # public data
    @property
    def doc(self):
        """
        Provide access to my docstring
        """
        return self.__doc__

    @doc.setter
    def doc(self, explanation: str):
        """
        Set my docstring
        """
        # attach
        self.__doc__ = explanation
        # and done
        return

    # metamethods
    def __init__(self, name=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # set my name
        self._pyre_name = name
        # all done
        return

    # name binding
    def __set_name__(self, cls: type, name: str):
        """
        Set the {name} by which instances of {cls} know me
        """
        # bind me
        self._pyre_bind(name=name)
        # all done
        return

    # descriptor implementation
    def __get__(self, instance, cls: type) -> typing.Any:
        """
        Read my value
        """
        # when accessing through a class record
        if instance is None:
            # grant access to the descriptor
            return self
        # otherwise, ask {instance} for my value
        return instance._pyre_get(name=self._pyre_name)

    def __set__(self, instance, value) -> None:
        """
        Write my value
        """
        # ask {instance} to process and record the new {value}
        instance._pyre_set(name=self._pyre_name, value=value)
        # all done
        return

    def __delete__(self, instance) -> None:
        """
        Delete my value
        """
        # ask {instance} to forget my value
        instance._pyre_delete(name=self._pyre_name)
        # all done
        return

    # framework hooks
    def _pyre_bind(self, name):
        """
        Set my name
        """
        # if i don't already have a name
        if self._pyre_name is None:
            # save my new name
            self._pyre_name = name
        # all done
        return

    def _pyre_clone(self, **kwds):
        """
        Make a copy
        """
        # call my constructor and return the new instance
        return type(self)(name=self._pyre_name, **kwds)

    # implementation details
    _pyre_name = None
    _pyre_descriptors = {}
    _pyre_localDescriptors = {}


# end of file
