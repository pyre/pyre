# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# exceptions
from .exceptions import ProtocolError


# specific responses
class Continue(ProtocolError):
    """
    Continue
    """
    # state
    code = 100
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Request received, please continue"


class SwitchingProtocols(ProtocolError):
    """
    Switching Protocols
    """
    # state
    code = 101
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Switching to new protocol; obey Upgrade header"


class Created(ProtocolError):
    """
    Created
    """
    # state
    code = 201
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Document created, URL follows"


class Accepted(ProtocolError):
    """
    Accepted
    """
    # state
    code = 202
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Request accepted, processing continues off-line"


class NonAuthoritativeInformation(ProtocolError):
    """
    Non-Authoritative Information
    """
    # state
    code = 203
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Request fulfilled from cache"


class NoContent(ProtocolError):
    """
    No Content
    """
    # state
    code = 204
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Request fulfilled, nothing follows"


class ResetContent(ProtocolError):
    """
    Reset Content
    """
    # state
    code = 205
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Clear input form for further input"



class PartialContent(ProtocolError):
    """
    Partial Content
    """
    # state
    code = 206
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Partial content follows"


class MultipleChoices(ProtocolError):
    """
    Multiple Choices
    """
    # state
    code = 300
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Object has several resources -- see URI list"


class MovedPermanently(ProtocolError):
    """
    Moved Permanently
    """
    # state
    code = 301
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Object moved permanently -- see URI list"


class Found(ProtocolError):
    """
    Found
    """
    # state
    code = 302
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Object moved temporarily -- see URI list"


class SeeOther(ProtocolError):
    """
    See Other
    """
    # state
    code = 303
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Object moved -- see Method and URL list"


class NotModified(ProtocolError):
    """
    Not Modified
    """
    # state
    code = 304
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Document has not changed since given time"


class UseProxy(ProtocolError):
    """
    Use Proxy
    """
    # state
    code = 305
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "You must use proxy specified in Location to access this resource"


class TemporaryRedirect(ProtocolError):
    """
    Temporary Redirect
    """
    # state
    code = 307
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Object moved temporarily -- see URI list"


class BadRequestSyntax(ProtocolError):
    """
    Bad Request
    """
    # state
    code = 400
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Bad request syntax or unsupported method"


class Unauthorized(ProtocolError):
    """
    Unauthorized
    """
    # state
    code = 401
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "No permission -- see authorization schemes"


class PaymentRequired(ProtocolError):
    """
    Payment Required
    """
    # state
    code = 402
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "No payment -- see charging schemes"


class Forbidden(ProtocolError):
    """
    Forbidden
    """
    # state
    code = 403
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Request forbidden -- authorization will not help"


class NotFound(ProtocolError):
    """
    Not Found
    """
    # state
    code = 404
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Nothing matches the given URI"


class MethodNotAllowed(ProtocolError):
    """
    Method Not Allowed
    """
    # state
    code = 405
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Specified method is invalid for this resource"


class NotAcceptable(ProtocolError):
    """
    Not Acceptable
    """
    # state
    code = 406
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "URI not available in preferred format"


class ProxyAuthenticationRequired(ProtocolError):
    """
    Proxy Authentication Required
    """
    # state
    code = 407
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "You must authenticate with this proxy before proceeding"


class RequestTimeout(ProtocolError):
    """
    Request Timeout
    """
    # state
    code = 408
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Request timed out; try again later"


class Conflict(ProtocolError):
    """
    Conflict
    """
    # state
    code = 409
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Request conflict"


class Gone(ProtocolError):
    """
    Gone
    """
    # state
    code = 410
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "URI no longer exists and has been permanently removed"


class LengthRequired(ProtocolError):
    """
    Length Required
    """
    # state
    code = 411
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Client must specify Content-Length"


class PreconditionFailed(ProtocolError):
    """
    Precondition Failed
    """
    # state
    code = 412
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Precondition in headers is false"


class RequestEntityTooLarge(ProtocolError):
    """
    Request Entity Too Large
    """
    # state
    code = 413
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Entity is too large"


class RequestURITooLong(ProtocolError):
    """
    Request-URI Too Long
    """
    # state
    code = 414
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "URI is too long"


class UnsupportedMediaType(ProtocolError):
    """
    Unsupported Media Type
    """
    # state
    code = 415
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Entity body in unsupported format"


class RequestedRangeNotSatisfiable(ProtocolError):
    """
    Requested Range Not Satisfiable
    """
    # state
    code = 416
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Cannot satisfy request range"


class ExpectationFailed(ProtocolError):
    """
    Expectation Failed
    """
    # state
    code = 417
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Expect condition could not be satisfied"


class PreconditionRequired(ProtocolError):
    """
    Precondition Required
    """
    # state
    code = 428
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "The origin server requires the request to be conditional"


class TooManyRequests(ProtocolError):
    """
    Too Many Requests
    """
    # state
    code = 429
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "The user has sent too many requests in a given amount of time (rate limiting)"


class RequestHeaderFieldsTooLarge(ProtocolError):
    """
    Request Header Fields Too Large
    """
    # state
    code = 431
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = ("The server is unwilling to process the request because its header fields "
                  "are too large")


class InternalServerError(ProtocolError):
    """
    Internal Server Error
    """
    # state
    code = 500
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Server got itself in trouble"


class NotImplemented(ProtocolError):
    """
    Not Implemented
    """
    # state
    code = 501
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Server does not support this operation"


class BadGateway(ProtocolError):
    """
    Bad Gateway
    """
    # state
    code = 502
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Invalid responses from another server/proxy"


class ServiceUnavailable(ProtocolError):
    """
    Service Unavailable
    """
    # state
    code = 503
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "The server cannot process the request due to a high load"


class GatewayTimeout(ProtocolError):
    """
    Gateway Timeout
    """
    # state
    code = 504
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "The gateway server did not receive a timely response"


class HTTPVersionNotSupported(ProtocolError):
    """
    HTTP Version Not Supported
    """
    # state
    code = 505
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "Cannot fulfill request"


class NetworkAuthenticationRequired(ProtocolError):
    """
    Network Authentication Required
    """
    # state
    code = 511
    status = " ".join(filter(None, (line.strip() for line in __doc__.splitlines())))
    description = "The client needs to authenticate to gain network access"


# end of file
