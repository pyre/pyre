# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import journal.interfaces


# the component declaration
class ANSIRenderer(pyre.component, family="merlin.renderers.ansi", 
                   implements=journal.interfaces.renderer):
    """
    Custom replacement for the {journal} renderer
    """


    # interface
    @pyre.export
    def render(self, page, metadata):
        """
        Convert the diagnostic information into a form that a device can record
        """
        # my colors; hardwired for now
        marker = self.pallete[metadata['severity']]
        blue = self.colors['blue']
        normal = self.colors['normal']
        # extract the information from the metadata
        channel = '{}{}{}'.format(blue, metadata['channel'], normal)
        severity = '{}{}{}'.format(marker, metadata['severity'].upper(), normal)

        # make an iterator over the message contents
        lines = iter(page)
        # build the first line of the message
        yield "{}: {}: {}".format(channel, severity, next(lines))
        # and render the rest
        for line in lines: yield line
            
        # all done
        return


    # private data
    esc = "[{}m"
    colors = {
        "": "", # no color given
        "none": "", # no color
        "normal": esc.format("0"), # reset back to whatever is the default for the terminal

        # regular colors
        "black": esc.format("0;30"),
        "red": esc.format("0;31"),
        "green": esc.format("0;32"),
        "brown": esc.format("0;33"),
        "blue": esc.format("0;34"),
        "purple": esc.format("0;35"),
        "cyan": esc.format("0;36"),
        "light-gray": esc.format("0;37"),

        # bright colors
        "dark-gray": esc.format("1;30"),
        "light-red": esc.format("1;31"),
        "light-green": esc.format("1;32"),
        "yellow": esc.format("1;33"),
        "light-blue": esc.format("1;34"),
        "light-purple": esc.format("1;35"),
        "light-cyan": esc.format("1;36"),
        "white": esc.format("1;37"),
        }

    pallete = {
        'info': colors['green'],
        'warning': colors['purple'],
        'error': colors['red'],
        }


# end of file 
