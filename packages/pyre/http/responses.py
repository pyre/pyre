# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# exceptions
from .exceptions import ProtocolError


# specific responses
class Continue(ProtocolError):
    """
    Continue
    """

    # the status code
    code = 100
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Request received, please continue"


class SwitchingProtocols(ProtocolError):
    """
    Switching Protocols
    """

    # the status code
    code = 101
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Switching to new protocol; obey Upgrade header"


class Created(ProtocolError):
    """
    Created
    """

    # the status code
    code = 201
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Document created, URL follows"


class Accepted(ProtocolError):
    """
    Accepted
    """

    # the status code
    code = 202
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Request accepted, processing continues off-line"


class NonAuthoritativeInformation(ProtocolError):
    """
    Non-Authoritative Information
    """

    # the status code
    code = 203
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Request fulfilled from cache"


class NoContent(ProtocolError):
    """
    No Content
    """

    # the status code
    code = 204
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Request fulfilled, nothing follows"


class ResetContent(ProtocolError):
    """
    Reset Content
    """

    # the status code
    code = 205
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Clear input form for further input"


class PartialContent(ProtocolError):
    """
    Partial Content
    """

    # the status code
    code = 206
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Partial content follows"


class MultipleChoices(ProtocolError):
    """
    Multiple Choices
    """

    # the status code
    code = 300
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Object has several resources -- see URI list"


class MovedPermanently(ProtocolError):
    """
    Moved Permanently
    """

    # the status code
    code = 301
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Object moved permanently -- see URI list"


class Found(ProtocolError):
    """
    Found
    """

    # the status code
    code = 302
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Object moved temporarily -- see URI list"


class SeeOther(ProtocolError):
    """
    See Other
    """

    # the status code
    code = 303
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Object moved -- see Method and URL list"


class NotModified(ProtocolError):
    """
    Not Modified
    """

    # the status code
    code = 304
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Document has not changed since given time"


class UseProxy(ProtocolError):
    """
    Use Proxy
    """

    # the status code
    code = 305
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "You must use proxy specified in Location to access this resource"


class TemporaryRedirect(ProtocolError):
    """
    Temporary Redirect
    """

    # the status code
    code = 307
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Object moved temporarily -- see URI list"


class BadRequestSyntax(ProtocolError):
    """
    Bad Request
    """

    # the status code
    code = 400
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Bad request syntax or unsupported method"


class Unauthorized(ProtocolError):
    """
    Unauthorized
    """

    # the status code
    code = 401
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "No permission -- see authorization schemes"


class PaymentRequired(ProtocolError):
    """
    Payment Required
    """

    # the status code
    code = 402
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "No payment -- see charging schemes"


class Forbidden(ProtocolError):
    """
    Forbidden
    """

    # the status code
    code = 403
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Request forbidden -- authorization will not help"


class NotFound(ProtocolError):
    """
    Not Found
    """

    # the status code
    code = 404
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Nothing matches the given URI"


class MethodNotAllowed(ProtocolError):
    """
    Method Not Allowed
    """

    # the status code
    code = 405
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Specified method is invalid for this resource"


class NotAcceptable(ProtocolError):
    """
    Not Acceptable
    """

    # the status code
    code = 406
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "URI not available in preferred format"


class ProxyAuthenticationRequired(ProtocolError):
    """
    Proxy Authentication Required
    """

    # the status code
    code = 407
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "You must authenticate with this proxy before proceeding"


class RequestTimeout(ProtocolError):
    """
    Request Timeout
    """

    # the status code
    code = 408
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Request timed out; try again later"


class Conflict(ProtocolError):
    """
    Conflict
    """

    # the status code
    code = 409
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Request conflict"


class Gone(ProtocolError):
    """
    Gone
    """

    # the status code
    code = 410
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "URI no longer exists and has been permanently removed"


class LengthRequired(ProtocolError):
    """
    Length Required
    """

    # the status code
    code = 411
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Client must specify Content-Length"


class PreconditionFailed(ProtocolError):
    """
    Precondition Failed
    """

    # the status code
    code = 412
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Precondition in headers is false"


class RequestEntityTooLarge(ProtocolError):
    """
    Request Entity Too Large
    """

    # the status code
    code = 413
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Entity is too large"


class RequestURITooLong(ProtocolError):
    """
    Request-URI Too Long
    """

    # the status code
    code = 414
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "URI is too long"


class UnsupportedMediaType(ProtocolError):
    """
    Unsupported Media Type
    """

    # the status code
    code = 415
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Entity body in unsupported format"


class RequestedRangeNotSatisfiable(ProtocolError):
    """
    Requested Range Not Satisfiable
    """

    # the status code
    code = 416
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Cannot satisfy request range"


class ExpectationFailed(ProtocolError):
    """
    Expectation Failed
    """

    # the status code
    code = 417
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Expect condition could not be satisfied"


class PreconditionRequired(ProtocolError):
    """
    Precondition Required
    """

    # the status code
    code = 428
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "The origin server requires the request to be conditional"


class TooManyRequests(ProtocolError):
    """
    Too Many Requests
    """

    # the status code
    code = 429
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "The user has sent too many requests in a given amount of time (rate limiting)"


class RequestHeaderFieldsTooLarge(ProtocolError):
    """
    Request Header Fields Too Large
    """

    # the status code
    code = 431
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = (
        "The server is unwilling to process the request because its header fields " "are too large"
    )


class InternalServerError(ProtocolError):
    """
    Internal Server Error
    """

    # the status code
    code = 500
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Server got itself in trouble"


class NotImplemented(ProtocolError):
    """
    Not Implemented
    """

    # the status code
    code = 501
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Server does not support this operation"


class BadGateway(ProtocolError):
    """
    Bad Gateway
    """

    # the status code
    code = 502
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Invalid responses from another server/proxy"


class ServiceUnavailable(ProtocolError):
    """
    Service Unavailable
    """

    # the status code
    code = 503
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "The server cannot process the request due to a high load"


class GatewayTimeout(ProtocolError):
    """
    Gateway Timeout
    """

    # the status code
    code = 504
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "The gateway server did not receive a timely response"


class HTTPVersionNotSupported(ProtocolError):
    """
    HTTP Version Not Supported
    """

    # the status code
    code = 505
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "Cannot fulfill request"


class NetworkAuthenticationRequired(ProtocolError):
    """
    Network Authentication Required
    """

    # the status code
    code = 511
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "The client needs to authenticate to gain network access"


class NoResponse(ProtocolError):
    """
    No Response
    """

    # the status code, which is not a standard one: it is the one nginx records in its logs for
    # the same purpose, and it never reaches the client, since nothing does
    code = 444
    # the reason phrase, from my docstring
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    # and what it means
    description = "The server closed the connection without sending a response"
    # the server sends nothing, and closes the connection
    hangup = True


# end of file
