# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import re
from ..tracking import file as fileloc # i make file locators
# superclass
from .Scanner import Scanner


# declaration
class SWScanner(Scanner):
    """
    A scanner for languages that use leading whitespace to indicate the hierarchical structure
    of the content
    """


    # exceptions
    from .exceptions import IndentationError
    # tokens
    beginBlock = Scanner.pyre_token()
    endBlock = Scanner.pyre_token()
    comment = Scanner.pyre_token(head=r'(?<!\\)#', pattern='.*', tail='$')

    # implementation details
    def pyre_newline(self, line, text):
        """
        A fresh line was retrieved from the input stream
        """
        # my obligations are to
        #   discover the indentation level and issue the relevant block tokens
        #   indicate where in the line the scanner is going to start looking for tokens

        # look for leading whitespace
        margin = self.margin.match(text)
        # if there isn't any
        if not margin:
            # punt
            return 0
        # grab the location of the first non-whitespace character
        edge = margin.end()
        # the rest of the line
        rest = text[edge:].strip()
        # if the rest is blank or just a comment
        if not rest or self.comment.scanner.match(rest):
            # punt
            return 0
        # at this point we have a non-trivial line with leading whitespace; find out how much
        leader = margin.end()
        # get the current indentation level
        current = self.pyre_leader

        # if we are at the same indentation level
        if leader == current:
            # nothing to do
            return edge

        # get the input stream URI
        uri = self.pyre_uri
        # grab the indentation stack
        indentation = self.pyre_indentation

        # if this is the start of a new block
        if leader > current:
            # make a token to mark the beginning of the block
            token = self.beginBlock(locator=fileloc(source=uri, line=line+1, column=0))
            # send it on
            self.pyre_client.send(token)
            # save the current indentation level
            indentation.append(current)
            # and adjust the current one
            self.pyre_leader = leader
            # all done
            return edge

        # otherwise, we are closing
        token = self.endBlock(locator=fileloc(source=uri, line=line+1, column=0))
        # enough open blocks to get to the new indentation level
        while leader < current:
            # mark the end of a block
            self.pyre_client.send(token)
            # and update the indentation level
            current = indentation.pop()

        # save the indentation level
        self.pyre_leader = leader
        # check that this brought us back to a consistent indentation level
        if leader != current:
            # and if not, build a description of the problem
            fault = self.IndentationError(
                text = '',
                locator = fileloc(source=uri, line=line+1, column=0))
            # and invoke the downstream error handler
            client.throw(self.TokenizationError, fault)

        # skip over the whitespace margin
        return edge


    def pyre_start(self, **kwds):
        """
        Scanning has begun
        """
        # initialize the current indentation position
        self.pyre_leader = 0
        # the indentation stack
        self.pyre_indentation = []
        # and chain up
        return super().pyre_start(**kwds)


    def pyre_finish(self, line):
        """
        Scanning has ended
        """
        # at the end-of-file, the current indentation is 0
        leader = 0
        # the current indent level
        current = self.pyre_leader
        # make a end-of-block token
        token = self.endBlock(locator=fileloc(source=self.pyre_uri, line=line+1, column=0))
        # enough open blocks to get to the new indentation level
        for level in self.pyre_indentation:
            # mark the end of a block
            self.pyre_client.send(token)

        # clean up my local state
        self.pyre_leader = 0
        self.pyre_indentation = []

        # and chain up for the rest of the clean up
        return super().pyre_finish(line=line)


    # my indentation scanner
    margin = re.compile(r' *') # only spaces; tabs are an error


# end of file
