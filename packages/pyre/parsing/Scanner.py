# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
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
    # the stream wrapper
    from .InputStream import InputStream as pyre_inputStream
    # the default tokens; all scanners have these
    start = pyre_token()
    finish = pyre_token()
    whitespace = pyre_token(pattern=r'\s+')


    # interface
    def pyre_tokenize(self, uri, stream, client):
        """
        Extract lines from {stream}, convert them into token streams and send them to {client}
        """
        # show me
        # print(' ++ pyre.parsing.Scanner:')
        # print('      uri={}'.format(uri))
        # print('      stream={}'.format(stream))
        # print('      client={}'.format(client))

        # flush the token cache
        self.pyre_cache = []

        # to get things going, build a {start} token and pass it along to the {client}
        self.pyre_start(client=client, uri=uri, stream=stream)

        # fault detection
        fault = None
        # iterate over the contents of the stream
        for line, text in self.pyre_readlines():
            # reset the column number
            column = self.pyre_newline(line=line, text=text)
            # scan until then end of the line
            while column != len(text):
                # show me where I am
                # print('at line={}, column={}'.format(line+1, column))
                # and what is in the cache
                # print('token cache: {.pyre_cache}'.format(self))
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

        # wrap up by sending a {finish} token to the {client}
        self.pyre_finish(line=line)

        # all done
        return


    def pyre_readlines(self):
        """
        Pull and number lines from my stream
        """
        # my input stream wrapper knows what to do
        return self.pyre_stream


    def pyre_start(self, uri, client, stream):
        """
        Indicate the beginning of scanning
        """
        # save the source information
        self.pyre_uri = uri
        self.pyre_stream = self.pyre_inputStream(stream=stream)
        self.pyre_client = client
        # to get things going, build a {start} token
        start = self.start(locator=fileloc(source=uri, line=1, column=0))
        # and send it along
        self.pyre_client.send(start)
        # all done
        return


    def pyre_finish(self, line):
        """
        Indicate that scanning is complete
        """
        # to wrap things up, build a {finish} token
        finish = self.finish(locator=fileloc(source=self.pyre_uri, line=line+1, column=0))
        # and send it along
        self.pyre_client.send(finish)

        # reset the state
        self.pyre_uri = None
        self.pyre_stream = None
        self.pyre_client = None

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


    def pyre_newline(self, line, text):
        """
        Hook invoked when a new line of text is pulled from the input stream
        """
        # nothing to do by default; just reset the column number
        return 0


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


    # implementation details
    # set by my meta-class
    pyre_tokens = None # a list of my tokens
    pyre_recognizer = None # the compiled regex constructed out the patterns of my tokens

    # tokenizing state
    pyre_uri = None
    pyre_stream = None
    pyre_client = None
    pyre_cache = [] # the list of tokens that have been pushed back


# end of file
