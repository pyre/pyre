# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# exceptions
from .exceptions import Response, ProtocolError


# specific responses
class Continue(ProtocolError):
    """
    Continue
    """
    # state
    code = 100
    status = __doc__
    description = "Request received, please continue"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class SwitchingProtocols(ProtocolError):
    """
    Switching Protocols
    """
    # state
    code = 101
    status = __doc__
    description = "Switching to new protocol; obey Upgrade header"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class OK(Response):
    """
    OK
    """
    # state
    code = 200
    status = __doc__
    description = "Request fulfilled, document follows"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class Created(ProtocolError):
    """
    Created
    """
    # state
    code = 201
    status = __doc__
    description = "Document created, URL follows"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class Accepted(ProtocolError):
    """
    Accepted
    """
    # state
    code = 202
    status = __doc__
    description = "Request accepted, processing continues off-line"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NonAuthoritativeInformation(ProtocolError):
    """
    Non-Authoritative Information
    """
    # state
    code = 203
    status = __doc__
    description = "Request fulfilled from cache"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NoContent(ProtocolError):
    """
    No Content
    """
    # state
    code = 204
    status = __doc__
    description = "Request fulfilled, nothing follows"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ResetContent(ProtocolError):
    """
    Reset Content
    """
    # state
    code = 205
    status = __doc__
    description = "Clear input form for further input."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PartialContent(ProtocolError):
    """
    Partial Content
    """
    # state
    code = 206
    status = __doc__
    description = "Partial content follows."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class MultipleChoices(ProtocolError):
    """
    Multiple Choices
    """
    # state
    code = 300
    status = __doc__
    description = "Object has several resources -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class MovedPermanently(ProtocolError):
    """
    Moved Permanently
    """
    # state
    code = 301
    status = __doc__
    description = "Object moved permanently -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class Found(ProtocolError):
    """
    Found
    """
    # state
    code = 302
    status = __doc__
    description = "Object moved temporarily -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class SeeOther(ProtocolError):
    """
    See Other
    """
    # state
    code = 303
    status = __doc__
    description = "Object moved -- see Method and URL list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotModified(ProtocolError):
    """
    Not Modified
    """
    # state
    code = 304
    status = __doc__
    description = "Document has not changed since given time"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class UseProxy(ProtocolError):
    """
    Use Proxy
    """
    # state
    code = 305
    status = __doc__
    description = "You must use proxy specified in Location to access this resource."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class TemporaryRedirect(ProtocolError):
    """
    Temporary Redirect
    """
    # state
    code = 307
    status = __doc__
    description = "Object moved temporarily -- see URI list"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class BadRequestSyntax(ProtocolError):
    """
    Bad Request
    """
    # state
    code = 400
    status = __doc__
    description = "Bad request syntax or unsupported method"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class Unauthorized(ProtocolError):
    """
    Unauthorized
    """
    # state
    code = 401
    status = __doc__
    description = "No permission -- see authorization schemes"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PaymentRequired(ProtocolError):
    """
    Payment Required
    """
    # state
    code = 402
    status = __doc__
    description = "No payment -- see charging schemes"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class Forbidden(ProtocolError):
    """
    Forbidden
    """
    # state
    code = 403
    status = __doc__
    description = "Request forbidden -- authorization will not help"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotFound(ProtocolError):
    """
    Not Found
    """
    # state
    code = 404
    status = __doc__
    description = "Nothing matches the given URI"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class MethodNotAllowed(ProtocolError):
    """
    Method Not Allowed
    """
    # state
    code = 405
    status = __doc__
    description = "Specified method is invalid for this resource."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotAcceptable(ProtocolError):
    """
    Not Acceptable
    """
    # state
    code = 406
    status = __doc__
    description = "URI not available in preferred format."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ProxyAuthenticationRequired(ProtocolError):
    """
    Proxy Authentication Required
    """
    # state
    code = 407
    status = __doc__
    description = "You must authenticate with this proxy before proceeding."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestTimeout(ProtocolError):
    """
    Request Timeout
    """
    # state
    code = 408
    status = __doc__
    description = "Request timed out; try again later."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class Conflict(ProtocolError):
    """
    Conflict
    """
    # state
    code = 409
    status = __doc__
    description = "Request conflict."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class Gone(ProtocolError):
    """
    Gone
    """
    # state
    code = 410
    status = __doc__
    description = "URI no longer exists and has been permanently removed."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class LengthRequired(ProtocolError):
    """
    Length Required
    """
    # state
    code = 411
    status = __doc__
    description = "Client must specify Content-Length."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PreconditionFailed(ProtocolError):
    """
    Precondition Failed
    """
    # state
    code = 412
    status = __doc__
    description = "Precondition in headers is false."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestEntityTooLarge(ProtocolError):
    """
    Request Entity Too Large
    """
    # state
    code = 413
    status = __doc__
    description = "Entity is too large."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestURITooLong(ProtocolError):
    """
    Request-URI Too Long
    """
    # state
    code = 414
    status = __doc__
    description = "URI is too long."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class UnsupportedMediaType(ProtocolError):
    """
    Unsupported Media Type
    """
    # state
    code = 415
    status = __doc__
    description = "Entity body in unsupported format."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestedRangeNotSatisfiable(ProtocolError):
    """
    Requested Range Not Satisfiable
    """
    # state
    code = 416
    status = __doc__
    description = "Cannot satisfy request range."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ExpectationFailed(ProtocolError):
    """
    Expectation Failed
    """
    # state
    code = 417
    status = __doc__
    description = "Expect condition could not be satisfied."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class PreconditionRequired(ProtocolError):
    """
    Precondition Required
    """
    # state
    code = 428
    status = __doc__
    description = "The origin server requires the request to be conditional."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class TooManyRequests(ProtocolError):
    """
    Too Many Requests
    """
    # state
    code = 429
    status = __doc__
    description = "The user has sent too many requests in a given amount of time (rate limiting)."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class RequestHeaderFieldsTooLarge(ProtocolError):
    """
    Request Header Fields Too Large
    """
    # state
    code = 431
    status = __doc__
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
    status = __doc__
    description = "Server got itself in trouble"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NotImplemented(ProtocolError):
    """
    Not Implemented
    """
    # state
    code = 501
    status = __doc__
    description = "Server does not support this operation"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class BadGateway(ProtocolError):
    """
    Bad Gateway
    """
    # state
    code = 502
    status = __doc__
    description = "Invalid responses from another server/proxy."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class ServiceUnavailable(ProtocolError):
    """
    Service Unavailable
    """
    # state
    code = 503
    status = __doc__
    description = "The server cannot process the request due to a high load"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class GatewayTimeout(ProtocolError):
    """
    Gateway Timeout
    """
    # state
    code = 504
    status = __doc__
    description = "The gateway server did not receive a timely response"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class HTTPVersionNotSupported(ProtocolError):
    """
    HTTP Version Not Supported
    """
    # state
    code = 505
    status = __doc__
    description = "Cannot fulfill request."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class NetworkAuthenticationRequired(ProtocolError):
    """
    Network Authentication Required
    """
    # state
    code = 511
    status = __doc__
    description = "The client needs to authenticate to gain network access."

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


# end of file
