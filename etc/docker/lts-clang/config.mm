# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# with {pkgdb: dpkg} every external dependency is discovered
# from the installed ubuntu packages; leave this file as the place for any local overrides


# pyre: the libraries of the installed pyre that its clients link against
pyre.libraries := pyre-h5 pyre journal


# end of file
