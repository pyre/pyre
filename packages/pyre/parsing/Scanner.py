# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import io
import pyre.tracking
# my superclass
from .Lexer import Lexer


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
    def pyre_tokenize(self, uri, stream):
        """
        Convert the input {stream} into tokens
        """
        # print(' ++ pyre.parsing.Scanner:')
        # print('      uri={}'.format(uri))
        # print('      stream={}'.format(stream))
        # if the {stream} is not open in text mode
        if not isinstance(stream, io.TextIOBase):
            # wrap a {io.TextIOWrapper} around it
            stream = io.TextIOWrapper(stream)
        # clear out the token cache
        self.pyre_cache = []
        # tokenize the stream
        for token in self._pyre_tokenize(uri=uri, stream=stream):
            # first empty out the token cache, in case there was push back during processing
            yield from self.pyre_cache
            # then send the current token
            yield token
        # all done
        return


    def pyre_pushback(self, token):
        """
        Push a token back into the token stream
        """
        # do it
        self.pyre_cache.append(token)
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.pyre_cache = []
        return


    # implementation details
    def _pyre_tokenize(self, uri, stream):
        """
        Convert the contents of the input source into a token stream
        """
        # the locator factory
        locator = pyre.tracking.file
        # send a {start} token
        yield self.start(locator=locator(source=uri, line=1, column=0))

        # iterate over the contents of the stream
        for line, text in enumerate(stream):
            # reset the column
            column = 0
            # scan until the end of the line
            while column != len(text):
                # attempt to recognize the contents of the line
                match = self.pyre_recognizer.match(text, pos=column)
                # if it failed
                if not match:
                    # build an error descriptor
                    error = self.TokenizationError(
                        text=text[column:], locator=locator(source=uri, line=line+1, column=column))
                    # invoke the error handler
                    self._pyre_handleError(error=error)
                    # and skip the rest of this line
                    break
                # we have a match; find the name of the matching token
                name = match.lastgroup
                # get the token class
                tokenFactory = getattr(self, name)
                # make a token
                token = tokenFactory(
                    lexeme = match.group(name),
                    locator = locator(source=uri, line=line+1, column=column)
                    )
                # and attempt to
                try:
                    # toss it back to the caller
                     yield token
                # if anything goes wrong during the processing
                except self.ParsingError as error:
                    # invoke the error handler
                    self._pyre_handleError(error=error)
                    # and skip the rest of this line
                    break
                # update the column counter
                column = match.end()

        # send a {finish} token
        yield self.finish(locator=locator(source=uri, line=line+1, column=0))
        # all done
        return


    def _pyre_handleError(self, error):
        """
        Invoked when the scanner encounters an error
        """
        # by default, throw the error
        raise error


    # private data
    pyre_cache = [] # the list of tokens that have been pushed back
    # set by {Lexer}
    pyre_tokens = None # a list of my tokens
    pyre_recognizer = None # the compiled regex constructed out the patterns of my tokens


# end of file 
