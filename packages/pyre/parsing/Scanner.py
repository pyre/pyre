# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import io
from ..patterns import coroutine
from ..tracking import file as fileloc # i make file locators
# my superclass
from .Lexer import Lexer


# class declaration
class Scanner(metaclass=Lexer):
    """
    The input stream tokenizer
    """


    # types
    # exceptions
    from .exceptions import ParsingError, TokenizationError
    # the descriptor factory
    from .Descriptor import Descriptor as pyre_token
    # the default tokens; all scanners have these
    start = pyre_token()
    finish = pyre_token()
    whitespace = pyre_token(pattern=r'\s+')


    # interface
    def pyre_tokenize(self, uri, stream, client):
        # show me
        # print(' ++ pyre.parsing.Scanner:')
        # print('      uri={}'.format(uri))
        # print('      stream={}'.format(stream))
        # print('      client={}'.format(client))

        # if the {stream} is not open in text mode
        if not isinstance(stream, io.TextIOBase):
            # wrap a {io.TextIOWrapper} around it
            stream = io.TextIOWrapper(stream)
            # show me
            # print('        now open in text mode')

        # flush the token cache
        self.pyre_cache = []

        # to get things going, build a {start} token
        start = self.start(locator=fileloc(source=uri, line=1, column=0))
        # and send it along
        client.send(start)

        # fault detection
        fault = None
        # iterate over the contents of the stream
        for line, text in enumerate(stream):
            # reset the column number
            column = 0
            # scan until then end of the line
            while column != len(text):
                # print('at line={}, column={}'.format(line+1, column))
                # send all tokens currently in the token cache
                for token in self.pyre_cache: client.send(token)
                # and flush it
                self.pyre_cache = []

                # attempt to recognize the contents of the line
                match = self.pyre_recognizer.match(text, pos=column)
                # if i failed to recognize a valid token
                if not match:
                    # if this didn't just happen
                    if not fault:
                        # build an error descriptor
                        fault = self.TokenizationError(
                            text = text[column:],
                            locator = fileloc(source=uri, line=line+1, column=column))
                        # invoke the downstream error handler
                        client.throw(self.TokenizationError, fault)
                    # carry on: skip the current character
                    column += 1
                    # and try again
                    continue

                # we have a match; clear the fault indicator
                fault = None
                # lookup the name of the token
                name = match.lastgroup
                # get the token class
                factory = getattr(self, name)
                # make a token
                token = factory(
                    lexeme = match.group(name),
                    locator = fileloc(source=uri, line=line+1, column=column))

                # show me
                # print(token)
                # process it
                client.send(token)
                # if all went well, update the column counter and move on
                column = match.end()

        # all done; make a {finish} token
        finish = self.finish(locator=fileloc(source=uri, line=line+1, column=0))
        # and send it
        client.send(finish)
        # all done
        return


    def pyre_pushback(self, token):
        """
        Push a token back into the token stream
        """
        # do it
        self.pyre_cache.append(token)
        # all done
        return self


    # helpers
    @coroutine
    def pyre_ignoreWhitespace(self, client):
        """
        Remove {whitespace} tokens from the input stream
        """
        # support for upstream error notification
        fault = None
        # for ever
        while True:
            # attempt to
            try:
                # get a token
                token = yield fault
            # if anything goes wrong
            except self.ParsingError as error:
                # forward it to my client
                client.throw(type(error), error)

            # if it is not whitespace
            if not isinstance(token, self.whitespace):
                # pass it along
                fault = client.send(token)
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # storage for pushed back tokens
        self.pyre_cache = []
        # all done
        return


    # implementation details
    # private data
    pyre_cache = [] # the list of tokens that have been pushed back
    # set by {Lexer}
    pyre_tokens = None # a list of my tokens
    pyre_recognizer = None # the compiled regex constructed out the patterns of my tokens


# end of file
