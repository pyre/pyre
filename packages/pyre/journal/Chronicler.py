# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre
import journal

# my protocol
from .Journal import Journal

# the support channel managers
from .Debug import Debug
from .Firewall import Firewall
from .Error import Error
from .Warning import Warning
from .Informational import Informational


# the journal channel manager
class Chronicler(pyre.component, family="pyre.journal.chronicler", implements=Journal):
    """
    The top level manager of the application journal channels
    """

    # configurable state
    decor = pyre.properties.int()
    decor.default = 1
    decor.doc = "the default state of all application channels"

    detail = pyre.properties.int()
    detail.default = 2
    detail.doc = "the maximum level of detail that is included in the output"

    margin = pyre.properties.str()
    margin.default = "  "
    margin.doc = "the decoration to add to indented output"

    channels = pyre.properties.list(
        schema=pyre.properties.tuple(schema=pyre.properties.str())
    )
    channels.doc = "a list of channels to place under the control of the user"

    # interface obligations
    @pyre.export
    def register(self, app, name):
        """
        Register the application name with the chronicler
        """
        # register the app name with the journal
        journal.application(name=name)
        # go through the {app} journal channels
        for severity, section in app.pyre_journalChannels():
            # get the channel factory
            factory = self.map[severity]
            # build the component name
            channelName = ".".join([name, "journal", severity, section])
            # make the channel
            channel = factory(name=channelName, section=section)
            # transfer its state
            channel.apply()
        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the channel index is a list of components that manage channel state
        self.index = []
        # the table that maps severity name to component factories
        self.map = {
            # for end users
            "error": Error,
            "warning": Warning,
            "info": Informational,
            # for developers
            "debug": Debug,
            "firewall": Firewall,
        }
        # all done
        return

    # framework hooks
    def pyre_configured(self, **kwds):
        """
        Hook invoked when the component configuration is complete
        """
        # chain up
        yield from super().pyre_configured(**kwds)

        # transfer my state to the chronicler
        journal.decor(level=self.decor)
        journal.detail(level=self.detail)
        journal.margin(margin=self.margin)

        # all done
        return


# end of file
