# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre.parsing
import pyre.tracking


# the parser
class Parser(pyre.parsing.parser):
    """
    A simple parser for {cfg} files

    This parser understands a variant of the windows {INI} file format. See the package
    documentation for details.
    """


    # types
    from .exceptions import ParsingError
    from ..events import Assignment, ConditionalAssignment
    from .Scanner import Scanner as lexer # my superclass uses this to instantiate my scanner


    # interface
    def parse(self, uri, stream, locator):
        """
        Harvest the configuration events in {stream}
        """
        # initialize my context
        self.name = []
        self.family = []
        # tokenize the {stream}
        tokens = self.scanner.pyre_tokenize(uri=uri, stream=stream)
        # process the tokens
        for token in tokens:
            # look up the relevant production based on this terminal
            production = self.productions[type(token)]
            # and invoke it
            production(current=token, rest=tokens)
        # all done
        return self.configuration


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the list of harvested configuration events
        self.configuration = []
        # the production table
        self.productions = {
            # the ignorables
            self.scanner.start: self.ignore,
            self.scanner.comment: self.ignore,
            self.scanner.whitespace: self.ignore,
            self.scanner.finish: self.ignore,

            # context specifier
            self.scanner.secbeg: self.context,
            # assignment
            self.scanner.key: self.assignment
            }
        # all done
        return


    # implementation details
    def ignore(self, **kwds):
        """
        Do nothing
        """
        return


    def context(self, current, rest):
        """
        Process a section fragment and use it to specify the assignment context
        """
        # current is guaranteed to be a '['; get the next one
        current = next(rest)
        # if it is not a {key}
        if type(current) is not self.scanner.key:
            # we have an error
            msg = "expected an identifier; got {}".format(current)
            raise self.ParsingError(description=msg, locator=current.locator)
        # set the family to the lexeme
        self.family = current.lexeme.split('.')

        # get the next token
        current = next(rest)

        # if it is a {secend} marker
        if type(current) is self.lexer.secend:
            # clear the component name
            self.name = ()
            # and we are done
            return

        # if it is not a name marker
        if type(current) is not self.scanner.marker:
            # we have an error
            msg = "expected a '#'; got {}".format(current)
            raise self.ParsingError(description=msg, locator=current.locator)

        # get the next token
        current = next(rest)
        # if it is not a key
        if type(current) is not self.scanner.key:
            # we have an error
            msg = "expected an identifier; got {}".format(current)
            raise self.ParsingError(description=msg, locator=current.locator)
        # set the name to the lexeme
        self.name = current.lexeme.split('.')

        # get the next token
        current = next(rest)
        # if it is not a {secend} marker
        if type(current) is not self.lexer.secend:
            # we have an error
            msg = "expected a ']'; got {}".format(current)
            raise self.ParsingError(description=msg, locator=current.locator)

        # all done
        return

   
    def assignment(self, current, rest):
        """
        Process a key assignment
        """
        # get the key
        key = current.lexeme.split('.')
        # save its locator
        locator = current.locator
        # grab the next token
        current = next(rest)
        # if it is a value
        if type(current) is self.scanner.value:
            # extract it
            value = current.lexeme.strip()
        # otherwise
        else:
            # push it back
            self.scanner.pyre_pushback(current)
            # build an empty value
            value = None

        # time to build an assignment; if the component name is not empty
        if self.name:
            # build a conditional assignment
            event = self.ConditionalAssignment(
                component = self.name + key[:-1],
                condition = (self.name, self.family),
                key = key[-1:], value = value,
                locator = locator)
        # otherwise
        else:
            # build an unconditional assignment 
            event = self.Assignment(key = self.family + key, value = value, locator = locator)
        # in any case, add it to the pile
        self.configuration.append(event)
        # and return
        return


    # private data
    name = () # context: the current component name
    family = () # context: the current component family
    productions = None # the table of token handlers
    configuration = None # the list of configuration events harvested from the input source


# end of file
