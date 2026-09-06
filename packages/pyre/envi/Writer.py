# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the header
from .Header import Header


# the ENVI header writer
class Writer:
    """
    A writer of ENVI headers

    Traits that have been set are rendered under their ENVI spellings, in declaration order,
    followed by the extras; sequences and text fields go in braces, everything else bare.
    """

    # constants
    # the marker that opens every header
    marker = "ENVI"
    # the string valued keywords ENVI writes in braces
    braced = {"description", "map info", "projection info", "coordinate system string"}

    # interface
    def write(self, header: Header, uri) -> None:
        """
        Write {header} to the file at {uri}
        """
        # the location, as a path
        path = pyre.primitives.path(uri)
        # open the file
        with open(path, mode="w", encoding="utf-8") as stream:
            # and render into it
            stream.write(self.render(header=header))
        # all done
        return

    def render(self, header: Header) -> str:
        """
        Render {header} as the text of an ENVI header file
        """
        # start with the marker
        lines = [self.marker]
        # go through the traits
        for trait in Header.pyre_traits():
            # get the value
            value = getattr(header, trait.name)
            # skip the ones that were never set
            if value is None:
                # by moving on
                continue
            # the ENVI spelling is the alias that isn't the attribute name, when there is one
            keyword = self.keyword(trait=trait)
            # render the entry
            lines.append(f"{keyword} = {self.value(keyword=keyword, value=value)}")
        # then the extras, which carry their own keywords
        for keyword, value in header.extras.items():
            # render the entry
            lines.append(f"{keyword} = {self.value(keyword=keyword, value=value)}")
        # terminate the last line and assemble the text
        return "\n".join(lines) + "\n"

    # implementation details
    def keyword(self, trait) -> str:
        """
        The ENVI spelling of {trait}
        """
        # the aliases other than the attribute name
        spellings = sorted(trait.aliases - {trait.name})
        # the ENVI spelling is the one that's there, or the name itself when there isn't one
        return spellings[0] if spellings else trait.name

    def value(self, keyword: str, value) -> str:
        """
        Render {value} the way ENVI expects it for {keyword}
        """
        # sequences go in braces, comma separated
        if isinstance(value, (list, tuple)):
            # rendered item by item
            return "{" + ", ".join(str(item) for item in value) + "}"
        # text fields go in braces as well
        if keyword in self.braced:
            # as they are
            return "{" + str(value) + "}"
        # everything else is bare
        return str(value)


# end of file
