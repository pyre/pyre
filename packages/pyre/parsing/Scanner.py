# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre.tracking
from .Lexer import Lexer


class Scanner(metaclass=Lexer):
    """
    The input stream tokenizer
    """

    # pull the token descriptor factory
    from . import token

    # the default tokens: the scanner always generates this
    start = token()
    finish = token()
    whitespace = token(r"\s+")


    # constants
    ignoreWhitespace = True


    # public data
    stream = None
    tokens = None
    line = 0
    column = 0
    filename = ""

    @property
    def locator(self):
        from pyre.tracking.File import File
        return File(source=self.filename, line=self.line, column=self.column)


    # interface
    def tokenize(self, stream):
        # clear out the token cache
        self.tokens = []
        # clear out my location in the stream
        self.line = 0
        self.column = 0
        # record the name of the stream
        try:
            self.filename = stream.name
        except AttributeError:
            self.filename = "{unknown}"
        # indicate the beginning of tokenization 
        yield self.start(locator=self.locator)
        # tokenize the stream
        for token in self._tokenize(stream):
            # first, empty out any tokens that may have been pushed back
            for cached in self._tokenCache:
                yield cached
            # when that's done, return the current token
            yield token
        # indicate the end of the tokenization stream
        self.column = 0
        yield self.finish(locator=self.locator)
        # and terminate the iteration
        return


    def pushback(self, token):
        """
        Push a token back into the token stream
        """
        self._tokenCache.append(token)
        return self


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._tokenCache = []
        return

    # interface
    def _tokenize(self, stream):
        # iterate over the contents of the stream
        for line in stream:
            # reset the column position
            self.column = 0
            # skip whitespace
            while self.column != len(line):
                # skip whitespace
                if self.ignoreWhitespace:
                    match = self.whitespace.recognizer.match(line, self.column)
                    if match:
                        self.column = match.end()
                        if self.column == len(line):
                            break
                # attempt to recognize the contents of the line
                match = self.recognizer.match(line, self.column)
                if not match:
                    raise self.TokenizationError(locator=self.locator, text=line[self.column:])
                # we got one
                matches = match.groupdict()
                # figure out what it was by looking for a non-empty group that matches the
                # token class names
                for token in self.pyre_tokens:
                    text = matches[token.__name__]
                    if text:
                        yield token(lexeme=text, locator=self.locator)
                        break
                # update the column counter
                self.column = match.end()
            # update the line counter
            self.line += 1
            
        # done with the file
        return


    # exceptions
    from .exceptions import TokenizationError


# end of file 
