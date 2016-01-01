# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import pyre
# access to my protocol
import journal.protocols
# my facilities
from .Terminal import Terminal


# declaration
class Renderer(pyre.component, family='pyre.shells.renderer',
               implements=journal.protocols.renderer):
    """
    Custom replacement for the {journal} renderer
    """


    # public state
    terminal = Terminal()


    # interface
    @pyre.export
    def render(self, page, metadata):
        """
        Convert the diagnostic information into a form that a device can record
        """
        # if the page is empty, there's nothing to do
        if not page: return

        # my colors; hardwired for now
        marker = self.palette[metadata['severity']]
        blue = self.terminal.colors['blue']
        normal = self.terminal.colors['normal']
        # extract the information from the metadata
        channel = '{}{}{}'.format(blue, metadata['channel'], normal)
        severity = '{}{}{}'.format(marker, metadata['severity'].upper(), normal)

        # decorate the first line
        yield "{}: {}: {}".format(channel, severity, page[0])
        # and render the rest
        yield from page[1:]

        # all done
        return


    def __init__(self, **kwds):
        super().__init__(**kwds)

        # get my terminal
        terminal = self.terminal
        # build my palette
        self.palette = {
            'info': terminal.colors['green'],
            'warning': terminal.colors['purple'],
            'error': terminal.colors['red'],
            'debug': terminal.colors['brown'],
            'firewall': terminal.colors['light-red'],
            }

        # all done
        return


# end of file
