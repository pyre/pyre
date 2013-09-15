# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import pyre.parsing


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
    def pyre_tokenize(self, uri, stream):
        """
        Convert the input {stream} into tokens that are not whitespace
        """
        # tokenize the input stream
        for token in super().pyre_tokenize(uri=uri, stream=stream):
            # filter out whitespace
            if type(token) is self.whitespace: continue
            # yield the token
            yield token

        # all done
        return

        
# end of file 
