# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# class declaration
class Response:
    """
    Encapsulation of the HTTP response codes, their standard names, and a human readable
    explanation of the response type
    """


    # interface
    def error(self, code):
        """
        Build an error response with the given code
        """
        # get the message and the explanation
        message, explanation = self.responses[code]
        # build the description
        page = self.errorTemplate.format(code, message, explanation).encode('utf-8', 'strict')

        # build the headers
        headers = '\r\n'.join([
            # the top line
            "HTTP/1.1 {} {}".format(code, message),
            # the error content type
            "Content-Type: text/html;charset=utf-8",
            # what to do with the connection
            "Connection: close",
            # how much stuff we are sending
            "Content-Length: {}".format(len(page)),
            ]).encode('latin-1', 'strict')

        # build the response
        return b'\r\n'.join([headers, b'', page])


    # implementation details
    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols', 'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted', 'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices', 'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified', 'Document has not changed since given time'),
        305: ('Use Proxy', 'You must use proxy specified in Location to access this resource.'),
        307: ('Temporary Redirect', 'Object moved temporarily -- see URI list'),

        400: ('Bad Request', 'Bad request syntax or unsupported method'),
        401: ('Unauthorized', 'No permission -- see authorization schemes'),
        402: ('Payment Required', 'No payment -- see charging schemes'),
        403: ('Forbidden', 'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed', 'Specified method is invalid for this resource.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required',
              'You must authenticate with this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone', 'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable', 'Cannot satisfy request range.'),
        417: ('Expectation Failed', 'Expect condition could not be satisfied.'),
        428: ('Precondition Required', 'The origin server requires the request to be conditional.'),
        429: ('Too Many Requests',
              'The user has sent too many requests in a given amount of time ("rate limiting").'),
        431: ('Request Header Fields Too Large',
              'The server is unwilling to process the request because its header '
              'fields are too large.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented', 'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable', 'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout', 'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
        511: ('Network Authentication Required',
              'The client needs to authenticate to gain network access.'),
        }


    errorTemplate = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Error response</title>
        </head>
        <body>
            <h1>Error response</h1>
            <p>Error code: {0}</p>
            <p>Message: {1}</p>
            <p>Error code explanation: {0} - {2}</p>
        </body>
    </html>
    """



# end of file
