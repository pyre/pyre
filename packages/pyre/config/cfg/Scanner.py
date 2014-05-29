# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import pyre.parsing
import pyre.patterns


# the scanner
class Scanner(pyre.parsing.scanner):
    """
    Converts an input source into a stream of tokens. The input is expected to conform to a
    simple version of the well-known windows INI format.
    """


    # my tokens, in addition to the three inherited from {pyre.parsing.scanner}
    marker = pyre.parsing.token(pattern=r'#')
    secbeg = pyre.parsing.token(pattern=r'\[')
    secend = pyre.parsing.token(pattern=r'\]')
    comment = pyre.parsing.token(head=';', pattern=r'.*', tail='$')
    key = pyre.parsing.token(pattern=r'\w[-.:\w]*')
    value = pyre.parsing.token(head='=', pattern=r'[^;]*')


    # interface
    def pyre_tokenize(self, uri, stream, client):
        """
        Convert the input {stream} into tokens that are not whitespace
        """
        # adjust the client
        filtered = self.pyre_ignoreWhitespace(client)
        # and process the token stream
        return super().pyre_tokenize(uri=uri, stream=stream, client=filtered)


    # implementation details
    @pyre.patterns.coroutine
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

        
# end of file 
