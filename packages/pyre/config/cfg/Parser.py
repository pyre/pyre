# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import re
import pyre.tracking


# class declaration
class Parser:
    """
    A simple parser for {cfg} files

    This parser understands a variant of the windows {INI} file format. See the package
    documentation for details.
    """


    # constants
    # the supported forms
    comment = r"\s*;.*$"
    blankline = "\s*$"
    section = r"\s*\[\s*(?P<section>(?P<family>[^\]\s#]+)(\s*#\s*(?P<name>[^\]\s]+))?)\s*\]" 
    assignment = r"\s*(?P<assignment>(?P<key>[^=\s\[\]]+)\s*(=\s*(?P<value>[^;]*))?)"

    # combine the patterns and compile them
    scanner = re.compile('|'.join([
                blankline,
                comment,
                section,
                assignment,
                ]))

    # types
    from .exceptions import ParsingError
    from ..events import Assignment, ConditionalAssignment


    # interface
    def parse(self, uri, stream, locator):
        """
        Harvest the configuration events in {stream}
        """
        # initialize the component name
        name = ''
        # initialize the component family
        family = []
        # initialize the event list
        configuration = []
        # examine {stream}
        for lineno, line in enumerate(stream):
            # attempt to match the contents
            match = self.scanner.match(line)
            # if it didn't match
            if match is None:
                # build a locator
                uriloc = pyre.tracking.file(source=uri, line=lineno)
                # if i were handed a locator
                if locator:
                    # adjust it
                    locator = pyre.tracking.chain(this=uriloc, next=locator)
                # otherwise
                else:
                    # just use the new one
                    locator = uriloc

                # build the message
                msg = "syntax error"
                # we have a problem
                raise self.ParsingError(description=msg, locator=locator)
            # we have a match
            groups = match.groupdict()

            # is it an assignment?
            if groups['assignment']:
                # extract the key and value
                key = groups['key'].strip()
                value = groups['value'].strip()

                # if we have an explicit component name
                if name:
                    # build a conditional assignment event
                    event = self.ConditionalAssignment(
                        component=name,
                        condition=(name, family),
                        key=key, value=value, 
                        locator=pyre.tracking.file(source=uri, line=lineno))
                # otherwise
                else:
                    # build a simple assignment event
                    event = self.Assignment(
                        key=tuple(family + [key]),
                        value=value, 
                        locator=pyre.tracking.file(source=uri, line=lineno))
                # add it to the pile
                configuration.append(event)
                # grab the next line
                continue

            # is it a section?
            if groups['section']:
                # extract the family name
                family = groups['family'].strip().split('.')
                # extract the component name
                name = groups.get('name', '')
                # grab the next line
                continue

        # return the event list
        return configuration


# end of file 
