#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
Build a simple application that has a couple of external requirements that can be satisfied
using just the built-in package support
"""

# externals
import pyre


# the application
class simple(pyre.application, family='simple.app'):
    """
    The simple application
    """

    mpi = pyre.externals.mpi()
    mpi.doc = 'the mpi support'

    python = pyre.externals.python()
    python.doc = 'the python support'

    # obligations
    @pyre.export
    def main(self, *args, **kwds):
        """The main entry point"""
        # show me
        self.info.line("application: {.pyre_spec}".format(self))

        # the host catalog
        self.info.line()
        host = self.pyre_host
        self.info.line("  host: {.pyre_spec}".format(host))
        self.info.line("    nickname: {.nickname}".format(host))
        self.info.line("    hostname: {.hostname}".format(host))
        self.info.line("    distribution: {.distribution}".format(host))
        self.info.line("    available packages:")
        for category in host.externals.keys():
            self.info.line("      {}:".format(category))
            for package in host.externals[category]:
                self.info.line("        {.pyre_spec}".format(package))

        # the user choices
        self.info.line()
        user = self.pyre_user
        self.info.line("  user:")
        self.info.line("    name: {.name}".format(user))
        self.info.line("    email: {.email}".format(user))
        self.info.line("    affiliation: {.affiliation}".format(user))
        self.info.line("    package choices:")
        for category, package in user.externals.items():
            self.info.line("      {}: {.pyre_spec}".format(category, package))

        # my requirements
        self.info.line()
        self.info.line("  requirements: {.requirements}".format(self))
        self.info.line("  dependencies:")
        for category, package in self.dependencies.items():
            self.info.line("      {}: {.pyre_spec}".format(category, package))

        self.info.log()

        # my python
        python = self.python
        self.info.line()
        self.info.line("  python: {.pyre_spec}".format(python))
        self.info.line("    bin: {.bindir}".format(python))
        self.info.line("    inc: {.incdir}".format(python))
        self.info.line("    lib: {.libdir}".format(python))
        self.info.line("    interpreter: {.interpreter}".format(python))

        # my mpi
        mpi = self.mpi
        self.info.line()
        self.info.line("  mpi: {.pyre_spec}".format(mpi))
        self.info.line("    bin: {.bindir}".format(mpi))
        self.info.line("    inc: {.incdir}".format(mpi))
        self.info.line("    lib: {.libdir}".format(mpi))
        self.info.line("    launcher: {.launcher}".format(mpi))

        # all done
        self.info.log()

        # indicate success
        return 0


# the driver
def test():
    # instantiate the app
    app = simple(name="app")
    # and invoke it
    return app.main()


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
