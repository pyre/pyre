# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the georeferencing record
from .MapInfo import MapInfo


# the contents of an ENVI header
class Header(pyre.component, family="pyre.envi.header"):
    """
    The contents of an ENVI header

    The standard keywords are traits, each aliased to its ENVI spelling, so a value read from a
    file is converted to its documented type; keywords the standard does not define land in
    {extras} as text. The keyword list follows the published ENVI header specification.

    Like every component, a named header accepts trait values as constructor keywords, under
    the attribute names or the ENVI spellings, and user configuration under its name overrides
    them; an anonymous header takes values only by assignment.
    """

    # the layout of the product
    description = pyre.properties.str()
    description.default = None
    description.doc = "a string describing the image or the processing performed"

    # the number of samples in a line
    samples = pyre.properties.int()
    samples.default = None
    samples.doc = "the number of samples per image line for each band"

    # the number of lines
    lines = pyre.properties.int()
    lines.default = None
    lines.doc = "the number of lines per image for each band"

    # the number of bands
    bands = pyre.properties.int()
    bands.default = None
    bands.doc = "the number of bands per image file"

    # the size of the header embedded in the file
    headerOffset = pyre.properties.int()
    headerOffset.default = 0
    headerOffset.aliases = {"header offset"}
    headerOffset.doc = "the number of bytes of embedded header information in the file"

    # the ENVI file type
    fileType = pyre.properties.str()
    fileType.default = None
    fileType.aliases = {"file type"}
    fileType.doc = "the ENVI file type"

    # the ENVI code of the type of the data
    dataType = pyre.properties.int()
    dataType.default = None
    dataType.aliases = {"data type"}
    dataType.validators = pyre.constraints.isMember(1, 2, 3, 4, 5, 6, 9, 12, 13, 14, 15)
    dataType.doc = "the ENVI code for the type of data representation"

    # the interleave of the bands
    interleave = pyre.properties.str()
    interleave.default = None
    interleave.validators = pyre.constraints.isMember("bsq", "bil", "bip")
    interleave.doc = "the data interleave; one of bsq, bil, bip"

    # the byte order of numeric data
    byteOrder = pyre.properties.int()
    byteOrder.default = None
    byteOrder.aliases = {"byte order"}
    byteOrder.validators = pyre.constraints.isMember(0, 1)
    byteOrder.doc = "the order of bytes in numeric data; 0 is little endian, 1 is big endian"

    # georeferencing
    mapInfo = pyre.properties.str()
    mapInfo.default = None
    mapInfo.aliases = {"map info"}
    mapInfo.doc = "geographic information; see {map} for the parsed form"

    # custom projection information
    projectionInfo = pyre.properties.str()
    projectionInfo.default = None
    projectionInfo.aliases = {"projection info"}
    projectionInfo.doc = "custom projection information"

    # the coordinate system
    coordinateSystem = pyre.properties.str()
    coordinateSystem.default = None
    coordinateSystem.aliases = {"coordinate system string"}
    coordinateSystem.doc = "the ENVI coordinate system identifier"

    # the geographic corners of a file without map information
    geoPoints = pyre.properties.list(schema=pyre.properties.float())
    geoPoints.default = None
    geoPoints.aliases = {"geo points"}
    geoPoints.doc = "geographic corners for non-georeferenced files"

    # the size of a pixel
    pixelSize = pyre.properties.list(schema=pyre.properties.float())
    pixelSize.default = None
    pixelSize.aliases = {"pixel size"}
    pixelSize.doc = "the x and y pixel size in meters"

    # rational polynomial coefficients
    rpcInfo = pyre.properties.strings()
    rpcInfo.default = None
    rpcInfo.aliases = {"rpc info"}
    rpcInfo.doc = "rational polynomial coefficient geolocation information"

    # the x coordinate of the upper left pixel
    xStart = pyre.properties.float()
    xStart.default = None
    xStart.aliases = {"x start"}
    xStart.doc = "the image x coordinate of the upper left pixel"

    # the y coordinate of the upper left pixel
    yStart = pyre.properties.float()
    yStart.default = None
    yStart.aliases = {"y start"}
    yStart.doc = "the image y coordinate of the upper left pixel"

    # an associated elevation model
    dem = pyre.properties.path()
    dem.default = None
    dem.aliases = {"dem file"}
    dem.doc = "the path to a DEM associated with the image"

    # and the band of it that goes with the image
    demBand = pyre.properties.int()
    demBand.default = None
    demBand.aliases = {"dem band"}
    demBand.doc = "the 1-based index of the DEM band associated with the image"

    # the bands
    bandNames = pyre.properties.strings()
    bandNames.default = None
    bandNames.aliases = {"band names"}
    bandNames.doc = "the names of the image bands"

    # the center wavelength of each band
    wavelength = pyre.properties.list(schema=pyre.properties.float())
    wavelength.default = None
    wavelength.doc = "the center wavelength of each band"

    # and its units
    wavelengthUnits = pyre.properties.str()
    wavelengthUnits.default = None
    wavelengthUnits.aliases = {"wavelength units"}
    wavelengthUnits.doc = "the wavelength units"

    # the full width at half maximum of each band
    fwhm = pyre.properties.list(schema=pyre.properties.float())
    fwhm.default = None
    fwhm.doc = "the full width at half maximum of each band, in the wavelength units"

    # the bands that are bad
    bbl = pyre.properties.list(schema=pyre.properties.int())
    bbl.default = None
    bbl.doc = "the bad band multiplier of each band; 0 is bad, 1 is good"

    # the bands to load automatically
    defaultBands = pyre.properties.list(schema=pyre.properties.int())
    defaultBands.default = None
    defaultBands.aliases = {"default bands"}
    defaultBands.doc = "the 1-based band numbers to load automatically"

    # the gain of each band
    dataGain = pyre.properties.list(schema=pyre.properties.float())
    dataGain.default = None
    dataGain.aliases = {"data gain values"}
    dataGain.doc = "the gain value of each band"

    # the offset of each band
    dataOffset = pyre.properties.list(schema=pyre.properties.float())
    dataOffset.default = None
    dataOffset.aliases = {"data offset values"}
    dataOffset.doc = "the offset value of each band"

    # the reflectance gain of each band
    dataReflectanceGain = pyre.properties.list(schema=pyre.properties.float())
    dataReflectanceGain.default = None
    dataReflectanceGain.aliases = {"data reflectance gain values"}
    dataReflectanceGain.doc = "the reflectance gain value of each band"

    # the reflectance offset of each band
    dataReflectanceOffset = pyre.properties.list(schema=pyre.properties.float())
    dataReflectanceOffset.default = None
    dataReflectanceOffset.aliases = {"data reflectance offset values"}
    dataReflectanceOffset.doc = "the reflectance offset value of each band"

    # the pixel value to ignore
    dataIgnore = pyre.properties.float()
    dataIgnore.default = None
    dataIgnore.aliases = {"data ignore value"}
    dataIgnore.doc = "the pixel value that should be ignored in image processing"

    # the scale of the reflectance
    reflectanceScaleFactor = pyre.properties.float()
    reflectanceScaleFactor.default = None
    reflectanceScaleFactor.aliases = {"reflectance scale factor"}
    reflectanceScaleFactor.doc = "the factor that scales reflectance to the [0,1] range"

    # the solar irradiance of each band
    solarIrradiance = pyre.properties.list(schema=pyre.properties.float())
    solarIrradiance.default = None
    solarIrradiance.aliases = {"solar irradiance"}
    solarIrradiance.doc = "the top of the atmosphere solar irradiance of each band, in W/(m^2 μm)"

    # the names of the spectra in a spectral library
    spectraNames = pyre.properties.strings()
    spectraNames.default = None
    spectraNames.aliases = {"spectra names"}
    spectraNames.doc = "the names of the spectra in a spectral library"

    # the timestamps of the bands of a temporal cube
    timestamp = pyre.properties.strings()
    timestamp.default = None
    timestamp.doc = "the timestamps of the bands of a temporal cube"

    # classification
    classes = pyre.properties.int()
    classes.default = None
    classes.doc = "the number of pixel classes of a classification file"

    # the names of the classes
    classNames = pyre.properties.strings()
    classNames.default = None
    classNames.aliases = {"class names"}
    classNames.doc = "the class names of a classification file"

    # and their colors
    classLookup = pyre.properties.list(schema=pyre.properties.int())
    classLookup.default = None
    classLookup.aliases = {"class lookup"}
    classLookup.doc = "the rgb class colors of a classification file"

    # display
    defaultStretch = pyre.properties.str()
    defaultStretch.default = None
    defaultStretch.aliases = {"default stretch"}
    defaultStretch.doc = "the type of stretch to apply on display"

    # the default color table
    colorTable = pyre.properties.list(schema=pyre.properties.int())
    colorTable.default = None
    colorTable.aliases = {"color table"}
    colorTable.doc = "the default color table; a 3 x 256 array of bytes"

    # the values to extract from a complex image
    complexFunction = pyre.properties.str()
    complexFunction.default = None
    complexFunction.aliases = {"complex function"}
    complexFunction.validators = pyre.constraints.isMember(
        "Real", "Imaginary", "Power", "Magnitude", "Phase"
    )
    complexFunction.doc = "the values to extract from a complex image"

    # the averaging window of Z plots
    zPlotAverage = pyre.properties.int()
    zPlotAverage.default = None
    zPlotAverage.aliases = {"z plot average"}
    zPlotAverage.doc = "the number of pixels in x and y to average for Z plots"

    # the range of Z plots
    zPlotRange = pyre.properties.list(schema=pyre.properties.float())
    zPlotRange.default = None
    zPlotRange.aliases = {"z plot range"}
    zPlotRange.doc = "the default minimum and maximum values for Z plots"

    # and the titles of their axes
    zPlotTitles = pyre.properties.strings()
    zPlotTitles.default = None
    zPlotTitles.aliases = {"z plot titles"}
    zPlotTitles.doc = "the x and y axis titles for Z plots"

    # acquisition
    acquisitionTime = pyre.properties.str()
    acquisitionTime.default = None
    acquisitionTime.aliases = {"acquisition time"}
    acquisitionTime.doc = "the data acquisition time, in ISO 8601 form"

    # the instrument type
    sensorType = pyre.properties.str()
    sensorType.default = None
    sensorType.aliases = {"sensor type"}
    sensorType.doc = "the instrument type"

    # the azimuth of the sun
    sunAzimuth = pyre.properties.float()
    sunAzimuth.default = None
    sunAzimuth.aliases = {"sun azimuth"}
    sunAzimuth.doc = "the angle of the sun, in degrees clockwise from due north"

    # its elevation
    sunElevation = pyre.properties.float()
    sunElevation.default = None
    sunElevation.aliases = {"sun elevation"}
    sunElevation.doc = "the angle of the sun above the horizon, in degrees"

    # the cloud cover
    cloudCover = pyre.properties.float()
    cloudCover.default = None
    cloudCover.aliases = {"cloud cover"}
    cloudCover.doc = "the percentage of cloud cover within the raster"

    # classification information from other formats
    securityTag = pyre.properties.str()
    securityTag.default = None
    securityTag.aliases = {"security tag"}
    securityTag.doc = "classification information inherited from other formats"

    # the spatial and spectral read routines
    readProcedures = pyre.properties.strings()
    readProcedures.default = None
    readProcedures.aliases = {"read procedures"}
    readProcedures.doc = "the names of the spatial and spectral read routines"

    # normalizers
    @pyre.descriptors.normalizer(traits=[interleave])
    def lower(value: str, **kwds) -> str:
        """
        Fold the interleave to lower case, the spelling the validator knows
        """
        # easy enough
        return value.lower()

    # interface
    @property
    def datatype(self) -> str | None:
        """
        The name of the pyre cell type that matches my {dataType} code, in the host's byte order
        """
        # get the code
        code = self.dataType
        # if it hasn't been set
        if code is None:
            # there is nothing to say
            return None
        # the trait accepts only the codes ENVI defines, so the code is in the table
        return self.datatypes[code]

    @property
    def cell(self) -> str | None:
        """
        The name of the pyre cell type that reads my product in place: my {datatype} with the
        byte order marker my {byteOrder} calls for, so a product written on a machine of the
        other endianness comes through the swap
        """
        # get the native name
        name = self.datatype
        # if there is no data type, or the byte order is not known
        if name is None or self.byteOrder is None:
            # there is nothing to add
            return name
        # a single byte scalar has no order
        if name in ("uint8", "int8"):
            # so it needs no marker
            return name
        # ENVI byte order 0 is little endian, 1 is big endian; the grid factories accept either
        # marker and collapse the one that names the host's own order to the native cell
        return name + ("be" if self.byteOrder == 1 else "le")

    @property
    def shape(self) -> tuple[int, ...] | None:
        """
        The shape of the product as laid out in the file: (lines, samples) for a single band,
        and the three axes in interleave order otherwise
        """
        # get the extents: the lines
        lines = self.lines
        # the samples
        samples = self.samples
        # and the bands
        bands = self.bands
        # if the image extents are missing
        if lines is None or samples is None:
            # there is no shape
            return None
        # a single band, declared or implied, is a plane
        if bands is None or bands == 1:
            # of lines and samples
            return lines, samples
        # otherwise the interleave decides where the band axis goes; the ENVI default is bsq
        interleave = self.interleave or "bsq"
        # band sequential: whole planes, one after the other
        if interleave == "bsq":
            # bands are the slowest axis
            return bands, lines, samples
        # band interleaved by line: each line carries all bands
        if interleave == "bil":
            # bands sit between lines and samples
            return lines, bands, samples
        # band interleaved by pixel: each pixel carries all bands
        return lines, samples, bands

    @property
    def offset(self) -> int:
        """
        The number of bytes to skip before the first cell of the product
        """
        # the header offset, with the ENVI default when it is missing
        return self.headerOffset or 0

    def map(self) -> MapInfo | None:
        """
        Parse my {mapInfo} into a georeferencing record
        """
        # get the text
        text = self.mapInfo
        # if there isn't any
        if text is None:
            # there is no georeferencing
            return None
        # otherwise, parse it
        return MapInfo.parse(text=text)

    # metamethods
    def __init__(self, extras: dict | None = None, **kwds):
        # chain up; a named instance may be built with trait values as keywords, under either
        # the attribute names or the ENVI spellings, and the framework deposits them in the
        # configuration store at construction priority before we get here
        super().__init__(**kwds)
        # the keywords the standard does not define, as text: a string for a bare value and a
        # list of strings for a braced one
        self.extras = dict(extras) if extras else {}
        # all done
        return

    # implementation details
    # the ENVI data type codes and the names of the matching pyre cells
    datatypes = {
        1: "uint8",
        2: "int16",
        3: "int32",
        4: "float32",
        5: "float64",
        6: "complex64",
        9: "complex128",
        12: "uint16",
        13: "uint32",
        14: "int64",
        15: "uint64",
    }


# end of file
