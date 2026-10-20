# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import re
import string


class PyreError(Exception):
    """
    Base class for all pyre related errors
    """

    # public data
    description = "generic pyre error"

    # the parser of the format fields of descriptions
    pyre_formatter = string.Formatter()

    # interface
    def pyre_render(self, *, template: str) -> str:
        """
        Render {template}, a description of mine, by resolving the fields that refer to me;
        everything else, e.g. the braces of text that was never meant to be a template, is left
        as it was written
        """
        # attempt to
        try:
            # split the template into literal text and fields
            pieces = list(self.pyre_formatter.parse(template))
        # if it is not even well formed, e.g. it has a lone closing brace
        except ValueError:
            # it is text, so leave it alone
            return template
        # the fragments of the rendering
        fragments = []
        # go through the pieces
        for literal, name, spec, conversion in pieces:
            # add the literal text
            fragments.append(literal)
            # a piece with no field
            if name is None:
                # contributes nothing more
                continue
            # resolve the field and add it
            fragments.append(self.pyre_field(name=name, spec=spec, conversion=conversion))
        # assemble the rendering
        return "".join(fragments)

    def pyre_field(self, *, name: str, spec: str, conversion: str | None) -> str:
        """
        Resolve the field {name} of a description of mine, or spell it as it was written, when it
        does not refer to me, or does not resolve
        """
        # the conversion and the format specification, as they were written
        suffix = (f"!{conversion}" if conversion else "") + (f":{spec}" if spec else "")
        # and the whole field
        written = "{" + name + suffix + "}"
        # the position the field names, which is everything before its first attribute or item
        base = re.split(r"[.\[]", name, maxsplit=1)[0]
        # and the path from there to the value
        path = name[len(base) :]
        # fields that name anything else
        if base not in ("", "0"):
            # are text
            return written
        # i am not a field of my own description, since i would render it again, unless asked
        # for my representation
        if not path and conversion != "r":
            # so i am text too
            return written
        # attempt to
        try:
            # look the field up, with an explicit position
            value, _ = self.pyre_formatter.get_field("0" + path, (self,), {})
            # convert it
            value = self.pyre_formatter.convert_field(value, conversion)
            # resolve the fields of its format specification
            spec = self.pyre_render(template=spec) if spec else ""
            # and format it
            return self.pyre_formatter.format_field(value, spec)
        # if the field leads nowhere, or its value can't be formatted the way it asks
        except (AttributeError, IndexError, KeyError, TypeError, ValueError):
            # spell it as it was written
            return written

    # meta-methods
    def __init__(self, description=None, locator=None, error=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # attach the locator
        self.locator = locator
        # and the actual error
        self.error = error
        # if this particular invocation overrides the default description
        if description is not None:
            # record it
            self.description = description
        # all done
        return

    def __str__(self):
        # render the error message
        reason = self.pyre_render(template=self.description)
        # if we have a locator
        if self.locator:
            # give it a chance to pinpoint the error
            return f"{self.locator}: {reason}"
        # otherwise
        return reason

    def _pyre_report(self):
        """
        Generate a more verbose report regarding this error
        """
        # first, generate the textual representation of the error
        yield str(self)
        # if there is a locator
        if self.locator:
            # add its contents to the report
            yield str(self.locator)
        # if an underlying error is what brought this about
        if self.error is not None:
            # pass along its reason
            yield f"reason: {self.error}"
        # all done
        return


class FrameworkError(PyreError):
    """
    Base class for all framework exceptions

    Useful when you are trying to catch any and all pyre framework errors
    """


class BadResourceLocatorError(FrameworkError):
    """
    Exception raised when a URI is not formed properly
    """

    # public data
    description = "{0.uri}: {0.reason}"

    # meta-methods
    def __init__(self, uri, reason, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the error info
        self.uri = uri
        self.reason = reason
        # all done
        return


class ComponentNotFoundError(FrameworkError):

    # public data
    description = "could not resolve {0.uri} into a component"

    # public data
    def __init__(self, uri, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the error info
        self.uri = uri
        # all done
        return


class ExternalNotFoundError(FrameworkError):
    """
    Base class for parsing errors
    """

    # public data
    description = "could not locate support for external package {0.category!r}"

    # meta-methods
    def __init__(self, category, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the error info
        self.category = category
        # all done
        return


# end of file
