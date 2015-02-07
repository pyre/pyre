# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# exceptions
from ..exceptions import NexusError


# local anchor
class ProtocolError(NexusError):
    """
    Base exceptions for all error conditions detected by http components
    """

    # meta-methods
    def __init__(self, server, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the server reference
        self.server = server
        # all done
        return


    def __str__(self):
        """
        The default rendering of protocol errors
        """
        return """
        <head>
          <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
          <title>Unhappy web server - {0.server.name}</title>
        </head>
        <body>
          <h1>Something went very wrong</h1>
          <p>
            The server <em>{0.server.name}</em> is very unhappy and returned error code {0.code}.
          </p>
          <p>The standard description for this error is: {0.__doc__}</p>
          <p>{0.description}</p>
        </body>
        """.format(self)


# specific errors
class ContinueError(ProtocolError):
    """
    Continue
    """
    # state
    code = 100
    description = "Request received, please continue"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class SwitchingProtocolsError(ProtocolError):
    """
    Switching Protocols
    """
    # state
    code = 101
    description = "Switching to new protocol; obey Upgrade header"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class OKError(ProtocolError):
    """
    OK
    """
    # state
    code = 200
    description = "Request fulfilled, document follows"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class CreatedError(ProtocolError):
    """
    Created
    """
    # state
    code = 201
    description = "Document created, URL follows"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class AcceptedError(ProtocolError):
    """
    Accepted
    """
    # state
    code = 202
    description = "Request accepted, processing continues off-line"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NonAuthoritativeInformationError(ProtocolError):
    """
    Non-Authoritative Information
    """
    # state
    code = 203
    description = "Request fulfilled from cache"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NoContentError(ProtocolError):
    """
    No Content
    """
    # state
    code = 204
    description = "Request fulfilled, nothing follows"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ResetContentError(ProtocolError):
    """
    Reset Content
    """
    # state
    code = 205
    description = "Clear input form for further input."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PartialContentError(ProtocolError):
    """
    Partial Content
    """
    # state
    code = 206
    description = "Partial content follows."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class MultipleChoicesError(ProtocolError):
    """
    Multiple Choices
    """
    # state
    code = 300
    description = "Object has several resources -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class MovedPermanentlyError(ProtocolError):
    """
    Moved Permanently
    """
    # state
    code = 301
    description = "Object moved permanently -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class FoundError(ProtocolError):
    """
    Found
    """
    # state
    code = 302
    description = "Object moved temporarily -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class SeeOtherError(ProtocolError):
    """
    See Other
    """
    # state
    code = 303
    description = "Object moved -- see Method and URL list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotModifiedError(ProtocolError):
    """
    Not Modified
    """
    # state
    code = 304
    description = "Document has not changed since given time"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class UseProxyError(ProtocolError):
    """
    Use Proxy
    """
    # state
    code = 305
    description = "You must use proxy specified in Location to access this resource."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class TemporaryRedirectError(ProtocolError):
    """
    Temporary Redirect
    """
    # state
    code = 307
    description = "Object moved temporarily -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class BadRequestSyntaxError(ProtocolError):
    """
    Bad Request
    """
    # state
    code = 400
    description = "Bad request syntax or unsupported method"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class UnauthorizedError(ProtocolError):
    """
    Unauthorized
    """
    # state
    code = 401
    description = "No permission -- see authorization schemes"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PaymentRequiredError(ProtocolError):
    """
    Payment Required
    """
    # state
    code = 402
    description = "No payment -- see charging schemes"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ForbiddenError(ProtocolError):
    """
    Forbidden
    """
    # state
    code = 403
    description = "Request forbidden -- authorization will not help"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotFoundError(ProtocolError):
    """
    Not Found
    """
    # state
    code = 404
    description = "Nothing matches the given URI"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class MethodNotAllowedError(ProtocolError):
    """
    Method Not Allowed
    """
    # state
    code = 405
    description = "Specified method is invalid for this resource."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotAcceptableError(ProtocolError):
    """
    Not Acceptable
    """
    # state
    code = 406
    description = "URI not available in preferred format."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ProxyAuthenticationRequiredError(ProtocolError):
    """
    Proxy Authentication Required
    """
    # state
    code = 407
    description = "You must authenticate with this proxy before proceeding."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestTimeoutError(ProtocolError):
    """
    Request Timeout
    """
    # state
    code = 408
    description = "Request timed out; try again later."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ConflictError(ProtocolError):
    """
    Conflict
    """
    # state
    code = 409
    description = "Request conflict."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class GoneError(ProtocolError):
    """
    Gone
    """
    # state
    code = 410
    description = "URI no longer exists and has been permanently removed."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class LengthRequiredError(ProtocolError):
    """
    Length Required
    """
    # state
    code = 411
    description = "Client must specify Content-Length."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PreconditionFailedError(ProtocolError):
    """
    Precondition Failed
    """
    # state
    code = 412
    description = "Precondition in headers is false."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestEntityTooLargeError(ProtocolError):
    """
    Request Entity Too Large
    """
    # state
    code = 413
    description = "Entity is too large."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestURITooLongError(ProtocolError):
    """
    Request-URI Too Long
    """
    # state
    code = 414
    description = "URI is too long."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class UnsupportedMediaTypeError(ProtocolError):
    """
    Unsupported Media Type
    """
    # state
    code = 415
    description = "Entity body in unsupported format."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestedRangeNotSatisfiableError(ProtocolError):
    """
    Requested Range Not Satisfiable
    """
    # state
    code = 416
    description = "Cannot satisfy request range."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ExpectationFailedError(ProtocolError):
    """
    Expectation Failed
    """
    # state
    code = 417
    description = "Expect condition could not be satisfied."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PreconditionRequiredError(ProtocolError):
    """
    Precondition Required
    """
    # state
    code = 428
    description = "The origin server requires the request to be conditional."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class TooManyRequestsError(ProtocolError):
    """
    Too Many Requests
    """
    # state
    code = 429
    description = "The user has sent too many requests in a given amount of time (rate limiting)."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestHeaderFieldsTooLargeError(ProtocolError):
    """
    Request Header Fields Too Large
    """
    # state
    code = 431
    description = ("The server is unwilling to process the request because its header fields "
                  "are too large.")

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class InternalServerError(ProtocolError):
    """
    Internal Server Error
    """
    # state
    code = 500
    description = "Server got itself in trouble"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotImplementedError(ProtocolError):
    """
    Not Implemented
    """
    # state
    code = 501
    description = "Server does not support this operation"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class BadGatewayError(ProtocolError):
    """
    Bad Gateway
    """
    # state
    code = 502
    description = "Invalid responses from another server/proxy."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ServiceUnavailableError(ProtocolError):
    """
    Service Unavailable
    """
    # state
    code = 503
    description = "The server cannot process the request due to a high load"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class GatewayTimeoutError(ProtocolError):
    """
    Gateway Timeout
    """
    # state
    code = 504
    description = "The gateway server did not receive a timely response"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class HTTPVersionNotSupportedError(ProtocolError):
    """
    HTTP Version Not Supported
    """
    # state
    code = 505
    description = "Cannot fulfill request."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NetworkAuthenticationRequiredError(ProtocolError):
    """
    Network Authentication Required
    """
    # state
    code = 511
    description = "The client needs to authenticate to gain network access."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


# end of file
