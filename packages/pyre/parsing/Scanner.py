# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Lexer import Lexer


class Scanner(object, metaclass=Lexer):
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


    # interface
    def tokenize(self, stream):
        # clear out the token cache
        self.tokens = []
        # clear out my location in the stream
        self.line = 0
        # indicate the beginning of tokenization 
        yield self.start()

        # iterate over the contents of the stream
        for line in stream:
            # print("line {0}".format(self.line))
            # reset the column position
            self.column = 0
            # skip whitespace
            while self.column != len(line):
                # print("    column {0}".format(self.column))
                # skip whitespace
                if self.ignoreWhitespace:
                    match = self.whitespace.recognizer.match(line, self.column)
                    if match:
                        # print("{{whitespace: line {0}, from column {1} to {2}}}".format(
                                # self.line, self.column, match.end()))
                        self.column = match.end()
                        if self.column == len(line):
                            break
                # attempt to recognize the contents of the line
                match = self.recognizer.match(line, self.column)
                if not match:
                    raise Exception
                
                matches = match.groupdict()
                for token in self._pyre_Tokens:
                    text = matches[token.__name__]
                    if text:
                        yield token(lexeme=text)
                        break

                self.column = match.end()
                
            # update the line counter
            self.line += 1
            
        # indicate that the end of file has been reached
        yield self.finish()
        # and terminate the iteration
        return


# end of file 
