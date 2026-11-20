# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Schema import Schema


# declaration
class Channel(Schema):
    """
    A representation of channels that cross an {exec}

    A channel is rendered as the import path of its class, its hints and the numbers of its
    descriptors, e.g. {pyre.ipc.SocketPair:SocketPair?family=1&type=1&proto=0#7}; a process
    that inherits the descriptors under the same numbers turns the string back into the channel
    """

    # constants
    # my name
    typename = "channel"
    # and what i say when a value cannot be made into a channel
    complaint = "could not use {0.value!r} as a channel"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a channel
        """
        # get the channels
        from ..ipc.Channel import Channel

        # channels
        if isinstance(value, Channel):
            # are left alone
            return value
        # text
        if isinstance(value, str):
            # is parsed
            hints, descriptors = self.parse(text=value)
            # and turned into the channel it describes
            return Channel.arrive(hints=hints, descriptors=descriptors)
        # all other types are incompatible
        raise self.CastingError(value=value, description=self.complaint)

    def string(self, value):
        """
        Render value as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # ask the channel how it leaves
        hints, descriptors = value.depart()
        # the hints other than its kind
        settings = "&".join(f"{key}={setting}" for key, setting in hints.items() if key != "kind")
        # and its descriptors
        numbers = ",".join(str(descriptor) for descriptor in descriptors)
        # put it all together
        return f"{hints['kind']}?{settings}#{numbers}"

    # implementation details
    def parse(self, text):
        """
        Extract the hints and the descriptor numbers from the rendering of a channel in {text}
        """
        # split off the descriptors
        head, _, numbers = text.partition("#")
        # separate the kind from the rest of the hints
        kind, _, settings = head.partition("?")
        # the hints start with the kind
        hints = {"kind": kind}
        # followed by the rest
        hints.update(setting.split("=", 1) for setting in settings.split("&") if setting)
        # get the descriptors
        descriptors = [int(number) for number in numbers.split(",") if number]
        # and hand them off
        return hints, descriptors

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a channel
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onChannel
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
