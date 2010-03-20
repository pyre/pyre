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
        Handler for the beginning of the document
        """
        # print(
            # "line {0}, col {1}: start document".format(
                # self._locator.getLineNumber(), self._locator.getColumnNumber()))

        # initialize the parsing variables
        self._nodeStack = []
        self._currentNode = self._document

        # notify the document that parsing has begun
        self._document.initialize(locator=self._locator)

        return


    def startElement(self, name, attributes):
        """
        Handler for the beginning of an element
        """
        # print(
            # "line {0}, col {1}: start element {2!r}".format(
                # self._locator.getLineNumber(), self._locator.getColumnNumber(), name))

        # get the current node to build me a rep for the requested child node
        try:
            node = self._currentNode.newNode(
                name=name, attributes=attributes, locator=self._locator)
        # either bad document or a bad handler constructor
        except TypeError as error:
            msg = "could not instantiate handler for node {0!r}; extra attributes?".format(name)
            raise self.DTDError(
                    parser=self, document=self._document,
                    description=msg, locator=self._locator) from error
        # the current node doesn't permit this particular child node
        except KeyError as error:
            msg = "could not locate handler for node {0!r} in {1!r}".format(
                name, self._currentNode.__class__)
            raise self.DTDError(
                    parser=self, document=self._document,
                    description=msg, locator=self._locator) from error

        # push the current node on the stack
        self._nodeStack.append(self._currentNode)
        # and make the new node the focus of attention
        self._currentNode = node

        return


    def characters(self, content):
        """
        Handler for the content of a tag
        """

        if self.ignoreWhitespace:
            content = content.strip()

        if content:
            # print(
                # "line {0}, col {1}: characters {2!r}".format(
                    # self._locator.getLineNumber(), self._locator.getColumnNumber(), content))
            try:
                # get the current node handler to process the element content
                self._currentNode.content(text=content, locator=self._locator)
            except AttributeError as error:
                # raise an error if it doesn't have one
                msg = "element {0._currentNode.tag!r} does not accept character data".format(self)
                raise self.DTDError(
                    parser=self, document=self._document,
                    description=msg, locator=self._locator) from error

        return


    def endElement(self, name):
        """
        Handler for the end of an element
        """
        # print(
            # "line {0}, col {1}: end element {2!r}".format(
                # self._locator.getLineNumber(), self._locator.getColumnNumber(), name))

        # grab the current node and its parent
        node = self._currentNode
        self._currentNode = self._nodeStack.pop()

        # let the parent node know we reached an element end
        try:
            node.notify(parent=self._currentNode, locator=self._locator)
        except Exception as error:
            msg = "error while calling the method 'notify' of {0}".format(self._currentNode)
            raise self.ProcessingError(
                parser=self, document=self._document,
                description=msg, locator=self._locator) from error
            
        return


    def endDocument(self):
        """
        Handler for the end of the document
        """

        # print(
            # "line {0}, col {1}: end document".format(
                # self._locator.getLineNumber(), self._locator.getColumnNumber()))

        self._document.finalize(locator=self._locator)

        self._nodeStack = []
        self._currentNode = None

        return




    # exceptions
    from . import DTDError, ParsingError, ProcessingError, UnsupportedFeatureError


# end of file 
