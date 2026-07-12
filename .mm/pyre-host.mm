# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# host is a pure extension: it has no library of its own and depends on nothing external, so it
# builds unconditionally and its bindings ride in the {pyre} package that hosts them
pyre-host.extensions := pyre-host.ext


# the host extension meta-data
pyre-host.ext.root := extensions/host/
# the module stays {host}; it is imported as {pyre.extensions.host}
pyre-host.ext.stem := host
# the module rides in the {pyre} package, alongside {libpyre}
pyre-host.ext.pkg := pyre.pkg
pyre-host.ext.wraps := pyre.lib
pyre-host.ext.capsule :=
pyre-host.ext.extern := journal.lib pybind11 python
pyre-host.ext.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-host.ext.lib.c++.defines += $(pyre.lib.c++.defines)
pyre-host.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically


# end of file
