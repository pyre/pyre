# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import xml.sax


class Reader(xml.sax.ContentHandler):
    """
    An event driver reader for XML documents
    """


    # public data
    ignoreWhitespace = False


    # interface
    def read(self, *, stream, document, features=(), saxparser=None):
        """
        Buld a representation of the information in {stream}

        parameters:
            {stream}: a URI or file-like object
            {document}: an instance of the Document data structure to be decorated with the
                        contents of {stream}
            {saxparser}: the SAX style parser to use; defaults to xml.sax.make_parser()
            {features}: the optional parsing features to enable; expected to be a tuple of
                        (feature, value) pairs; for more details, see the builtin package
                        xml.sax or your parser's documentation

        The Reader attempts to normalize the exceptions that may be generated while attempting
        to understand the XML document using the exception classes in this package. This
        mechanism fails if you supply your own parser, so you must be ready to catch any
        exceptions it may generate
        """

        # attach the document
        self._document = document
        # create a parser
        parser = saxparser or xml.sax.make_parser()

        # apply the optional features
        unsupported = []
        for feature, value in features:
            try:
                parser.setFeature(feature, value)
            except xml.sax.SAXNotSupportedException:
                unsupported.append(feature)
        # raise an exception if any requests could not be satisfied
        if unsupported:
            raise self.UnsupportedFeatureError(self, document, unsupported)

        # parse
        parser.setContentHandler(self)
        try:
            parser.parse(stream)
        except xml.sax.SAXParseException as error:
            # something bad happened; normalize the exception
            raise self.ParsingError(
                parser=self, document=document, description=error.getMessage(),
                locator=self._locator) from error
        # clean up
        parser.setContentHandler(None)
        # and return the decorated data structure
        return self._document.dom


    # content handling: these methods are called by the underlying parser
    def startDocument(self):
        """
        """


    # exceptions
    from . import ParsingError, UnsupportedFeatureError


# end of file 
