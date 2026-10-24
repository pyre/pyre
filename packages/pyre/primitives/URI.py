# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import ipaddress
import re
import typing

# my address (can be | is) a Path
# currently, it's up to the user to use paths for the address field
# it should really be the default, but uris get used by the {framework} in many places and
# it won't be easy to track them all down; p2?
from .Path import Path


# implementation details
class URI:
    # types
    from .exceptions import ParsingError

    # public data
    @property
    def uri(self):
        """
        Assemble a string from my parts
        """
        # make a pile
        parts = filter(
            None,
            [
                # my scheme
                f"{self.scheme}:" if self.scheme else "",
                f"//{self.authority}" if self.authority else "",
                f"{self.address}" if self.address else "",
                f"?{self.query}" if self.query else "",
                f"#{self.fragment}" if self.fragment else "",
            ],
        )
        # assemble and return
        return "".join(parts)

    @property
    def server(self):
        """
        Extract the parts of my {authority}
        """
        # get my authority
        authority = self.authority
        # if it's blank
        if not authority:
            # not much to do
            return (None,) * 4
        # attempt to
        try:
            # split it into its parts
            userinfo, host, port = self._authority(text=authority, value=authority)
        # if it is not a valid authority, which can only happen to a uri that was not parsed
        except self.ParsingError:
            # there is nothing to report
            return (None,) * 4
        # a user information without a colon
        if userinfo is None:
            # names neither a user nor a password
            user, password = None, None
        # otherwise
        else:
            # split it at the first colon
            user, colon, password = userinfo.partition(":")
            # a password is there only after a colon
            password = password if colon else None
        # an empty port is the same as no port at all
        port = port if port else None
        # return the fields
        return host, port, user, password

    # interface
    @classmethod
    def parse(
        cls,
        value,
        scheme: typing.Optional[str] = None,
        authority: typing.Optional[str] = None,
        address: typing.Optional[str | Path] = None,
    ):
        """
        Convert {value} into a {uri}
        """
        # if {value} is already a {uri}
        if isinstance(value, cls):
            # and it has all the parts the defaults would fill in
            if (
                value.scheme is not None
                and value.authority is not None
                and value.address is not None
            ):
                # it is used as it is
                return value
            # otherwise, fill in the missing parts in a copy, so the original is left alone; a
            # default reaches only a part that is missing, since {clone} keeps the parts it is
            # not given
            return value.clone(
                scheme=scheme if value.scheme is None else None,
                authority=authority if value.authority is None else None,
                address=address if value.address is None else None,
            )
        # if {value} is a path
        if isinstance(value, Path):
            # build a {file} uri and return it
            return cls(scheme="file", address=value)
        # otherwise, assume it is a string; control characters belong nowhere in a uri, while
        # blanks are kept, since they are part of the names of the resources users type
        if cls._controls.search(value):
            # so complain
            raise cls.ParsingError(
                value=value, description="{0.value!r} is not a uri: it holds a control character"
            )
        # split it into its parts
        match = cls._uriParser.match(value)
        # which fails only for text that starts with an ampersand, a rule older than RFC 3986
        if not match:
            # so complain
            raise cls.ParsingError(
                value=value, description="{0.value!r} is not a uri: it starts with '&'"
            )
        # extract the parts: the scheme
        thescheme = match.group("scheme")
        # the authority
        theauthority = match.group("authority")
        # the address
        theaddress = match.group("address")
        # the query
        thequery = match.group("query")
        # and the fragment
        thefragment = match.group("fragment")
        # a scheme starts with a letter, followed by letters, digits, plus, minus or dot
        if thescheme is not None and not cls._schemeParser.match(thescheme):
            # anything else is not one
            raise cls.ParsingError(
                value=value,
                description=(
                    "{0.value!r} is not a uri: a scheme starts with a letter, followed by"
                    " letters, digits, '+', '-' or '.'"
                ),
            )
        # an authority
        if theauthority is not None:
            # must split into its parts
            cls._authority(text=theauthority, value=value)
        # without a scheme or an authority, a colon before the first slash would read as a scheme
        if thescheme is None and theauthority is None and ":" in theaddress.partition("/")[0]:
            # so RFC 3986 does not allow one there
            raise cls.ParsingError(
                value=value,
                description=(
                    "{0.value!r} is not a uri: without a scheme, a colon may not come before the"
                    " first slash"
                ),
            )
        # a fragment ends the uri
        if thefragment is not None and "#" in thefragment:
            # so it cannot hold another one
            raise cls.ParsingError(
                value=value, description="{0.value!r} is not a uri: it has more than one fragment"
            )
        # build a uri and return it
        return cls(
            scheme=thescheme if thescheme is not None else scheme,
            authority=theauthority if theauthority is not None else authority,
            address=theaddress if theaddress is not None else address,
            query=thequery,
            fragment=thefragment,
        )

    def clone(
        self,
        scheme: typing.Optional[str] = None,
        authority: typing.Optional[str] = None,
        address: typing.Optional[str] = None,
        query: typing.Optional[str] = None,
        fragment: typing.Optional[str] = None,
    ):
        """
        Make a copy of me with the indicated adjustments
        """
        # that's what my constructor does...
        return type(self)(
            scheme=self.scheme if scheme is None else scheme,
            authority=self.authority if authority is None else authority,
            address=self.address if address is None else address,
            query=self.query if query is None else query,
            fragment=self.fragment if fragment is None else fragment,
        )

    # meta-methods
    def __init__(
        self,
        scheme: typing.Optional[str] = None,
        authority: typing.Optional[str] = None,
        address: typing.Optional[str] = None,
        query: typing.Optional[str] = None,
        fragment: typing.Optional[str] = None,
    ):
        # save my parts
        self.scheme = scheme
        self.authority = authority
        self.address = address
        self.query = query
        self.fragment = fragment
        # all done
        return

    def __add__(self, other):
        """
        Enable concatenations

        N.B.: this is not {join}; it just takes my string representation, adds {other} to the
        end, and attempts to parse the result as a {uri}
        """
        # if {other} is not a string
        if not isinstance(other, str):
            # i don't know what to do, so let python look for another way, or complain
            return NotImplemented
        # otherwise, turn me into a string and add {other}
        new = str(self) + other
        # coerce that into a uri and return it
        return self.parse(new)

    def __truediv__(self, other: Path):
        """
        Clone me and splice {other} to my {address}
        """
        # make a new uri by splicing the path {other} to my address
        return self.clone(address=self.address / other)

    def __itruediv__(self, other: Path):
        """
        Syntactic sugar for assembling paths
        """
        # splice {other} into my address
        self.address /= other
        # and done
        return self

    def __str__(self):
        # easy enough
        return self.uri

    # implementation details
    @classmethod
    def _authority(cls, text, value):
        """
        Split the authority {text} of the uri {value} into its user information, host and port,
        as RFC 3986 spells them; the host of an IP literal comes back without its brackets
        """
        # split the authority
        match = cls._authorityParser.match(text)
        # if it does not split
        if not match:
            # complain
            raise cls.ParsingError(
                value=value,
                description=(
                    "{0.value!r} is not a uri: its authority is not of the form"
                    " [user[:password]@]host[:port], with a numeric port"
                ),
            )
        # get the user information
        userinfo = match.group("userinfo")
        # and the host, which is either an IP literal
        literal = match.group("literal")
        # or a registered name, or an IPv4 address
        host = match.group("host")
        # the user information and a registered name
        for part in (userinfo, host):
            # may not hold the characters RFC 3986 excludes
            if part is not None and cls._excluded.search(part):
                # so complain
                raise cls.ParsingError(
                    value=value,
                    description=(
                        "{0.value!r} is not a uri: its authority holds a blank, a brace, or one"
                        ' of the characters < > " \\ ^ ` | [ ]'
                    ),
                )
        # an IP literal
        if literal is not None:
            # must be an IPv6 address, or a future one
            cls._literal(text=literal, value=value)
            # whose host is the address itself
            host = literal
        # hand back the parts
        return userinfo, host, match.group("port")

    @classmethod
    def _literal(cls, text, value):
        """
        Check that the IP literal {text} of the uri {value} is an IPv6 address, or a future one
        """
        # a future IP literal names its version
        if cls._futureParser.match(text):
            # and is good as it is
            return text
        # a zone is spelled with a percent sign, which RFC 3986 does not allow in a literal
        if "%" not in text:
            # attempt to
            try:
                # interpret the rest as an IPv6 address
                ipaddress.IPv6Address(text)
            # if it is not one
            except ipaddress.AddressValueError:
                # fall through to the complaint
                pass
            # if it is one
            else:
                # it is good
                return text
        # anything else is not an IP literal
        raise cls.ParsingError(
            value=value,
            description=(
                "{0.value!r} is not a uri: the host in brackets is neither an IPv6 address nor a"
                " future IP literal"
            ),
        )

    # the generic split of RFC 3986, appendix B, which every text matches, except the ones pyre
    # refuses because they start with an ampersand
    _uriParser = re.compile(
        # disallow '&' at the beginning of uri, as does the regexlib.com pattern this split came
        # with, presumably so text that continues a query is not mistaken for a uri; RFC 3986
        # allows it, but the rule is kept
        r"^(?=[^&])"
        # grab the scheme
        r"(?:(?P<scheme>[^:/?#]+):)?"
        # the authority
        r"(?://(?P<authority>[^/?#]*))?"
        # the address, typically a path
        r"(?P<address>[^?#]*)"
        # the query, i.e. the ?key=value&... chunks
        r"(?:\?(?P<query>[^#]*))?"
        # and the fragment
        r"(?:#(?P<fragment>.*))?",
        # the address may span lines, so the control check can see them
        re.DOTALL,
    )

    # a scheme: a letter, followed by letters, digits, plus, minus or dot
    _schemeParser = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*$")

    # an authority: user information, a host, and a port, which is a number, or empty
    _authorityParser = re.compile(
        # the user information, which holds no @
        r"^(?:(?P<userinfo>[^@]*)@)?"
        # the host: an IP literal in brackets, or a registered name
        r"(?:\[(?P<literal>[^\]]*)\]|(?P<host>[^:@\[\]]*))"
        # the optional port number
        r"(?::(?P<port>[0-9]*))?$"
    )

    # a future IP literal: a version, and an address of letters, digits and some punctuation
    _futureParser = re.compile(r"^[vV][0-9A-Fa-f]+\.[A-Za-z0-9\-._~!$&'()*+,;=:]+$")

    # the characters RFC 3986 excludes from user information and host names
    _excluded = re.compile(r'[ "<>\\^`{|}\[\]]')

    # control characters, which RFC 3986 excludes from every part of a uri
    _controls = re.compile(r"[\x00-\x1f\x7f]")

    # my parts are all i hold, so i need no dictionary
    __slots__ = ("scheme", "authority", "address", "query", "fragment")


# end of file
