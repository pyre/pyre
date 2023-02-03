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
    # name binding
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

    # cloning
    def _pyre_clone(self, **kwds):
        """
        Make a copy
        """
        # call my constructor and return the new instance
        return type(self)(name=self._pyre_name, **kwds)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a descriptor
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDescriptor
        # if it doesn't understand
        except AttributeError:
            # get my class
            cls = type(self)
            # and my poorly formed visitor
            visitor = type(authority)
            # it's not a visitor, since we only get here when all alternatives are exhausted
            raise NotImplementedError(
                f"class '{visitor.__module__}.{visitor.__name__}' "
                f"is not a '{cls.__module__}.{cls.__name__}' visitor"
            )
        # otherwise, invoke the handler
        return handler(object=self, **kwds)

    # decoration
    def _pyre_marker(self):
        """
        Generate an identifying mark for structural renderings
        """
        # easy
        return "d"

    # rendering
    def _pyre_render(self, channel=None, flush=True):
        """
        Generate a representation of my structure
        """
        # get the explorer factory
        from .Explorer import Explorer as explorer

        # if we don't have a channel
        if channel is None:
            # get the journal
            import journal

            # and make one
            channel = journal.info("pyre.h5.object")

        # build the report
        channel.report(report=explorer().explore(self))
        # if we were asked to flush the channel
        if flush:
            # do it
            channel.log()

        # all done
        return

    # implementation details
    _pyre_name = None
    _pyre_descriptors = {}
    _pyre_localDescriptors = {}


# end of file
