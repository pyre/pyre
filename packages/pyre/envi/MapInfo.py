# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the georeferencing record
class MapInfo:
    """
    The contents of the ENVI {map info} field

    The field ties a reference pixel to map coordinates and gives the pixel size; the first
    seven items are fixed, and what follows depends on the projection: a zone and hemisphere for
    UTM, then the datum, then {key=value} settings such as the units and the rotation.
    """

    # metamethods
    def __init__(
        self,
        projection: str,
        pixel: tuple[float, float],
        coordinates: tuple[float, float],
        size: tuple[float, float],
        extras: list[str] | None = None,
        **kwds,
    ):
        # chain up
        super().__init__(**kwds)
        # the projection name
        self.projection = projection
        # the reference pixel, as 1-based (x, y) image coordinates
        self.pixel = pixel
        # the map coordinates of the reference pixel, as (x, y): easting and northing, or
        # longitude and latitude
        self.coordinates = coordinates
        # the pixel size, as (x, y)
        self.size = size
        # the projection dependent items, as text
        self.extras = list(extras) if extras else []
        # all done
        return

    # interface
    def settings(self) -> dict[str, str]:
        """
        The {key=value} items among my extras
        """
        # split the items that look like settings
        return dict(item.split("=", 1) for item in self.extras if "=" in item)

    def toPixel(self, x: float, y: float) -> tuple[float, float]:
        """
        Convert map coordinates to 0-based (line, sample) image coordinates
        """
        # unpack
        px, py = self.pixel
        x0, y0 = self.coordinates
        dx, dy = self.size
        # the sample grows with x, the line grows against y
        sample = (px - 1) + (x - x0) / dx
        line = (py - 1) + (y0 - y) / dy
        # all done
        return line, sample

    def toMap(self, line: float, sample: float) -> tuple[float, float]:
        """
        Convert 0-based (line, sample) image coordinates to map coordinates
        """
        # unpack
        px, py = self.pixel
        x0, y0 = self.coordinates
        dx, dy = self.size
        # invert {toPixel}
        x = x0 + (sample - (px - 1)) * dx
        y = y0 - (line - (py - 1)) * dy
        # all done
        return x, y

    def render(self) -> str:
        """
        Render me in the form the {map info} field takes
        """
        # the numeric items, rendered the way ENVI writes them
        numbers = [self.number(value) for value in (*self.pixel, *self.coordinates, *self.size)]
        # the projection name first, then the numbers, then the projection dependent items
        items = [self.projection, *numbers, *self.extras]
        # joined with commas
        return ", ".join(items)

    @staticmethod
    def number(value: float) -> str:
        """
        Render {value} with the shortest text that reads back exactly, and without a trailing
        zero when it is integral, which is how ENVI writes reference pixels and integral sizes
        """
        # the shortest round trip form
        text = str(value)
        # drop a trailing zero after the point
        return text[:-2] if text.endswith(".0") else text

    @classmethod
    def parse(cls, text: str) -> "MapInfo":
        """
        Build a record out of the {text} of a {map info} field
        """
        # split the items
        items = [item.strip() for item in text.split(",")]
        # the projection name
        projection = items[0]
        # the reference pixel
        pixel = float(items[1]), float(items[2])
        # its map coordinates
        coordinates = float(items[3]), float(items[4])
        # the pixel size
        size = float(items[5]), float(items[6])
        # whatever follows is projection dependent
        extras = [item for item in items[7:] if item]
        # assemble the record and return it
        return cls(
            projection=projection, pixel=pixel, coordinates=coordinates, size=size, extras=extras
        )

    def __str__(self) -> str:
        # render
        return self.render()


# end of file
