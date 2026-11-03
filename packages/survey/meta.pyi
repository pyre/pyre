# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# the build fills in the date of the build
date: str
# the version, as major, minor and micro numbers
major: int
minor: int
micro: int
# and the revision of the source it was built from
revision: str
# all of it together
version: tuple[int, int, int, str]

# the decorations of the help system
copyright: str
banner: str
authors: str
header: str

# end of file
