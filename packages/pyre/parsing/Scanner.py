# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import pyre.tracking
# my superclass
from .Lexer import Lexer


class Scanner(metaclass=Lexer):
    """
    The input stream tokenizer
    """


    # types
    # exceptions 
    from .exceptions import TokenizationError
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
        # clear out the token cache
        self.pyre_cache = []
        # tokenize the stream
        for token in self._pyre_tokenize(uri=uri, stream=stream):
            # first empty out the token cache
            for cached in self.pyre_cache: yield cached
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
                    # nothing more to do...
                    raise self.TokenizationError(
                        text=text[column:], locator=locator(source=uri, line=line+1, column=column))
                # we have a match; find the name of the matching token
                name = match.lastgroup
                # get the token class
                token = getattr(self, name)
                # make a token and toss it back
                yield token(
                    lexeme = match.group(name),
                    locator = locator(source=uri, line=line+1, column=column)
                    )
                # update the column counter
                column = match.end()

        # send a {finish} token
        yield self.finish(locator=locator(source=uri, line=line+1, column=0))
        # all done
        return


    # private data
    pyre_cache = [] # the list of tokens that have been pushed back
    # set by {Lexer}
    pyre_tokens = None # a list of my tokens
    pyre_recognizer = None # the compiled regex constructed out the patterns of my tokens


# end of file 
