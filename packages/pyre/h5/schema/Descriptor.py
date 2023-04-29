# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import journal
import typing


# the base node
class Descriptor:
    """
    The base structural element
    """

    # metamethods
    def __init__(self, name: typing.Optional[str] = None, **kwds):
        # chain up
        super().__init__(**kwds)
        # set my name; this does not have to be the name by which I am known to my container,
        # since valid h5 group member names may not be valid python identifiers
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

    # framework hooks
    # name binding
    def _pyre_bind(self, name: str):
        """
        Set my name
        """
        # if i don't already have a name
        if self._pyre_name is None:
            # save my new name
            self._pyre_name = name
        # all done
        return

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
            ) from None
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
    def _pyre_view(self, channel=None, flush=True):
        """
        Generate a representation of my structure
        """
        # get the viewer factory
        from .Viewer import Viewer as viewer

        # if we don't have a channel
        if channel is None:
            # make one
            channel = journal.info("pyre.h5.object")
        # build the report
        channel.report(report=viewer().visit(self))
        # if we were asked to flush the channel
        if flush:
            # do it
            channel.log()
        # all done
        return

    # implementation details
    _pyre_name: typing.Optional[str] = None


# end of file
