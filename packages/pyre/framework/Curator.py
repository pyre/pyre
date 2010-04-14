# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import re


class Curator(object):
    """
    """


    # public data
    sources = ()


    # interface
    def loadConfiguration(self, source):
        """
        Load configuration setting from {source}
        """


    # lower level interface
    def parseURI(self, uri):
        """
        Extract the scheme, address and fragment from {uri}.
        """
        # run uri through the recognizer
        match = self._uriRecognizer.match(uri)
        # if it fails to match, it must be malformed (or my regex is bad...)
        if match is None:
            raise self.BadResourceLocator(uri=uri, reason="unrecognizable")
        # extract the scheme
        scheme = match.group("scheme") or self.defaultMethod
        scheme = scheme.strip().lower()
        # extract the addres
        address = match.group("address")
        # check that it's not blank
        if not address:
            raise self.BadResourceLocator(uri=uri, reason="missing address")
        # extract the fragment
        fragment = match.group("fragment")
        # and return the triplet
        return scheme, address, fragment


    # meta methods
    def __init__(self):
        self.sources = []
        return


    # exceptions
    from . import BadResourceLocator


    # constants
    defaultMethod = "file"


    # private data
    _uriRecognizer = re.compile(
        r"((?P<scheme>[^:]+)://)?(?P<address>[^#]*)(#(?P<fragment>.*))?"
        )

    # from http://regexlib.com/Search.aspx?k=URL
    r"""
    ^(?=[^&])
    (?:(?<scheme>[^:/?#]+):)?
    (?://(?<authority>[^/?#]*))?
    (?<path>[^?#]*)(?:\?(?<query>[^#]*))?
    (?:#(?<fragment>.*))?
    """


# end of file 
