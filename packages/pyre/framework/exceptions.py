# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2025 all rights reserved
#


class PyreError(Exception):
    """
    Base class for all pyre related errors
    """

    # public data
    description = "generic pyre error"

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
        reason = self.description.format(self)
        # if we have a locator
        if self.locator:
            # give it a chance to pinpoint the error
            return "{.locator}: {}".format(self, reason)
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
