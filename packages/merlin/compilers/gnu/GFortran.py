# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import re
import subprocess
# framework
import merlin


# the FORTRAN compiler from the GNU compiler suite
class GFortran(merlin.component,
          family="merlin.compilers.gnu.gfortran", implements=merlin.protocols.compiler):
    """
    The FORTRAN compiler from the GNU compiler suite
    """


    # constants
    suite = "gcc"
    language = "fortran"


    # configurable state
    driver = merlin.properties.path()
    driver.default = "gfortran"


    # interface
    def version(self):
        """
        Retrieve the compiler version
        """
        # get the driver
        driver = str(self.driver)

        # set up the shell command
        settings = {
            'executable': driver,
            'args': (driver, '--version'),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout

            # the first line is the version
            line = next(stream).strip()
            # extract the fields
            match = self._regex.match(line)
            # if it didn't match
            if not match:
                # oh well...
                return 'unknown', 'unknown', 'unknown'
            # otherwise, extract the version fields
            major = match.group("major")
            minor = match.group("minor")
            micro = match.group("micro")
            # and return it
            return major, minor, micro

        # all done
        return 'unknown', 'unknown', 'unknown'


    # implementation details
    _version = None
    _regex = re.compile(r"GNU Fortran\s+\(.*\)\s+(?P<major>\d+)\.(?P<minor>\d+)\.(?P<micro>\d+)")


# end of file
