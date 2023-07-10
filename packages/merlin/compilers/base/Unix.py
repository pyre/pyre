# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import subprocess
import merlin


# basic mechanisms for building the compiler command line
class Unix(merlin.component, implements=merlin.protocols.external.compiler):
    """
    Base compiler in the tradition of the C compiler in Unix
    """

    # configurable state
    driver = merlin.properties.path()
    driver.doc = "the path to the compiler executable"

    # attributes
    @property
    def version(self):
        """
        Retrieve my version
        """
        # get my cached value
        version = self._version
        # if i haven't done this before
        if version is None:
            # retrieve it
            version = self._getVersion()
            # and cache it
            self._version = version
        # all done
        return version

    # flags
    flag_compile = "-c"
    flag_cov = "--coverage"
    flag_dialect = "-std="
    flag_debug = "-g"
    flag_define = "-D"
    flag_dll = "-shared"
    flag_incpath = "-I"
    flag_libpath = "-L"
    flag_library = "-l"
    flag_makedep = "-MD"
    flag_opt = "-O"
    flag_preprocess = "-E"
    flag_pic = "-f"
    flag_prof = "-E"
    flag_version = "--version"
    flag_warn = "-W"
    flag_write = "-o"

    # interface
    def compile(self, driver, source, object, **kwds):
        """
        Generate the command to compile {source} to {object}
        """
        # start with the driver
        yield f"echo {driver}"
        # the baseline command options
        yield from self._baseline()
        # output generation
        yield from self._write(path=object)
        # the source to compiler
        yield from self._compile(source=source)
        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the version cache
        self._version = None
        # all done
        return

    # command line generators
    def _baseline(self):
        """
        Add a collection of flags to the command line unconditionally
        """
        # nothing by default
        return []

    def _compile(self, source):
        """
        Restrict the processing to the compilation phase
        """
        # get the flag
        flag = self.flag_compile
        # add to the command line
        yield f"{flag} {source}"
        # all done
        return

    def _coverage(self):
        """
        Generate coverage information
        """
        # add the correct flag to the command line
        yield self.flag_cov
        # all done
        return

    def _debug(self):
        """
        Generate debugging symbols
        """
        # add the flag
        yield self.flag_debug
        # all done
        return

    def _dialect(self, std):
        """
        Specify the language dialect
        """
        # get the flag
        flag = self.flag_dialect
        # add the dialect specification  to the command line
        yield f"{flag}{std}"
        # all done
        return

    def _define(self, symbols):
        """
        Build a command line fragment to define the given {symbols} for the preprocessor
        """
        # get the flag
        flag = self.flag_define
        # go through the symbols
        for symbol in symbols:
            # prefix each one with the correct flag and make it available
            yield f"{flag}{symbol}"
        # all done
        return

    def _dll(self):
        """
        Build a shared object
        """
        # add the flag
        yield self.flag_dll
        # all done
        return

    def _incpath(self, paths):
        """
        Build a command line fragment to add the given paths to the preprocessor search list
        """
        # get the flag
        flag = self.flag_incpath
        # go through the paths
        for path in paths:
            # prefix each one with the correct flag and make it available
            yield f"{flag}{path}"
        # all done
        return

    def _libpath(self, paths):
        """
        Build a command line fragment to add the given paths to the linker search list
        """
        # get the flag
        flag = self.flag_libpath
        # go through the paths
        for path in paths:
            # prefix each one with the correct flag and make it available
            yield f"{flag}{path}"
        # all done
        return

    def _libraries(self, paths):
        """
        Link against the libraries in {paths}
        """
        # get the flag
        flag = self.flag_library
        # go through the path
        for path in paths:
            # prefix each one with the correct flag and make it available
            yield f"{flag}{path}"
        # all done
        return

    def _makedep(self):
        """
        Generate a dependency tree for the current translation unit
        """
        # add the correct flag to the command line
        yield self.flag_makedep
        # all done
        return

    def _opt(self, level=3):
        """
        Control the optimizationlevel
        """
        # get the flag
        flag = self.flag_opt
        # form the optimization level
        yield f"{flag}{level}"
        # all done
        return

    def _pic(self, model="PIC"):
        """
        Generate position independent code, suitable for inclusion in  a shared library
        """
        # get the flag
        flag = self.flag_pic
        # add the command line argument
        yield f"{flag}{model}"
        # all done
        return

    def _preprocess(self):
        """
        Restrict the processing to the preprocessing phase
        """
        # add the correct flag to the command line
        yield self.flag_preprocess
        # all done
        return

    def _prof(self):
        """
        Generate profiling information
        """
        # add the correct flag to the command line
        yield self.flag_prof
        # all done
        return

    def _sources(self, paths):
        """
        Add the {paths} to the list of sources to compile
        """
        # no transformation needed, by default
        yield from paths
        # all done
        return

    def _warn(self, diagnostics=None):
        """
        Control the generation of warnings; the default is to complain about everything
        """
        # get the flag
        flag = self.flag_warn
        # if the user didn't restrict the list
        if diagnostics is None:
            # complain about everything
            yield f"{flag}all"
            # and done
            return
        # otherwise, go through them
        for diagnostic in diagnostics:
            # and add each one to the command line
            yield f"{flag}{diagnostic}"
        # all done
        return

    def _write(self, path):
        """
        Place the output in {path}
        """
        # get the flag
        flag = self.flag_write
        # add to the command line
        yield f"{flag} {path}"
        # all done
        return

    # helpers
    def _getVersion(self):
        """
        Retrieve the compiler version
        """
        # get the driver
        driver = str(self.driver)
        # and the recognizer
        regex = self._version_regex
        # set up the shell command
        settings = {
            "executable": driver,
            "args": (driver, self.flag_version),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # the first line is the version
            line = next(stream).strip()
            # extract the fields
            match = regex.match(line)
            # if we got a match
            if match:
                # extract the version fields
                major = match.group("major")
                minor = match.group("minor")
                micro = match.group("micro")
                # assemble the version tuple and return it
                return major, minor, micro
        # otherwise, report failure with the correct structure
        return "unknown", "unknown", "unknown"

    # the version regex
    _version_regex = []


# end of file
