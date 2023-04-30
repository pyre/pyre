# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# the manager of intermediate and final build products
class FHS(merlin.component, family="merlin.layouts.fhs", implements=merlin.protocols.prefix):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # required state
    bin = merlin.properties.path()
    bin.default = "bin"
    bin.doc = "the location of executables"

    config = merlin.properties.path()
    config.default = "etc/config"
    config.doc = "global package configuration files"

    doc = merlin.properties.path()
    doc.default = "doc"
    doc.doc = "package documentation"

    etc = merlin.properties.path()
    etc.default = "etc"
    etc.doc = "host specific files"

    include = merlin.properties.path()
    include.default = "include"
    include.doc = "library header files"

    lib = merlin.properties.path()
    lib.default = "lib"
    lib.doc = "libraries"

    libexec = merlin.properties.path()
    libexec.default = "libexec"
    libexec.doc = "binaries that are meant to be used by other packages"

    share = merlin.properties.path()
    share.default = "share"
    share.doc = "architecture independent package files"

    var = merlin.properties.path()
    var.default = "var"
    var.doc = "runtime files"


# end of file
