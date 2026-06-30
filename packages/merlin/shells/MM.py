# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# externals
import json
import os
import re
import shutil
import subprocess
import sys

# support
import pyre
import merlin
import journal


# the app
class MM(pyre.application, family="pyre.applications.mm", namespace="mm"):
    """
    An opinionated build framework based on GNU make

    Michael Aïvázis <michael.aivazis@para-sim.com>
    copyright 1998-2026 all rights reserved
    """

    # project configuration
    version = pyre.properties.str()
    version.default = None
    version.doc = "the project version; try to deduce it, if not set"

    # compute branch-keyed build paths and print shell export statements
    mode = pyre.properties.str()
    mode.default = "dev"
    mode.validators = pyre.constraints.isMember(
        "dev", "release", "conda", "macports", "ubuntu"
    )
    mode.doc = "the strategy for generating locations for the build products"

    branch = pyre.properties.bool()
    branch.default = None
    branch.doc = "derive the {tag} from repository state (False clears it; None leaves it unchanged)"

    activate = pyre.properties.bool()
    activate.default = False
    activate.doc = "print shell commands that add the build's bin and python packages to the session"

    syntax = pyre.properties.str()
    syntax.default = "sh"
    syntax.validators = pyre.constraints.isMember("sh", "csh", "fish")
    syntax.doc = "the shell syntax to use when printing export statements"

    tag = pyre.properties.str()
    tag.default = os.environ.get("mm_tag")
    tag.doc = "an optional discriminator appended to {bldroot} and {prefix} to separate build contexts"

    prefix = pyre.properties.path()
    prefix.default = None
    prefix.doc = "the path to the installation directory"

    bldroot = pyre.properties.path()
    bldroot.default = None
    bldroot.doc = "the path to the intermediate build products"

    toolchains = pyre.properties.path()
    toolchains.default = None
    toolchains.doc = (
        "the directory where environment-level developer toolchains are installed"
    )

    target = pyre.properties.strings()
    target.default = ["debug", "shared"]
    target.doc = "the list of target variants to build"

    compilers = pyre.properties.strings()
    compilers.default = ["clang", "python/python3"]
    compilers.doc = "the set of compilers to use"

    local = pyre.properties.str()
    local.default = None
    local.doc = "the name of a optional local makefile with additional targets"

    pkgdb = pyre.properties.str()
    pkgdb.default = "adhoc"
    pkgdb.validators = pyre.constraints.isMember("adhoc", "conda", "macports", "dpkg")
    pkgdb.doc = (
        "use one of the supported package managers for resolving external dependencies"
    )

    # mm behavior
    setup = pyre.properties.bool()
    setup.default = False
    setup.doc = "build a package database, instead of invoking make"

    serial = pyre.properties.bool()
    serial.default = False
    serial.doc = "control whether to run make in parallel"

    slots = pyre.properties.int()
    slots.default = None
    slots.aliases |= {"j", "jobs"}
    slots.doc = "the number of recipes to execute simultaneously; defaults to all cores"

    show = pyre.properties.bool()
    show.default = False
    show.doc = "display details about the invocation of make"

    dry = pyre.properties.bool()
    dry.default = False
    dry.aliases |= {"n"}
    dry.doc = "do everything except invoke make"

    quiet = pyre.properties.bool()
    quiet.default = False
    quiet.aliases |= {"q"}
    quiet.doc = "suppress all non-critical output"

    color = pyre.properties.bool()
    color.default = True
    color.doc = "colorize screen output on supported terminals"

    palette = pyre.properties.str()
    palette.default = "builtin"
    palette.doc = "color palette for colorizing screen output on supported terminals"

    # make behavior
    ignore = pyre.properties.bool()
    ignore.default = False
    ignore.aliases |= {"k"}
    ignore.doc = "ask make to ignore build target failures and keep going"

    verbose = pyre.properties.bool()
    verbose.default = False
    verbose.aliases |= {"v"}
    verbose.doc = "ask make to show each action taken"

    rules = pyre.properties.bool()
    rules.default = False
    rules.doc = "ask make to print the rule database"

    trace = pyre.properties.bool()
    trace.default = False
    trace.doc = "ask make to print trace information"

    # the name of the GNU make executable
    make = pyre.properties.path(default=os.environ.get("GNU_MAKE", "gmake"))
    make.default = os.environ.get(
        "GNU_MAKE", "gmake" if pyre.executive.host.platform == "darwin" else "make"
    )
    make.doc = "the name of the GNU make executable"

    # environment
    host = pyre.platforms.platform()
    host.doc = "information about the current host"

    environment = pyre.properties.str()
    environment.default = os.environ.get("CONDA_DEFAULT_ENV", "")
    environment.doc = "the name of the conda environment"

    # the name of the directory with project and user makefile fragments
    cfgdir = pyre.properties.path()
    cfgdir.default = ".mm"
    cfgdir.doc = "the relative path to project and user makefile fragments"

    # the layout out of the installation area
    binPrefix = pyre.properties.path()
    binPrefix.default = "bin"
    binPrefix.aliases |= {"bin-prefix"}
    binPrefix.doc = "installation location for executables"

    libPrefix = pyre.properties.path()
    libPrefix.default = "lib"
    libPrefix.aliases |= {"lib-prefix"}
    libPrefix.doc = "installation location for libraries and shared objects"

    incPrefix = pyre.properties.path()
    incPrefix.default = "include"
    incPrefix.aliases |= {"include-prefix"}
    incPrefix.doc = "installation location for header files"

    pycPrefix = pyre.properties.path()
    pycPrefix.default = "packages"
    pycPrefix.aliases |= {"python-prefix"}
    pycPrefix.doc = "installation location for python packages"

    docPrefix = pyre.properties.path()
    docPrefix.default = "doc"
    docPrefix.aliases |= {"doc-prefix"}
    docPrefix.doc = "installation location for documentation files"

    etcPrefix = pyre.properties.path()
    etcPrefix.default = "etc"
    etcPrefix.aliases |= {"etc-prefix"}
    etcPrefix.doc = "installation location for system auxiliary files"

    sharePrefix = pyre.properties.path()
    sharePrefix.default = "share"
    sharePrefix.aliases |= {"share-prefix"}
    sharePrefix.doc = "installation location for platform independent files"

    varPrefix = pyre.properties.path()
    varPrefix.default = "var"
    varPrefix.aliases |= {"var-prefix"}
    varPrefix.doc = "installation location for runtime files"

    # my internal layout; users should probably stay away from these
    makefile = pyre.properties.path()
    makefile.default = "merlin.mm"
    makefile.doc = "the name of the top level internal makefile; caveat emptor"

    engine = pyre.properties.path()
    engine.doc = "the path to the built-in make engine; caveat emptor"

    portinfo = pyre.properties.path()
    portinfo.doc = "the directory with the built-in portinfo headers; caveat emptor"

    runcfg = pyre.properties.paths()
    runcfg.doc = "a list of paths to add to the make include path; caveat emptor"

    # important environment variables
    PATH = pyre.properties.envpath(variable="PATH")
    PYTHONPATH = pyre.properties.envpath(variable="PYTHONPATH")

    # compiler search paths
    incpath = pyre.properties.paths()
    incpath.doc = "a list of paths to search for headers"

    libpath = pyre.properties.paths()
    libpath.doc = "a list of paths to search for libraries"

    # the main entry point
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # if we are just setting up the package database
        if self.setup:
            # build the package database
            return self.buildPackageDatabase()
        # if we are setting or clearing the branch context
        if self.branch is not None:
            # generate the {eval} script
            return self.establishBranchContext()
        # if we are activating the build in the current session
        if self.activate:
            # generate the {eval} script
            return self.activateSession()
        # otherwise, launch the build
        return self.launch()

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # N.B.:
        #   the {explore} step could happen here
        #   there were some corner cases that were raising exceptions
        #   investigate and rethink
        # get the current user
        self.user = self.pyre_executive.user
        # and the version
        self._version = "{}.{}.{} rev {}".format(*merlin.meta.version)
        # prime the make executable
        self._builder = None
        # my top level makefile
        self._makefile = None
        # the user configuration directory
        self._userCfg = None
        # the project root
        self._root = None
        # the project configuration directory
        self._projectCfg = None
        # the path to the optional makefile with additional configuration and targets
        self._localMakefile = None
        # the name of the compiler suite used to compile C/C++ code, and hence is responsible
        # for setting the runtime ABI
        self._suite = None
        # the path to the intermediate products of the build
        self._bldroot = None
        # the target identification
        self._bldTarget = None
        self._bldVariants = None
        self._bldTag = None
        # and the install directory
        self._prefix = None
        # the directory with the environment-level developer toolchains
        self._toolchains = None
        # the python package installation directory; may be overridden by mode-specific logic
        self._pycPrefix = None
        # the syntax dispatch table: maps shell names to (var, value) -> export/unset statement
        # {value} of None means unset the variable rather than export it; every statement is
        # terminated with a ';' so the lines survive being flattened onto one line — an unquoted
        # 'eval $(mm --activate)' collapses the newlines, and without the terminator one statement
        # runs into the next (zsh errors outright, bash silently mis-parses)
        self._syntaxDispatch = {
            "sh": lambda var, value: (
                f"unset {var};" if value is None else f'export {var}="{value}";'
            ),
            "csh": lambda var, value: (
                f"unsetenv {var};" if value is None else f'setenv {var} "{value}";'
            ),
            "fish": lambda var, value: (
                f"set -e {var};" if value is None else f'set -x {var} "{value}";'
            ),
        }
        # the mode dispatch tables
        self._bldrootDispatch = {
            "dev": self._devBldroot,
            "release": self._releaseBldroot,
            "conda": self._condaBldroot,
            "macports": self._macportsBldroot,
            "ubuntu": self._ubuntuBldroot,
        }
        self._prefixDispatch = {
            "dev": self._devPrefix,
            "release": self._releasePrefix,
            "conda": self._condaPrefix,
            "macports": self._macportsPrefix,
            "ubuntu": self._ubuntuPrefix,
        }
        # the pkgdb dispatch table
        self._pkgdbDispatch = {
            "adhoc": self._buildAdhocPackageDatabase,
            "conda": self._buildCondaPackageDatabase,
            "macports": self._buildMacportsPackageDatabase,
            "dpkg": self._buildDpkgPackageDatabase,
        }
        # verify both mode dispatch tables are in sync with the mode validator; scan for the
        # first validator that carries a {choices} attribute (see pyre/pyre#176 for a better API)
        for modeValidator in filter(
            lambda v: hasattr(v, "choices"), self.pyre_trait("mode").validators
        ):
            # check both tables
            for name, table in [
                ("bldroot", self._bldrootDispatch),
                ("prefix", self._prefixDispatch),
            ]:
                # if the keys don't match the validator choices, something is wrong
                if set(table) != modeValidator.choices:
                    # make a channel
                    channel = journal.firewall("mm.mode")
                    # report
                    channel.line(
                        f"{name} dispatch table is out of sync with the mode validator"
                    )
                    # indent
                    channel.indent()
                    # details:
                    channel.line(f"dispatch keys: {set(table)}")
                    channel.log(f"validator choices: {modeValidator.choices}")
                    # outdent
                    channel.outdent()
                    # flush
                    channel.log()
            # we only care about the first match
            break
        # verify the pkgdb dispatch table is in sync with the pkgdb validator
        for pkgdbValidator in filter(
            lambda v: hasattr(v, "choices"), self.pyre_trait("pkgdb").validators
        ):
            # if the keys don't match the validator choices, something is wrong
            if set(self._pkgdbDispatch) != pkgdbValidator.choices:
                # make a channel
                channel = journal.firewall("mm.pkgdb")
                # report
                channel.line(
                    "pkgdb dispatch table is out of sync with the pkgdb validator"
                )
                channel.indent()
                channel.line(f"dispatch keys:     {set(self._pkgdbDispatch)}")
                channel.log(f"validator choices: {pkgdbValidator.choices}")
                channel.outdent()
                channel.log()
            # we only care about the first match
            break
        # verify the syntax dispatch table is in sync with the syntax validator
        for syntaxValidator in filter(
            lambda v: hasattr(v, "choices"), self.pyre_trait("syntax").validators
        ):
            # if the keys don't match the validator choices, something is wrong
            if set(self._syntaxDispatch) != syntaxValidator.choices:
                # make a channel
                channel = journal.firewall("mm.syntax")
                # report
                channel.line(
                    "syntax dispatch table is out of sync with the syntax validator"
                )
                channel.indent()
                channel.line(f"dispatch keys:     {set(self._syntaxDispatch)}")
                channel.log(f"validator choices: {syntaxValidator.choices}")
                channel.outdent()
                channel.log()
            # we only care about the first match
            break
        # all done
        return

    # implementation details
    def launch(self):
        """
        Launch GNU make
        """
        # explore
        self.explore()
        # if the user has asked to see the recipe execution details
        if self.verbose:
            # fall back to serial mode so the output is not garbled
            self.serial = True
        # build the make command line
        argv = list(self.assembleMakeCommandLine())
        # if the user asked to see the make command line
        if self.show:
            # make a channel
            channel = journal.help("mm.make")
            # show
            channel.line(argv[0])
            channel.indent()
            channel.report(report=argv[1:])
            channel.outdent()
            # flush
            channel.log()
        # if this is a dry run
        if self.dry:
            # do not go any further
            return 0
        # go to the right place
        os.chdir(self._anchor)
        # build the environment updates
        env = {
            "PATH": os.pathsep.join(map(str, self.PATH)),
            "PYTHONPATH": os.pathsep.join(map(str, self.PYTHONPATH)),
        }
        # apply them
        os.environ.update(env)
        # assemble the subprocess options
        settings = {
            "executable": str(self.make),
            "args": argv,
            "universal_newlines": True,
            "shell": False,
        }
        # invoke GNU make; we already know {self.make} is good, since we verified its version.
        # any other modes of failure?
        with subprocess.Popen(**settings) as make:
            # wait for it to finish and harvest its exit code
            status = make.wait()
        # and share it with the shell
        return status

    def buildPackageDatabase(self):
        """
        Build an external package database for the engine
        """
        # explore the project layout so {locateBuildRoot} can find the project root
        self.explore()
        # get the temporary staging area; already incorporates the build variant tag
        stage = self.locateBuildRoot()
        # ensure the staging directory exists on a fresh checkout
        stage.mkdir(parents=True, exist_ok=True)
        # the location of the package database
        db = stage / f"pkg-{self.pkgdb}.db"
        # dispatch to the mode-specific implementation
        return self._pkgdbDispatch[self.pkgdb](db)

    def establishBranchContext(self):
        """
        Set or clear the branch-keyed tag and activate the corresponding session
        """
        # if branch is True, derive a tag from the repository state
        if self.branch:
            # find the project root to get the project name
            root = self.locateProjectRoot()
            # get te branch name
            branch = self.gitCurrentBranch()
            # the tag is the relative path that discriminates this build context; it is
            # appended to {bldroot} and {prefix} by {locateBuildRoot} and {locatePrefix}
            self.tag = f"{root.name}/{branch}"
        # if branch is False, clear the tag so the tag-less paths are used
        else:
            self.tag = None
        # let {activateSession} emit the full shell context, including the updated {mm_tag}
        return self.activateSession()

    def activateSession(self):
        """
        Print shell commands that establish the build context in the current session
        """
        # resolve all paths
        self.explore()
        # the new installation prefix and python package directory
        newPrefix = self._prefix
        newPyc = newPrefix / (self._pycPrefix or self.pycPrefix)
        # if a previous activation is recorded in the environment, remove its contributions
        # from the path variables before injecting the new ones
        oldPrefixStr = os.environ.get("mm_prefix")
        oldPycStr = os.environ.get("mm_pyc")
        if oldPrefixStr:
            self.PATH = self.eject(
                var=self.PATH, path=(pyre.primitives.path(oldPrefixStr) / "bin")
            )
        if oldPycStr:
            self.PYTHONPATH = self.eject(
                var=self.PYTHONPATH, path=pyre.primitives.path(oldPycStr)
            )
        # build the updated PATH and PYTHONPATH with the new entries at the front
        path = os.pathsep.join(
            str(p) for p in self.inject(var=self.PATH, path=(newPrefix / "bin"))
        )
        pythonpath = os.pathsep.join(
            str(p) for p in self.inject(var=self.PYTHONPATH, path=newPyc)
        )
        # emit the full shell context
        emit = self._syntaxDispatch[self.syntax]
        # the tag: None triggers an unset rather than an export
        print(emit("mm_tag", self.tag or None))
        # the prefix and python package path, so the next activation can undo this one
        print(emit("mm_prefix", str(newPrefix)))
        print(emit("mm_pyc", str(newPyc)))
        # the updated path variables
        print(emit("PATH", path))
        print(emit("PYTHONPATH", pythonpath))
        # all done
        return 0

    def explore(self):
        """
        Gather the locations of all important directories and files
        """
        # verify we have the correct make
        self._builder = self.verifyGNUMake()
        # verify my installation
        self._makefile = self.verifyInstallation()
        # get the user configuration directory
        self._userCfg = self.locateUserConfig()
        # find the project root
        self._root = self.locateProjectRoot()
        # and the project configuration directory
        self._projectCfg = self.locateProjectConfig()
        # load the project specific configuration files
        self.loadProjectConfig()
        # locate the local makefile
        self._localMakefile = self.locateLocalMakefile()
        # mark the location from which mm was invoked
        self._origin = pyre.primitives.path.cwd()
        # mark the path that will become the {cwd} for make
        self._anchor = self._localMakefile.parent if self._localMakefile else self._root
        # determine the compiler suite
        self._suite = self.deduceCompilerSuite()
        # construct the build tag; must precede {locateBuildRoot} since it needs {_bldTag}
        self._bldTarget, self._bldVariants, self._bldTag = self.assembleBuildTarget()
        # figure out where to put the intermediate products of the build
        self._bldroot = self.locateBuildRoot()
        # figure out the install directory
        self._prefix = self.locatePrefix()
        # figure out where the environment-level developer toolchains live
        self._toolchains = self.locateToolchains()
        # adjust my environment variables with the build configuration
        self.updateEnvironmentVariables()
        # all done
        return

    def assembleMakeCommandLine(self):
        """
        Put together the GNU make command line
        """
        # start with the flags that control the behavior of make
        yield from self.configureMake()
        # add the project configuration
        yield from self.configureProject()
        # the product version
        yield from self.configureVersion()
        # the build target
        yield from self.configureTarget()
        # information about the user that invoked mm
        yield from self.describeUser()
        # information about the host mm is running on
        yield from self.describeHost()
        # configure the engine
        yield from self.configureBuilder()
        # finally, whatever else the user put on the command line
        yield from self.argv
        # all done
        return

    def verifyInstallation(self):
        """
        Ensure that this is a valid installation
        """
        # anything wrong here is an error
        # if the path to the engine doesn't exist
        if not self.engine.exists():
            # grab a channel
            channel = journal.error("mm.installation")
            # complain
            channel.line(f"could not find the path to my makefiles")
            channel.line(f"while verifying my installation")
            channel.indent()
            channel.line(f"the path '{self.engine}'")
            channel.line(f"doesn't exist or is not readable")
            channel.outdent()
            channel.line(f"check your setting for my 'engine' property")
            # flush
            channel.log()
        # form the path to the top level makefile
        merlin = self.engine / self.makefile
        # check that the top level makefile exists
        if not merlin.exists():
            # grab a channel
            channel = journal.error("mm.installation")
            # complain
            channel.line(f"could not find my main makefile")
            channel.line(f"while verifying my installation")
            channel.indent()
            channel.line(f"the file '{merlin}'")
            channel.line(f"doesn't exist or is not readable")
            channel.outdent()
            channel.line(f"check your setting for my 'makefile' property")
            # flush
            channel.log()
        # if the path to the {portinfo} headers doesn't exist
        if not self.portinfo.exists():
            # grab a channel
            channel = journal.error("mm.installation")
            # complain
            channel.line(f"can't find my include directory")
            channel.line(f"while verifying my installation")
            channel.indent()
            channel.line(f"the path '{self.portinfo}'")
            channel.line(f"doesn't exist or is not readable")
            channel.outdent()
            channel.line(f"check your setting for my 'portinfo' property")
            # flush
            channel.log()
        # form the path to the {portinfo}
        portinfo = self.portinfo / "portinfo"
        # check that the top level header file exists
        if not portinfo.exists():
            # grab a channel
            channel = journal.error("mm.installation")
            # complain
            channel.line(f"could not find my top level header file")
            channel.line(f"while verifying my installation")
            channel.indent()
            channel.line(f"the file '{portinfo}'")
            channel.line(f"doesn't exist or is not readable")
            channel.outdent()
            channel.line(f"check your setting for my 'portinfo' property")
            # flush
            channel.log()
        # all done
        return merlin

    def verifyGNUMake(self):
        """
        Get the GNU make version and verify it's sufficiently recent
        """
        # set up the subprocess settings
        settings = {
            "executable": str(self.make),
            "args": [str(self.make), "--version"],
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # attempt to
        try:
            # invoke GNU make to extract its version
            with subprocess.Popen(**settings) as make:
                # wait for it to finish and harvest its exit code
                stdout, stderr = make.communicate()
                # grab the status code
                status = make.returncode
                # if there was an error
                if status != 0:
                    # grab a channel
                    channel = journal.error("mm.gnu")
                    # complain
                    channel.line(f"failed to launch '{self.make}'")
                    channel.line(
                        f"while attempting to retrieve the version of GNU make"
                    )
                    channel.indent()
                    channel.line(f"'{self.make}' returned error code {status}")
                    channel.outdent()
                    channel.line(f"check your setting for my 'make' property")
                    # flush
                    channel.log()
                    # and bail, just in case errors aren't fatal
                    return
                # otherwise, grab the first line of output
                signature = stdout.splitlines()[0]
                # take it apart using the GNU make version parser
                match = self.gnuMakeVersionParser.match(signature)
                # if it doesn't match
                if not match:
                    # we have a problem
                    channel = journal.error("mm.gnu")
                    # complain
                    channel.line(f"could not find a suitable installation of GNU make")
                    channel.line(f"while verifying my installation")
                    channel.indent()
                    channel.line(f"'{self.make}' doesn't seem to be GNU make")
                    channel.line(f"you need GNU make 4.4 or higher")
                    channel.outdent()
                    channel.line(f"check your setting for my 'make' property")
                    # flush
                    channel.log()
                    # and bail, just in case errors aren't fatal
                    return
                # get the version info
                major, minor, micro = map(int, match.groups(default=0))
                # we need 4.4 or higher, for the {.WAIT} prerequisite ordering primitive
                if (major, minor, micro) < (4, 4, 0):
                    # we have a problem
                    channel = journal.error("mm.gnu")
                    # complain
                    channel.line(f"your version of GNU make is too old")
                    channel.line(f"while verifying my installation")
                    channel.indent()
                    channel.line(f"you need GNU make 4.4 or higher")
                    channel.line(
                        f"your '{self.make}' version is {major}.{minor}.{micro}"
                    )
                    channel.outdent()
                    channel.line(f"check your setting for my 'make' property")
                    # flush
                    channel.log()
                    # and bail, just in case errors aren't fatal
                    return
        # if the executable could not be found
        except FileNotFoundError as error:
            # we have a problem
            channel = journal.error("mm.gnu")
            # complain
            channel.line(f"an unexpected error occurred")
            channel.line(f"while attempting to retrieve the version of GNU make")
            channel.indent()
            channel.line(f"could not find '{self.make}'")
            channel.line(f"launching it resulted in: {error}")
            channel.outdent()
            channel.line(f"check your setting for my 'make' property")
            # flush
            channel.log()
        # if the launch fails in a more general way
        except OSError as error:
            # we have a problem
            channel = journal.error("mm.gnu")
            # complain
            channel.line(f"an unexpected error occurred")
            channel.line(f"while attempting to retrieve the version of GNU make")
            channel.indent()
            channel.line(f"launching '{self.make}' returned")
            channel.line(f"{error}")
            channel.outdent()
            channel.line(f"check your setting for my 'make' property")
            # flush
            channel.log()
        # if {subprocess} detected some other kind of problem
        except subprocess.SubprocessError as error:
            # we have a problem
            channel = journal.error("mm.gnu")
            # complain
            channel.line(f"an unexpected error occurred")
            channel.line(f"while attempting to retrieve the version of GNU make")
            channel.indent()
            channel.line(f"launching '{self.make}' failed with")
            channel.line(f"{error}")
            channel.outdent()
            channel.line(f"check your setting for my 'make' property")
            # flush
            channel.log()

        # all done
        return

    def locateUserConfig(self):
        """
        Find the user configuration directory
        """
        # figure out where the configuration directory is; first, try looking for an XDG compliant
        # layout; perhaps the system sets up the mandated environment variable
        xdgHome = (
            pyre.primitives.path(os.getenv("XDG_CONFIG_HOME", self.XDG_CONFIG))
            .expanduser()
            .resolve()
        )
        # point to the {mm} specific directory
        xdg = xdgHome / "mm"
        # if it is a real directory
        if xdg.exists() and xdg.isDirectory():
            # hand it off
            return xdg
        # otherwise, get the user's home directory
        home = self.user.home
        # if it's not a good place
        if not (home and home.exists()):
            # and we are allowed to speak
            if not self.quiet:
                # make a channel
                channel = journal.warning("mm.user")
                # complain
                channel.line(f"could not find your home directory")
                channel.line(f"while looking for user specific makefile fragments")
                channel.indent()
                channel.line(f"'{home}' is not a valid path")
                channel.line(f"and your system doesn't have any good ideas")
                channel.outdent()
                channel.line(f"is this a cloud instance?")
                channel.line(
                    f"if not, check the value of your 'HOME' environment variable"
                )
                # flush
                channel.log()
            # nothing further to do
            return None
        # look for the configuration directory
        candidate = home / self.cfgdir
        # if it exists and it is a directory
        if candidate.exists() and candidate.isDirectory():
            # hand it off
            return candidate
        # if we couldn't find it
        if not self.quiet:
            # pick a channel
            channel = journal.warning("mm.user")
            # complain
            channel.line(f"could not find your makefile fragments")
            channel.line(f"while looking for user specific configuration")
            channel.indent()
            channel.line(f"neither '{xdg}'")
            channel.line(f"nor '{candidate}'")
            channel.line(f"exist and are readable")
            channel.outdent()
            channel.line(f"if this is unexpected, check")
            channel.indent()
            channel.line(f"the value of your 'XDG_CONFIG_HOME' environment variable")
            channel.line(f"or the value of your 'HOME' environment variable")
            channel.line(f"and the value of my 'cfgdir' property")
            channel.outdent()
            # flush
            channel.log()
        # all done
        return None

    def locateProjectRoot(self):
        """
        Find the project root directory
        """
        # use my configuration directory as the target of the hunt
        marker = self.cfgdir
        # hunt it down, starting at the current working directory
        root = self.locateMarker(marker=marker)
        # if it's not there
        if not root:
            # use the current working directory
            root = pyre.primitives.path.cwd()
            # if we are allowed to speak
            if not self.quiet:
                # make a channel
                channel = journal.warning("mm.project")
                # complain
                channel.line(f"could not find the project root directory")
                channel.line(f"while exploring the current workspace")
                channel.indent()
                channel.line(f"no '{marker}' directory")
                channel.line(f"in '{root}' or any of its parents")
                channel.outdent()
                channel.line(
                    f"if this is unexpected, check the value of my 'cfgdir' property"
                )
                # flush
                channel.log()
        # all done
        return root

    def locateProjectConfig(self):
        """
        Find the project configuration directory
        """
        # assuming that {_root} points to a valid directory, form the expected location
        candidate = self._root / self.cfgdir
        # check whether it's a valid path and hand it off to the caller
        # N.B.:
        #     no reason to complain here; if {candidate} doesn't exist, a warning has been
        #     generated already by {locateProjectRoot}
        return candidate if candidate.exists() else None

    def locateLocalMakefile(self):
        """
        Find the location of the local makefile
        """
        # get the name of the local makefile
        local = self.local
        # if the user hasn't bothered
        if not local:
            # don't go looking
            return None
        # otherwise, look for it
        location = self.locateMarker(marker=self.local, sentinel=self._root)
        # and return its location
        return location

    def locateBuildRoot(self):
        """
        Figure out where to put the intermediate products of the build
        """
        return self._bldrootDispatch[self.mode]()

    def locatePrefix(self):
        """
        Figure out where to install the build products
        """
        return self._prefixDispatch[self.mode]()

    def locateToolchains(self):
        """
        Figure out where environment-level developer toolchains are installed; the location is
        keyed by the active environment rather than the build context, so a toolchain is shared
        across every build variant while still tracking where node and python come from
        """
        # if the user has expressed an opinion
        if self.toolchains is not None:
            # use it
            return self.toolchains
        # otherwise anchor on a per-environment directory under the user's tools tree
        base = pyre.primitives.path("~/tools/mm").expanduser()
        # get the active environment
        env = self.environment
        # and fold it the environment name, when there is one
        return base / env / "toolchains" if env else base / "toolchains"

    def deduceCompilerSuite(self):
        """
        Look through the set of {compilers} to deduce the name of the compiler suite that
        determines the runtime ABI
        """
        # for now, look for the first chosen compiler that is not fully resolved
        suite = next((c for c in self.compilers if "/" not in c), "")
        # and call it a day
        return suite

    def assembleBuildTarget(self):
        """
        Construct the build tag that indicates platform and build characteristics
        """
        # get the target platform; note that this may be different that
        # the machine on which mm is running
        host = self.host
        # the target platform is made out of its name and architecture
        target = [host.platform, host.cpus.architecture]
        # assemble the variants
        variants = list(sorted(self.target))
        # and build the tag
        tag = "-".join(filter(None, variants + target))
        # all done
        return target, variants, tag

    def loadProjectConfig(self):
        """
        Look for configuration files in the project area and load them
        """
        # get the directory with the project configuration
        projectCfg = self._projectCfg
        # if it doesn't exist
        if projectCfg is None:
            # nothing further to do
            return
        # otherwise, form the path to the configuration file
        cfg = projectCfg / "mm.yaml"
        # if the file exists:
        if cfg.exists():
            # load it
            pyre.loadConfiguration(cfg)
        # next, look for a branch specific configuration file; get the name of the branch
        branch = self.gitCurrentBranch()
        # form the name of the configuration file
        cfg = projectCfg / f"{branch}.yaml"
        # and if the file exists
        if cfg.exists():
            # load it
            pyre.loadConfiguration(cfg)
        # all done
        return

    def updateEnvironmentVariables(self):
        """
        Incorporate the build configuration into the relevant environment variables
        """
        # get the installation directory
        prefix = self._prefix
        # configure the environment
        # the path
        self.PATH = self.inject(var=self.PATH, path=(prefix / "bin"))
        # the dynamic linker path
        # the python path
        self.PYTHONPATH = self.inject(var=self.PYTHONPATH, path=(prefix / "packages"))
        # configure mm
        # update the compiler include path
        self.incpath = self.inject(var=self.incpath, path=(prefix / "include"))
        self.incpath = self.inject(var=self.incpath, path=self.portinfo)
        # update the linker library path
        self.libpath = self.inject(var=self.libpath, path=(prefix / "lib"))
        # all done
        return

    def configureMake(self):
        """
        Generate command line arguments for make
        """
        # start off with the executable
        yield str(self.make)
        # complain about typos
        yield "--warn-undefined-variables"
        # if the user asked to ignore build failures
        if self.ignore:
            # ask make to comply
            yield "--keep-going"
        # if the user did not explicitly ask to see action details
        if not self.verbose:
            # silence them
            yield "--silent"
        # if the user asked to see the database of rules
        if self.rules:
            # ask make to print them out
            yield "--print-data-base"
        # if the user wants trace information
        if self.trace:
            # ask make to generate it
            yield "--trace"
        # parallelism
        yield from self.computeSlots()
        # add the top level makefile to the pile
        yield f"--makefile={self._makefile}"
        # adjust the include path so make can find our makefile fragments
        # first, get any extra paths the user has asked for explicitly
        for cfg in self.runcfg:
            # the ones that exist
            if cfg.exists():
                # get folded with the include flag
                yield f"--include-dir={cfg}"
            # the rest
            else:
                # unless told otherwise
                if not self.quiet:
                    # generate a warning
                    channel = journal.warning("mm.includes")
                    # complain
                    channel.line(f"while assembling the make command line")
                    channel.indent()
                    channel.line(f"the path '{cfg}' does not exist")
                    channel.outdent()
                    channel.line(f"check your setting for my 'runcfg' property")
                    # flush
                    channel.log()
        # if the user configuration directory exists
        if self._userCfg:
            # add it to the pile
            yield f"--include-dir={self._userCfg}"
        # similarly, if the path to the project configuration exists
        if self._projectCfg:
            # add it to the pile
            yield f"--include-dir={self._projectCfg}"
        # finally, add the path to the implementation makefiles
        yield f"--include-dir={self.engine.parent}"

        # all done
        return

    def configureProject(self):
        """
        Build the variable assignments that communicate the project configuration
        to the implementation engine
        """
        # the project home
        yield f"project.home={self._root}"
        # the build mode, so the make subsystem can gate behavior on {mode != dev}
        yield f"project.mode={self.mode}"
        # the path to the mm configuration files
        yield f"project.config={self._projectCfg}"
        # the location to place the intermediate build products
        yield f"project.bldroot={self._bldroot}"
        # the path from which mm was invoked
        yield f"project.origin={self._origin}"
        # the path from which make was invoked by mm
        yield f"project.anchor={self._anchor}"
        # if there is  local makefile
        yield f"project.makefile={self._localMakefile or ''}"
        # the installation location
        yield f"project.prefix={self._prefix}"
        # the layout of the installation area
        yield f"builder.dest.bin={self._prefix / self.binPrefix}/"
        yield f"builder.dest.lib={self._prefix / self.libPrefix}/"
        yield f"builder.dest.inc={self._prefix / self.incPrefix}/"
        yield f"builder.dest.pyc={self._prefix / (self._pycPrefix or self.pycPrefix)}/"
        yield f"builder.dest.doc={self._prefix / self.docPrefix}/"
        yield f"builder.dest.share={self._prefix / self.sharePrefix}/"
        yield f"builder.dest.etc={self._prefix / self.etcPrefix}/"
        yield f"builder.dest.var={self._prefix / self.varPrefix}/"
        # all done
        return

    def configureVersion(self):
        """
        Build the version information that mm will use to tag the build
        """
        # get the user's choice
        version = self.version
        # if we have an explicit version
        if version:
            # parse it, assuming it of the form "major.minor.micro"
            major, minor, micro = version.split(".")
            # give default values to the two other fields
            ahead = 0
            revision = ""
        # if we don't
        else:
            # attempt to derive one from the most recent git tag
            version = self.gitDescribe()
            # if git knows
            if version:
                # unpack
                major, minor, micro, revision, ahead = version
            # otherwise
            else:
                # do something stupid
                major, minor, micro, revision, ahead = 0, 0, 1, "", 0
                # and if we are allowed to make noise
                if not self.quiet:
                    # get a channel
                    channel = journal.warning("mm.version")
                    # complain
                    channel.line(f"while figuring out the product version")
                    channel.indent()
                    channel.line(f"no explicit setting was provided")
                    channel.line(f"and parsing the latest git tag failed")
                    channel.line(
                        f"using the default value of '{major}.{minor}.{micro}'"
                    )
                    channel.line(f"but that's probably not what you want")
                    channel.outdent()
                    channel.line(
                        f"please use '--version' to provide a reasonable value"
                    )
                    # flush
                    channel.log()
        # in any case, we know have what we need to send to mm
        yield f"repo.major={major}"
        yield f"repo.minor={minor}"
        yield f"repo.micro={micro}"
        yield f"repo.revision={revision}"
        yield f"repo.ahead={ahead}"
        # all done
        return

    def configureTarget(self):
        """
        Build the variable assignments that communicate the build target
        to the implementation engine
        """
        # set the target
        yield f"target={'-'.join(self._bldTarget)}"
        # its tag
        yield f"target.tag={self._bldTag}"
        # and the list of variants
        yield f"target.variants={' '.join(self._bldVariants)}"
        # all done
        return

    def describeUser(self):
        """
        Describe the user that invoked mm
        """
        # get the user info
        user = self.user
        # hand off the username
        yield f"user.username={user.username}"
        # the home directory
        yield f"user.home={user.home}"
        # the path to the user specific configuration file
        yield f"user.config={self._userCfg or ''}"
        # the uid
        yield f"user.uid={user.uid}"
        # full name
        yield f"user.name={user.name}"
        # email
        yield f"user.email={user.email}"
        # and environment
        yield f"user.environment={self.environment}"
        # all done
        return

    def describeHost(self):
        """
        Describe the host mm is running on
        """
        # ask the executive for the host info
        host = pyre.executive.host
        # hand off its name
        yield f"host.name={host.hostname}"
        # nickname
        yield f"host.nickname={host.nickname}"
        # the host os
        yield f"host.os={host.platform}"
        # architecture
        yield f"host.arch={host.cpus.architecture}"
        # and number of cores
        yield f"host.cores={host.cpus.cpus}"
        # all done
        return

    def relaunchArguments(self):
        """
        Yield the command-line arguments a recursively launched {mm} needs to reproduce this
        invocation's build-product locations (e.g. so the pkgdb rebuild lands where the parent
        expects it). The candidate set is an allowlist of the traits that shape {bldroot} and
        {prefix} — so an action like {--setup} can never be forwarded — and within it only the
        traits the user actually set on the command line are emitted
        """
        # the path-determining traits; this set has been stable for years and is cheap to extend
        for name in (
            "mode",
            "bldroot",
            "prefix",
            "tag",
            "environment",
            "compilers",
            "target",
        ):
            # the child reconstructs config-file, environment, and default values by itself
            if not self._fromCommandLine(name):
                continue
            # the resolved value
            value = getattr(self, name)
            # a path is a tuple of segments, so render it as a single string before anything
            # mistakes it for a multi-valued trait
            if isinstance(value, pyre.primitives.path):
                value = str(value)
            # genuinely multi-valued traits (compilers, target) are comma-separated
            elif isinstance(value, (list, tuple)):
                value = ",".join(map(str, value))
            # everything else stringifies directly
            else:
                value = str(value)
            # quote it so paths and values with spaces survive the make recipe shell
            yield f"--{name}='{value}'"

    def configureBuilder(self):
        """
        Configure the engine
        """
        # record how mm was invoked, including the arguments a recursive launch needs to land
        # its build products — and the pkgdb — in the same place as this invocation
        yield "mm=" + " ".join([sys.executable, __file__, *self.relaunchArguments()])
        # the version
        yield f"mm.version={self._version}"
        # the directory that holds the make engine, so {mm.home}/make is the engine root
        yield f"mm.home={self.engine.parent}"
        # the path to the top level makefile
        yield f"mm.merlin={self._makefile}"
        # the location of the built-in package database
        yield f"mm.extern={self.engine / 'extern'}"
        # the root of the environment-level developer toolchains
        yield f"toolchains.home={self._toolchains}"
        # the package manager
        yield f"mm.pkgdb={self.pkgdb}"
        # the list of compilers
        yield f"mm.compilers={' '.join(self.compilers)}"
        # the compiler header search path
        yield f"mm.incpath={' '.join(map(str, self.incpath))}"
        # the linker library search path
        yield f"mm.libpath={' '.join(map(str, self.libpath))}"
        # indicate whether the output should be colorized
        yield f"mm.color={'' if self.color else 'no'}"
        # and the palette to use
        yield f"mm.palette={self.palette}"
        # all done
        return

    # framework hooks
    def pyre_banner(self):
        """
        Generate the application banner
        """
        # sign on
        yield "  merlin mm {}.{}.{} rev {}".format(*merlin.meta.version)
        # all done
        return

    def pyre_help(self, indent=" " * 2):
        """
        Display the current configuration
        """
        # chain up
        yield from super().pyre_help(indent=indent)
        # make a pile for my public state
        public = []
        # collect my traits
        for trait in self.pyre_configurables():
            # get the name
            name = trait.name
            # and the tip
            tip = trait.tip or trait.doc
            # skip nameless undocumented ones
            if not name or not tip:
                continue
            # pile the rest
            public.append(name)

        # if we were able to find any trait info
        if public:
            # mark the section
            yield f"current configuration:"
            # figure out how much space we need
            width = max(map(len, public)) + 2  # for the dashes
            # for each public trait
            for name in public:
                # make a tag out of the name
                tag = f"--{name}"
                # show its details
                yield f"{indent}{tag:>{width}}: {getattr(self, name)}"
            # leave some space
            yield ""

        # all done
        return

    # helpers
    def locateMarker(self, marker, folder=None, sentinel=None):
        """
        Scan upwards for a directory that contains {marker}, starting at {folder}, if given, or
        the current working directory
        """
        # start with the current directory, unless the caller has opinions
        folder = pyre.primitives.path.cwd() if folder is None else folder
        # go through folders on the way to the root
        for candidate in folder.crumbs:
            # form the filename
            target = candidate / marker
            # if it exists
            if target.exists():
                # we have found the place
                return candidate
            # if we have reached the {sentinel}
            if sentinel and candidate == sentinel:
                # bail
                break
        # if we get this far, {marker} could not be found
        return None

    def inject(self, var, path):
        """
        Prepend {path} to {var}, keeping each value's first appearance only
        """
        # track what we have already yielded
        seen = set()
        # the new path always comes first
        yield path
        # save it
        seen.add(path)
        # go through the rest of the values in {var}
        for p in var:
            # if it hasn't been emitted before
            if p not in seen:
                # emit
                yield p
                # and remember
                seen.add(p)
        # all done
        return

    def eject(self, var, path):
        """
        Remove {path} from {var}
        """
        # go through the values in {var}
        for p in var:
            # skip the one we want to remove
            if p != path:
                # pass everything else through
                yield p
        # all done
        return

    def computeSlots(self):
        """
        Choose the number of jobs tha GNU make will execute in parallel
        """
        # if the user doesn't want any parallelism
        if self.serial:
            # let {make} know to execute only one recipe at a time
            yield f"--jobs=1"
            # all done
            return
        # get the user choice
        slots = self.slots
        # if the user hasn't expressed an opinion
        if slots is None:
            # let {make} figure it out
            yield "-j"
            # all done
            return
        # otherwise, use the user's value
        yield f"--jobs={slots}"

    def gitDescribe(self):
        """
        Extract project version metadata from the most recent git tag
        """
        # the git command line
        cmd = ["git", "describe", "--tags", "--long", "--always"]
        # settings
        options = {
            "executable": "git",
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, stderr = git.communicate()
            # get the status
            status = git.returncode
            # if something went wring
            if status != 0:
                # bail
                return
            # get the description
            description = stdout.strip()
            # parse it
            match = self.gitDescriptionParser.match(description)
            # if something went wrong
            if not match:
                # bail
                return
            # otherwise, extract the version info
            major = match.group("major") or "1"
            minor = match.group("minor") or "0"
            micro = match.group("micro") or "0"
            commit = match.group("commit")
            ahead = match.group("ahead")
            # if we are at a tagged commit
            if not ahead or int(ahead) == 0:
                # make sure {ahead} is an empty string
                ahead = ""
            # and return it
            return (major, minor, micro, commit, ahead)
        # if anything went wrong
        return

    def gitCurrentBranch(self):
        """
        Extract the name of the current git branch
        """
        # the git command line
        cmd = ["git", "branch", "--show-current"]
        # settings
        options = {
            "executable": "git",
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, stderr = git.communicate()
            # get the status
            status = git.returncode
            # if something went wring
            if status != 0:
                # bail
                return "unknown"
            # get the branch name
            branch = stdout.strip()
            # and return it
            return branch
        # if anything went wrong
        return "unknown"

    # private data
    # the XDG compliant fallback for user configuration
    XDG_CONFIG = pyre.primitives.path("~/.config")
    # make version
    gnuMakeVersionParser = re.compile(
        r"GNU Make (?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<micro>\d+))?"
    )
    # parser of the {git describe} result
    gitDescriptionParser = re.compile(
        r"(v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<micro>\d+)-(?P<ahead>\d+)-g)?(?P<commit>.+)"
    )

    def _fromCommandLine(self, name):
        """
        Test whether the value of the trait named {name} came from the command line, as opposed
        to a config file, an environment-derived default, or the trait default. Only command-
        line overrides are invisible to a recursively launched {mm}: the child runs in the same
        directory and inherits the same environment, so it reproduces everything else on its own
        """
        # the trait descriptor
        trait = self.pyre_trait(name)
        # the priority of its current value records which configuration category assigned it
        priority = self.pyre_inventory.getTraitPriority(trait)
        # command-line assignments belong to the {command} category; this is the same idiom
        # pyre itself uses to recognize a category (see framework/NameServer)
        return priority.category == priority.command.category

    def _buildAdhocPackageDatabase(self, db):
        """
        Create an empty package database for an ad-hoc build; the user is expected to have
        populated their own configuration files with the necessary package locations
        """
        # just touch the file so the build engine finds it
        open(db, "w")
        # all done
        return 0

    def _buildCondaPackageDatabase(self, db):
        """
        Interrogate the active conda/micromamba environment and write a package database by
        reading the on-disk {conda-meta} install records, without invoking the conda agent
        """
        # grab a channel
        channel = journal.info("mm.pkgdb")
        # check for an active conda environment
        prefix = os.environ.get("CONDA_PREFIX")
        # if there isn't one
        if not prefix:
            # grab an error channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line("no active conda environment found")
            error.line("activate a conda environment and re-run mm")
            error.log()
            # and bail
            return 1
        # the install database of the active environment
        meta = pyre.primitives.path(prefix) / "conda-meta"
        # if it isn't there, {CONDA_PREFIX} doesn't point at a real environment
        if not meta.isDirectory():
            # grab an error channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line(f"'{prefix}' is not a conda environment")
            error.line(f"no install database at {meta}")
            # flush
            error.log()
            # and bail
            return 1
        # log our starting state
        channel.line("building conda package database")
        channel.indent()
        channel.line(f"environment: {os.environ.get('CONDA_DEFAULT_ENV', '?')}")
        channel.line(f"prefix: {prefix}")
        channel.line(f"db: {db}")
        channel.outdent()
        channel.log()
        # index the installed packages by reading the {conda-meta} record names
        index = self._condaMetaIndex(meta)
        # the registry of supported externals and how each maps to conda packages
        recipes = self._condaRecipes()
        # the externals that intentionally have no conda recipe
        exceptions = self._condaExceptions()
        # warn if make/extern has gained a package neither registry accounts for
        self._condaCheckCoverage(recipes, exceptions)
        # resolve them against the installed packages
        entries = self._condaResolve(recipes, index, prefix)
        # report what we found
        channel.line(f"found {len(entries)} of {len(recipes)} supported packages")
        # list each one
        channel.indent()
        for entry in sorted(entries, key=lambda e: e["name"]):
            channel.line(f"{entry['name']}: {entry['version']}")
        channel.outdent()
        # flush
        channel.log()
        # get the name of the active environment for the file header
        environmentName = os.environ.get("CONDA_DEFAULT_ENV", "?")
        # open the database file
        with open(db, "w") as f:
            # the emacs mode line
            print("# -*- Makefile -*-", file=f)
            # identification
            print("# conda package database", file=f)
            # provenance
            print("# generated by: mm --pkgdb=conda --setup", file=f)
            # how it was discovered: the on-disk install database, no agent involved
            print(f"# source: {meta}", file=f)
            # the environment name
            print(f"# environment: {environmentName}", file=f)
            # and its prefix
            print(f"# prefix: {prefix}", file=f)
            # blank line before the {conda.prefix} declaration
            print(file=f)
            # the root of the active environment; factored out so all {.dir} entries track it
            print(f"conda.prefix := {prefix}", file=f)
            # the environment name; compared against {user.environment} at build time to catch switches
            print(f"conda.environment := {environmentName}", file=f)
            # blank line before the package entries
            print(file=f)
            # write an entry for each package we found, in alphabetical order
            for entry in sorted(entries, key=lambda e: e["name"]):
                # a comment line showing the mm name, full conda version, and origin
                print(f"# {entry['comment']}", file=f)
                # {?=} throughout so that anything the user set in {config.mm} takes precedence;
                # the load order is config.mm first, then this db, so {?=} here correctly
                # yields to user overrides while still providing the conda defaults
                # the version, for packages whose {init.mm} has version-dependent logic
                print(f"{entry['name']}.version ?= {entry['version']}", file=f)
                # the package-specific configuration lines that the recipe produced
                for line in entry["lines"]:
                    # emit each one
                    print(line, file=f)
                # blank line after each entry
                print(file=f)
        # all done
        return 0

    def _condaMetaIndex(self, meta):
        """
        Index the installed packages of a conda environment by reading the record names in
        {meta}; each record is named {name}-{version}-{build}.json, so a package's presence
        and version come straight from the filename without parsing any JSON
        """
        # the index we are building: conda package name -> (version, build, record path)
        index = {}
        # go through every file in the install database
        for filename in os.listdir(str(meta)):
            # we only care about package records
            if not filename.endswith(".json"):
                continue
            # drop the extension
            stem = filename[: -len(".json")]
            # records always carry the two dashes that separate name, version, and build;
            # anything else (a stray file) is not a package record we can parse
            if stem.count("-") < 2:
                continue
            # split the stem from the right so that dashes in the package name survive
            name, version, build = stem.rsplit("-", 2)
            # stash the record, keyed by package name
            index[name] = (version, build, meta / filename)
        # hand it back
        return index

    def _condaManifestDir(self, record, predicate):
        """
        Parse a conda-meta {record} and return the directory — relative to the environment
        prefix — of the first installed file that satisfies {predicate}, or None; the file
        paths in a record are already prefix-relative, so the directory can be joined onto
        {conda.prefix} directly
        """
        # read the record
        with open(str(record)) as stream:
            # as json
            data = json.load(stream)
        # the files it installed are listed relative to the prefix
        for path in data.get("files", []):
            # as a path
            candidate = pyre.primitives.path(path)
            # if it's the one we're after
            if predicate(candidate):
                # its directory is the answer
                return candidate.parent
        # nothing matched
        return None

    def _condaRecipes(self):
        """
        The registry mapping each supported mm external to the conda package(s) that provide
        it; a boring package lists only its candidate names, a package with an unusual on-disk
        layout names a {handler}, and a compound capability names a {capability}
        """
        # the registry; candidate names are tried in priority order
        return {
            "cantera": {"candidates": ["cantera"]},
            "catch2": {"candidates": ["catch2"]},
            "cgal": {"candidates": ["cgal"]},
            "cspice": {
                "candidates": ["cspice", "naif-cspice"],
                "handler": "_emitCondaCspice",
            },
            "cuda": {"capability": "_emitCondaCuda"},
            "eigen": {"candidates": ["eigen"]},
            "fftw": {"candidates": ["fftw"]},
            "fmt": {"candidates": ["fmt"]},
            "gdal": {"candidates": ["gdal"]},
            "geotiff": {"candidates": ["libgeotiff", "geotiff"]},
            "gmsh": {"candidates": ["gmsh"]},
            "gsl": {"candidates": ["gsl"]},
            "gtest": {"candidates": ["gtest", "libgtest"]},
            "hdf5": {"candidates": ["hdf5"]},
            "kokkos": {"candidates": ["kokkos"]},
            "libpq": {"candidates": ["libpq", "postgresql"]},
            "metis": {"candidates": ["metis"]},
            "mkl": {"candidates": ["mkl"]},
            "mpi": {"candidates": ["openmpi", "mpich"], "handler": "_emitCondaMpi"},
            "numpy": {
                "candidates": ["numpy"],
                "handler": "_emitCondaSitePackage",
                "module": "numpy",
            },
            "openblas": {"candidates": ["openblas"]},
            "parmetis": {"candidates": ["parmetis"]},
            "petsc": {"candidates": ["petsc"]},
            "proj": {"candidates": ["proj"]},
            "pybind11": {
                "candidates": ["pybind11"],
                "handler": "_emitCondaSitePackage",
                "module": "pybind11",
            },
            "pyre": {"candidates": ["pyre"]},
            "python": {"candidates": ["python"], "trim": True},
            "slepc": {"candidates": ["slepc"]},
            "sundials": {"candidates": ["sundials"]},
            "vtk": {"candidates": ["vtk"]},
            "yaml": {"candidates": ["yaml"]},
            "yaml-cpp": {"candidates": ["yaml-cpp"]},
        }

    def _condaExceptions(self):
        """
        The registry of supported externals that intentionally have no conda recipe, each
        mapped to the reason; these are packages mm knows how to use but that cannot — or
        should not — be discovered in a conda environment because they are installed from
        source, managed by the user, or are not conda packages at all. Listed here so the
        coverage check can tell a deliberate omission from a genuine gap
        """
        # name -> why it has no conda recipe
        return {
            "fmm3d": "user-managed; not generally available on conda-forge",
            "fortran": "pseudo-package; enables mixing fortran into a build, contributing "
            "the compiler's fortran runtime ($(compiler.fortran).mixed.libraries) at link "
            "time — a toolchain capability, not a discoverable conda library",
            "libtorch": "user-managed; not generally available on conda-forge",
            "p2": "internal; sandbox for the next generation of pyre",
            "summit": "source-only; in-house finite element code",
        }

    def _condaCheckCoverage(self, recipes, exceptions):
        """
        Compare the externals mm supports — the package directories under {engine}/extern —
        against the union of the conda {recipes} and the {exceptions} registry, and warn about
        any covered by neither; such an orphan means a package was added to make/extern without
        teaching the conda layer how to find it or marking it deliberately exempt
        """
        # the directory that holds one subdirectory per supported external
        externDir = self.engine / "extern"
        # if it isn't there, there is nothing to check; mm is installed in an unexpected way
        if not externDir.isDirectory():
            # quietly skip
            return
        # the externals the conda layer accounts for, one way or another
        known = set(recipes) | set(exceptions)
        # the supported externals are the subdirectories; loose files (init.mm, rules.mm, ...)
        # are framework glue, not packages
        orphans = sorted(
            entry
            for entry in os.listdir(str(externDir))
            if (externDir / entry).isDirectory() and entry not in known
        )
        # if every supported package is accounted for, we are done
        if not orphans:
            return
        # otherwise tell the developer; a warning rather than an error so it never blocks a
        # build — the orphan may deserve a recipe, an exception entry, or neither in this env
        warning = journal.warning("mm.pkgdb")
        # what happened
        warning.line("these externals under make/extern have no conda recipe:")
        # name them
        warning.indent()
        # one per line
        for orphan in orphans:
            # the offending package
            warning.line(orphan)
        warning.outdent()
        # what to do about it
        warning.line("add a recipe to _condaRecipes, or list it in _condaExceptions")
        # flush
        warning.log()

    def _condaResolve(self, recipes, index, prefix):
        """
        Resolve each supported external in {recipes} against the {index} of installed conda
        packages, returning a database entry for every one that is present and usable
        """
        # the entries we will write
        entries = []
        # go through the recipes
        for name, recipe in recipes.items():
            # a compound capability owns its own discovery and diagnostics
            capability = recipe.get("capability")
            # if this is one
            if capability:
                # let it decide whether the package can actually be built against
                entry = getattr(self, capability)(index, prefix)
                # record it if so
                if entry:
                    entries.append(entry)
                # on to the next recipe
                continue
            # otherwise, find the first installed candidate, in priority order
            candidate = next((c for c in recipe["candidates"] if c in index), None)
            # if none of them are installed, the package is absent
            if candidate is None:
                continue
            # unpack the record
            version, build, record = index[candidate]
            # trim to major.minor for packages that key interpreter names and paths off it
            mmVersion = (
                self._condaMajorMinor(version) if recipe.get("trim") else version
            )
            # the entry, ready for any package-specific configuration lines
            entry = {
                "name": name,
                "comment": f"{name} {version}  (conda: {candidate})",
                "version": mmVersion,
                "lines": [],
            }
            # a custom emitter for packages whose layout isn't boring
            handler = recipe.get("handler")
            # if there is one
            if handler:
                # let it populate the configuration lines
                getattr(self, handler)(entry, recipe, candidate, record, prefix)
            # otherwise the boring default: {dir} tracks {conda.prefix} and the
            # {name}/init.mm defaults ({dir}/include, {dir}/lib) do the rest
            else:
                # a conditional lazy reference to {conda.prefix}
                entry["lines"].append(f"{name}.dir ?= $(conda.prefix)")
            # keep it
            entries.append(entry)
        # hand back what we found
        return entries

    def _condaMajorMinor(self, version):
        """
        Trim a version string to {major.minor}; some packages (python) use this form in
        interpreter names and filesystem paths like {lib/python3.12}
        """
        # split into components
        parts = version.split(".")
        # keep the first two if we have them, otherwise return it unchanged
        return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else version

    def _emitCondaMpi(self, entry, recipe, candidate, record, prefix):
        """
        Emit the configuration for mpi; besides {dir}, the flavor (openmpi or mpich) selects
        the library names in {mpi/init.mm}
        """
        # {dir} tracks the environment root
        entry["lines"].append("mpi.dir ?= $(conda.prefix)")
        # the flavor is the conda package that satisfied the dependency
        entry["lines"].append(f"mpi.flavor ?= {candidate}")

    def _emitCondaCspice(self, entry, recipe, candidate, record, prefix):
        """
        Emit the configuration for cspice; CSPICE code includes its umbrella header flat, as
        {<SpiceUsr.h>}, but conda relocates the canonically flat headers into an
        {include/cspice} subdirectory, so the include path must point at wherever
        {SpiceUsr.h} actually landed rather than the {cspice/init.mm} default of {dir}/include
        """
        # {dir} tracks the environment root so the {libpath} default still resolves
        entry["lines"].append("cspice.dir ?= $(conda.prefix)")
        # ask the install manifest which directory the umbrella header landed in
        incdir = self._condaManifestDir(record, lambda path: path.name == "SpiceUsr.h")
        # if the header turned up, point {incpath} straight at its directory so the flat
        # {<SpiceUsr.h>} include resolves; this absorbs the conda {cspice} subdirectory and
        # collapses to {dir}/include for a canonically flat install
        if incdir:
            # anchor it to the environment root
            entry["lines"].append(f"cspice.incpath ?= $(conda.prefix)/{incdir}")
        # otherwise we cannot trust the include path; warn and leave the init.mm default
        else:
            # a warning rather than a hard failure: cspice is installed, just not where we expect
            warning = journal.warning("mm.pkgdb")
            # what happened
            warning.line(
                f"cspice is installed in '{prefix}' but SpiceUsr.h was not found"
            )
            # the consequence
            warning.line("leaving the default include path; it may be wrong")
            # flush
            warning.log()

    def _emitCondaSitePackage(self, entry, recipe, candidate, record, prefix):
        """
        Emit the configuration for a python package whose headers live in site-packages rather
        than {prefix}/include (numpy, pybind11); ask the package where its headers are and
        anchor {dir} to their parent so the {dir}/include and {dir}/lib defaults resolve
        """
        # the importable module name and the mm package name
        module = recipe["module"]
        target = entry["name"]
        # ask the package where its headers are
        includePath = self._queryPythonExpression(
            f"import {module}; print({module}.get_include())"
        )
        # if the query failed, fall back to {conda.prefix}; the defaults won't be right,
        # but it's the best we can do without the package telling us where it lives
        if not includePath:
            # the conservative fallback
            entry["lines"].append(f"{target}.dir ?= $(conda.prefix)")
            # nothing more to do
            return
        # the package root is the parent of its include directory
        root = pyre.primitives.path(includePath).parent
        # if it's within the conda prefix, anchor it to {conda.prefix} so the entry stays
        # portable across environments
        try:
            # express it relative to the environment root
            relativePath = root.relativeTo(prefix)
            # and record the anchored form
            entry["lines"].append(f"{target}.dir ?= $(conda.prefix)/{relativePath}")
        # otherwise fall back to the absolute path
        except ValueError:
            # record where it actually is
            entry["lines"].append(f"{target}.dir ?= {root}")

    def _emitCondaCuda(self, index, prefix):
        """
        Resolve cuda as a capability: it is usable only if the compiler ({cuda-nvcc}) and the
        runtime dev package ({cuda-cudart-dev}) are both present. The package set is version-
        keyed — cuda <= 11 is a single {cudatoolkit}, 12.x+ is a split stack — so a partial
        install is reported and cuda is left out of the database rather than letting the
        compiler or linker fail later. Returns a database entry, or None if cuda is absent or
        unusable
        """

        # a package family is present if any installed package starts with the stem; conda-forge
        # ships cuda as cross-arch umbrellas ({cuda-nvcc}) that depend on arch-specific splits
        # ({cuda-nvcc_linux-64}), and the umbrella is what the user installs
        def installed(stem):
            # the umbrella itself, or any of its arch splits
            return any(name == stem or name.startswith(stem + "_") for name in index)

        # modern conda-forge layout: a split stack pinned by {cuda-version}
        if "cuda-version" in index:
            # the families we must have to compile and link cuda code
            required = ["cuda-nvcc", "cuda-cudart-dev"]
            # any that are missing make the toolkit unusable
            missing = [stem for stem in required if not installed(stem)]
            # if the stack is incomplete
            if missing:
                # warn about a systemic problem the user should fix before building
                warning = journal.warning("mm.pkgdb")
                # what is wrong
                warning.line(f"cuda is partially installed in '{prefix}'")
                # which pieces are missing
                warning.line(f"missing: {', '.join(missing)}")
                # the consequence
                warning.line("cuda support disabled")
                # flush
                warning.log()
                # and leave cuda out of the database
                return None
            # the toolkit version comes free from the {cuda-version} pin
            version = index["cuda-version"][0]
            # the records that may carry the headers; conda-forge keeps them in the arch split
            headerRecords = [
                record
                for name, (_, _, record) in index.items()
                if name.startswith("cuda-cudart-dev")
            ]
            # provenance for the database comment
            candidate = "cuda-version + " + " + ".join(required)
        # legacy single-package layout: everything lives in {cudatoolkit}
        elif "cudatoolkit" in index:
            # the version and the one record that owns everything, headers included
            version, _, record = index["cudatoolkit"]
            # so that is the only place to look for the headers
            headerRecords = [record]
            # provenance
            candidate = "cudatoolkit"
        # cuda simply isn't installed in this environment
        else:
            # nothing to emit
            return None
        # locate {cuda.h} to discover the sysroot: conda-forge keeps it under
        # targets/<arch>/include and does NOT symlink it into {prefix}/include, so the include
        # directory and its parent (the root that holds both include/ and lib/) must be read
        # from the manifest rather than assumed to be {prefix}
        incdir = None
        # scan the records that might own the headers
        for record in headerRecords:
            # probe this manifest for {cuda.h}
            incdir = self._condaManifestDir(record, lambda path: path.name == "cuda.h")
            # stop at the first hit
            if incdir:
                break
        # if the headers turned up, the sysroot is the directory that holds include/ and lib/
        if incdir:
            # the cuda root is the parent of the include directory
            sysroot = incdir.parent
            # a sysroot of '.' means the headers sit directly under {prefix}/include
            dirLine = (
                "cuda.dir ?= $(conda.prefix)"
                if str(sysroot) == "."
                else f"cuda.dir ?= $(conda.prefix)/{sysroot}"
            )
        # otherwise we cannot trust the include path; warn and fall back to the prefix
        else:
            # a warning rather than a hard failure: cuda is installed, just not where we expect
            warning = journal.warning("mm.pkgdb")
            # what happened
            warning.line(f"cuda is installed in '{prefix}' but cuda.h was not found")
            # the consequence
            warning.line(
                "falling back to the environment prefix; the include path may be wrong"
            )
            # flush
            warning.log()
            # the conservative fallback
            dirLine = "cuda.dir ?= $(conda.prefix)"
        # {dir} drives the {cuda/init.mm} incpath default ({cuda.dir}/include plus the cuda-13
        # cccl wildcard); the default libpath is {lib64}, which the conda sysroot does not use,
        # so override it to the sibling {lib} of the include directory
        lines = [dirLine, "cuda.libpath ?= $(cuda.dir)/lib"]
        # hand back the entry
        return {
            "name": "cuda",
            "comment": f"cuda {version}  (conda: {candidate})",
            "version": self._condaMajorMinor(version),
            "lines": lines,
        }

    def _buildMacportsPackageDatabase(self, db):
        """
        Interrogate the active MacPorts installation and write a package database
        """
        # grab a channel
        channel = journal.info("mm.pkgdb")
        # find the port executable
        port = shutil.which("port")
        # if not found
        if not port:
            # make a channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line("could not find the 'port' executable")
            error.line("make sure MacPorts is installed and 'port' is on your PATH")
            # flush
            error.log()
            # bail
            return 1
        # derive the MacPorts prefix from the port executable location
        prefix = pyre.primitives.path(port).parent.parent
        # get the selected python3 version
        result = subprocess.run(
            [port, "select", "--show", "python3"],
            capture_output=True,
            text=True,
        )
        # if the query failed or no version is selected
        if result.returncode != 0 or "none" in result.stdout:
            # make a channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line("no python3 version selected in MacPorts")
            error.line("select one and retry, e.g.:")
            error.line("  sudo port select python3 python312")
            # flush
            error.log()
            # bail
            return 1
        # parse the selected version name e.g. "python312" -> tag "312", version "3.12"
        match = re.search(r"python(\d)(\d+)", result.stdout)
        # if we couldn't parse it
        if not match:
            # make a channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line(
                "could not parse the selected python3 version from 'port select'"
            )
            error.line(f"output: {result.stdout.strip()}")
            # flush
            error.log()
            # bail
            return 1
        # reconstruct the version tag and the interpreter path
        pyTag = f"{match.group(1)}{match.group(2)}"
        pyVersion = f"{match.group(1)}.{match.group(2)}"
        python = prefix / "bin" / f"python{pyVersion}"
        # log our starting state
        channel.line("building macports package database")
        channel.indent()
        channel.line(f"port: {port}")
        channel.line(f"prefix: {prefix}")
        channel.line(f"python: {python}")
        channel.line(f"db: {db}")
        channel.outdent()
        channel.log()
        # query the installed ports
        result = subprocess.run(
            [port, "installed"],
            capture_output=True,
            text=True,
        )
        # if the query failed
        if result.returncode != 0:
            # make a channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line(f"failed to query installed ports: {result.stderr.strip()}")
            # flush
            error.log()
            # bail
            return 1
        # parse active ports; each active line ends with "(active)"
        installed = set()
        for line in result.stdout.splitlines():
            # strip leading whitespace
            line = line.strip()
            # only active ports
            if line.endswith("(active)"):
                # the port name is the first token
                installed.add(line.split()[0])
        # the mapping from mm extern name to macports port name(s); try names in order;
        # python-versioned ports use {pyTag} e.g. "312" for python 3.12
        packages = {
            "cantera": ["cantera"],
            "catch2": ["catch2"],
            "cgal": ["cgal5", "cgal"],
            "cspice": ["cspice"],
            "eigen": ["eigen3"],
            "fftw": ["fftw-3"],
            "fmt": ["libfmt"],
            "gdal": ["gdal"],
            "geotiff": ["libgeotiff"],
            "gmsh": ["gmsh"],
            "gsl": ["gsl"],
            "gtest": ["googletest"],
            "hdf5": ["hdf5"],
            "kokkos": ["kokkos"],
            "libpq": ["libpq"],
            "metis": ["metis5", "metis"],
            "mpi": ["openmpi", "mpich"],
            "numpy": [f"py{pyTag}-numpy"],
            "openblas": ["OpenBLAS"],
            "parmetis": ["parmetis"],
            "petsc": ["petsc"],
            "proj": ["proj"],
            "pybind11": [f"py{pyTag}-pybind11"],
            "python": [f"python{pyTag}"],
            "slepc": ["slepc"],
            "sundials": ["sundials"],
            "vtk": ["vtk9", "vtk"],
            "yaml": ["libyaml"],
            "yaml-cpp": ["yaml-cpp"],
        }
        # collect the packages that are present in this installation
        found = {}
        for name, candidates in packages.items():
            for candidate in candidates:
                if candidate in installed:
                    found[name] = candidate
                    break
        # report what we found
        channel.line(f"found {len(found)} of {len(packages)} supported packages")
        channel.indent()
        for name, candidate in sorted(found.items()):
            channel.line(f"{name}  (macports: {candidate})")
        channel.outdent()
        channel.log()
        # open the database file
        with open(db, "w") as f:
            # the emacs mode line
            print("# -*- Makefile -*-", file=f)
            # identification
            print("# macports package database", file=f)
            # provenance
            print("# generated by: mm --pkgdb=macports --setup", file=f)
            # the agent and prefix
            print(f"# port: {port}", file=f)
            print(f"# prefix: {prefix}", file=f)
            # blank line before the prefix declaration
            print(file=f)
            # the root of the MacPorts installation; factored out so all {.dir} entries track it
            print(f"macports.prefix := {prefix}", file=f)
            # blank line before package entries
            print(file=f)
            # write an entry for each found package in alphabetical order
            for name in sorted(found):
                # get the macports port name
                candidate = found[name]
                # a comment line showing the mm name and macports port name
                print(f"# {name}  (macports: {candidate})", file=f)
                # mpi needs its flavor to select the right library names
                if name == "mpi":
                    print(f"mpi.dir ?= $(macports.prefix)", file=f)
                    print(f"mpi.flavor ?= {candidate}", file=f)
                # numpy headers live under site-packages/numpy/core, not the macports prefix
                elif name == "numpy":
                    includePath = self._queryPythonExpression(
                        "import numpy; print(numpy.get_include())",
                        python=python,
                    )
                    if includePath:
                        numpyCore = pyre.primitives.path(includePath).parent
                        try:
                            relativePath = numpyCore.relativeTo(prefix)
                            print(
                                f"numpy.dir ?= $(macports.prefix)/{relativePath}",
                                file=f,
                            )
                        except ValueError:
                            print(f"numpy.dir ?= {numpyCore}", file=f)
                    else:
                        print(f"numpy.dir ?= $(macports.prefix)", file=f)
                # pybind11 headers also live under site-packages
                elif name == "pybind11":
                    includePath = self._queryPythonExpression(
                        "import pybind11; print(pybind11.get_include())",
                        python=python,
                    )
                    if includePath:
                        pybind11Root = pyre.primitives.path(includePath).parent
                        try:
                            relativePath = pybind11Root.relativeTo(prefix)
                            print(
                                f"pybind11.dir ?= $(macports.prefix)/{relativePath}",
                                file=f,
                            )
                        except ValueError:
                            print(f"pybind11.dir ?= {pybind11Root}", file=f)
                    else:
                        print(f"pybind11.dir ?= $(macports.prefix)", file=f)
                # python version is major.minor only, as used in filesystem paths
                elif name == "python":
                    print(f"python.version ?= {pyVersion}", file=f)
                    print(f"python.dir ?= $(macports.prefix)", file=f)
                # all other packages anchor to the macports prefix
                else:
                    print(f"{name}.dir ?= $(macports.prefix)", file=f)
                # blank line after each entry
                print(file=f)
        # all done
        return 0

    def _buildDpkgPackageDatabase(self, db):
        """
        Interrogate the dpkg package manager and write a package database
        """
        # grab a channel
        channel = journal.info("mm.pkgdb")
        # dpkg-query is always present on Debian/Ubuntu
        dpkg = shutil.which("dpkg-query")
        # if not found, we're not on a dpkg-based system
        if not dpkg:
            # make a channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line("could not find 'dpkg-query'")
            error.line("make sure you are on a Debian/Ubuntu system")
            # flush
            error.log()
            # bail
            return 1
        # the dpkg prefix is always /usr
        prefix = pyre.primitives.path("/usr")
        # query the Python interpreter for the correct package installation directory
        platlib = self._queryPythonExpression(
            "import sysconfig; print(sysconfig.get_path('platlib'))"
        )
        # if the query failed we can't reliably determine where to put python packages
        if not platlib:
            # make a channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line("could not determine the python package installation directory")
            error.line("make sure python3 is installed and on your PATH")
            # flush
            error.log()
            # bail
            return 1
        # make the platlib path relative to the prefix
        try:
            pycPrefix = pyre.primitives.path(platlib).relativeTo(prefix)
        # if it's not under /usr, use it as-is
        except ValueError:
            pycPrefix = pyre.primitives.path(platlib)
        # log our starting state
        channel.line("building dpkg package database")
        channel.indent()
        channel.line(f"dpkg-query: {dpkg}")
        channel.line(f"prefix: {prefix}")
        channel.line(f"python packages: {pycPrefix}")
        channel.line(f"db: {db}")
        channel.outdent()
        channel.log()
        # query all installed packages with their versions and status
        result = subprocess.run(
            [dpkg, "-W", "-f=${Package}\t${Version}\t${db:Status-Status}\n"],
            capture_output=True,
            text=True,
        )
        # if the query failed
        if result.returncode != 0:
            # make a channel
            error = journal.error("mm.pkgdb")
            # complain
            error.line(f"failed to query installed packages: {result.stderr.strip()}")
            # flush
            error.log()
            # bail
            return 1
        # build an index of installed packages keyed by name
        installed = {}
        for line in result.stdout.splitlines():
            # split into package, version, status
            parts = line.split("\t")
            # skip malformed lines
            if len(parts) != 3:
                continue
            name, version, status = parts
            # only count fully installed packages
            if status.strip() == "installed":
                installed[name] = version
        # the mapping from mm extern name to dpkg package name(s); try names in order
        packages = {
            "cantera": ["libcantera-dev"],
            # libcatch2-dev ships v3 with libraries on Ubuntu 25.10+ / Debian trixie+
            "catch2": ["libcatch2-dev"],
            "cgal": ["libcgal-dev"],
            "cspice": ["libcspice-dev"],
            "eigen": ["libeigen3-dev"],
            "fftw": ["libfftw3-dev"],
            "fmt": ["libfmt-dev"],
            "gdal": ["libgdal-dev"],
            "geotiff": ["libgeotiff-dev"],
            "gmsh": ["gmsh"],
            "gsl": ["libgsl-dev"],
            "gtest": ["libgtest-dev"],
            "hdf5": ["libhdf5-dev"],
            "kokkos": ["libkokkos-dev"],
            "libpq": ["libpq-dev"],
            "metis": ["libmetis-dev"],
            "mpi": ["libopenmpi-dev", "libmpich-dev"],
            "numpy": ["python3-numpy"],
            "openblas": ["libopenblas-dev"],
            "parmetis": ["libparmetis-dev"],
            "petsc": ["petsc-dev"],
            "proj": ["libproj-dev"],
            "pybind11": ["pybind11-dev"],
            "python": ["python3"],
            "slepc": ["slepc-dev"],
            "sundials": ["libsundials-dev"],
            "vtk": ["libvtk9-dev", "libvtk7-dev"],
            "yaml": ["libyaml-dev"],
            "yaml-cpp": ["libyaml-cpp-dev"],
        }
        # collect the packages present on this system
        found = {}
        for name, candidates in packages.items():
            for candidate in candidates:
                if candidate in installed:
                    found[name] = (candidate, installed[candidate])
                    break
        # cuda is a capability: present only if the assets needed to compile and link cuda
        # code are installed and locatable; {dpkg -L} is used to verify and place them
        cuda = self._emitDpkgCuda(dpkg, installed, prefix)
        # report what we found
        channel.line(f"found {len(found)} of {len(packages)} supported packages")
        channel.indent()
        for name, (candidate, version) in sorted(found.items()):
            channel.line(f"{name}: {version}  (dpkg: {candidate})")
        # and cuda, if it cleared the capability check
        if cuda:
            channel.line(f"cuda: {cuda[0]}  (capability verified)")
        channel.outdent()
        channel.log()
        # open the database file
        with open(db, "w") as f:
            # the emacs mode line
            print("# -*- Makefile -*-", file=f)
            # identification
            print("# dpkg package database", file=f)
            # provenance
            print("# generated by: mm --pkgdb=dpkg --setup", file=f)
            print(f"# dpkg-query: {dpkg}", file=f)
            print(f"# prefix: {prefix}", file=f)
            # blank line before the prefix declaration
            print(file=f)
            # the system prefix; factored out so all {.dir} entries track it
            print(f"dpkg.prefix := {prefix}", file=f)
            # blank line before package entries
            print(file=f)
            # write an entry for each found package in alphabetical order
            for name in sorted(found):
                candidate, version = found[name]
                # a comment line showing the mm name, version, and dpkg package name
                print(f"# {name}: {version}  (dpkg: {candidate})", file=f)
                # python version is major.minor only
                if name == "python":
                    pyVersion = self._queryPythonExpression(
                        "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
                    )
                    if pyVersion:
                        print(f"python.version ?= {pyVersion}", file=f)
                    print(f"python.dir ?= $(dpkg.prefix)", file=f)
                # mpi needs its flavor to select the right library names
                elif name == "mpi":
                    print(f"mpi.dir ?= $(dpkg.prefix)", file=f)
                    flavor = "openmpi" if "openmpi" in candidate else "mpich"
                    print(f"mpi.flavor ?= {flavor}", file=f)
                # numpy headers live under the python package directory
                elif name == "numpy":
                    includePath = self._queryPythonExpression(
                        "import numpy; print(numpy.get_include())"
                    )
                    if includePath:
                        numpyCore = pyre.primitives.path(includePath).parent
                        try:
                            relativePath = numpyCore.relativeTo(prefix)
                            print(f"numpy.dir ?= $(dpkg.prefix)/{relativePath}", file=f)
                        except ValueError:
                            print(f"numpy.dir ?= {numpyCore}", file=f)
                    else:
                        print(f"numpy.dir ?= $(dpkg.prefix)", file=f)
                # pybind11 headers also live under the python package directory
                elif name == "pybind11":
                    includePath = self._queryPythonExpression(
                        "import pybind11; print(pybind11.get_include())"
                    )
                    if includePath:
                        pybind11Root = pyre.primitives.path(includePath).parent
                        try:
                            relativePath = pybind11Root.relativeTo(prefix)
                            print(
                                f"pybind11.dir ?= $(dpkg.prefix)/{relativePath}", file=f
                            )
                        except ValueError:
                            print(f"pybind11.dir ?= {pybind11Root}", file=f)
                    else:
                        print(f"pybind11.dir ?= $(dpkg.prefix)", file=f)
                # all other packages anchor to the dpkg prefix
                else:
                    print(f"{name}.dir ?= $(dpkg.prefix)", file=f)
                # version for packages whose init.mm has version-dependent logic
                print(f"{name}.version ?= {version}", file=f)
                # blank line after each entry
                print(file=f)
            # finally the cuda capability block, when cuda can actually be built against
            if cuda:
                # the ready-to-write makefile lines
                _, lines = cuda
                # emit each
                for line in lines:
                    print(line, file=f)
                # blank line after the block
                print(file=f)
        # all done
        return 0

    def _dpkgFiles(self, dpkg, package):
        """
        Return the absolute paths of the files installed by a dpkg {package}, via {dpkg -L}; an
        empty list if the package is unknown to dpkg
        """
        # ask for the package contents
        result = subprocess.run([dpkg, "-L", package], capture_output=True, text=True)
        # if the query failed, treat the package as having no files
        if result.returncode != 0:
            return []
        # each non-empty line is an absolute path owned by the package
        return [
            pyre.primitives.path(line) for line in result.stdout.splitlines() if line
        ]

    def _dpkgAnchor(self, path, prefix):
        """
        Render {path} relative to {dpkg.prefix} when it lives under it, otherwise as an absolute
        path; keeps the database tidy without assuming a layout
        """
        # the prefix itself collapses to the bare reference
        if str(path) == str(prefix):
            return "$(dpkg.prefix)"
        # express it under the prefix when possible
        try:
            return f"$(dpkg.prefix)/{path.relativeTo(prefix)}"
        # if it isn't under the prefix (e.g. /usr/local/cuda lives under /usr, but a custom
        # toolkit might not), keep it absolute
        except ValueError:
            return str(path)

    def _emitDpkgCuda(self, dpkg, installed, prefix):
        """
        Resolve cuda as a capability under dpkg: usable only if the compiler (nvcc), the runtime
        headers (cuda.h) and the runtime library (libcudart) are all installed and locatable.
        Debian/Ubuntu ships cuda in two very different layouts — the distro {nvidia-cuda-toolkit}
        (headers in /usr/include, multiarch libs) and the NVIDIA apt repo ({cuda-nvcc-X-Y} etc.,
        under /usr/local/cuda-X.Y with a {targets/<arch>} sysroot) — so the include and library
        directories are read from {dpkg -L} rather than assumed. A partial install is reported
        and cuda is omitted. Returns {(version, lines)}, or None if cuda is absent or unusable
        """
        # the installed packages that look cuda-related; capability is verified at the file
        # level, so the exact (version-suffixed) package names need not be known ahead of time
        candidates = [
            name
            for name in installed
            if name.startswith(("cuda-", "nvidia-cuda")) or "cudart" in name
        ]
        # if nothing cuda-ish is installed, cuda is simply absent
        if not candidates:
            return None
        # gather the file manifests of all the candidates once
        files = []
        for package in candidates:
            files.extend(self._dpkgFiles(dpkg, package))
        # locate the three assets that prove we can compile and link cuda code
        nvcc = next((path for path in files if path.name == "nvcc"), None)
        header = next((path for path in files if path.name == "cuda.h"), None)
        library = next(
            (path for path in files if path.name.startswith("libcudart.so")), None
        )
        # note which, if any, are missing
        missing = []
        if not nvcc:
            missing.append("nvcc")
        if not header:
            missing.append("cuda.h")
        if not library:
            missing.append("libcudart")
        # if any asset is missing, this is a systemic problem the user should fix; warn and
        # leave cuda out of the database rather than let the compiler or linker fail later
        if missing:
            # a warning channel
            warning = journal.warning("mm.pkgdb")
            # what is wrong
            warning.line("cuda is partially installed")
            # which assets are missing
            warning.line(f"missing: {', '.join(missing)}")
            # the consequence
            warning.line("cuda support disabled")
            # flush
            warning.log()
            # not usable
            return None
        # the include directory holds cuda.h; the toolkit root is its parent, which makes the
        # {cuda/init.mm} incpath default ({cuda.dir}/include plus the cccl wildcard) resolve
        cudaDir = header.parent.parent
        # the library directory is wherever libcudart actually landed (lib, lib64 or multiarch),
        # so it always overrides init.mm's {lib64} default
        libdir = library.parent
        # the version: a {cuda-X.Y} segment in the asset path (NVIDIA apt layout), else the
        # distro toolkit package version, trimmed to major.minor
        match = re.search(r"cuda-(\d+\.\d+)", str(header))
        if match:
            version = match.group(1)
        else:
            # the distro toolkit package carries the version
            pkgver = next(
                (
                    installed[pkg]
                    for pkg in ("nvidia-cuda-toolkit", "nvidia-cuda-dev")
                    if pkg in installed
                ),
                None,
            )
            # trim it, or admit we don't know
            version = self._condaMajorMinor(pkgver) if pkgver else "unknown"
        # the ready-to-write makefile lines
        lines = [
            f"# cuda: {version}  (dpkg: nvcc + cuda.h + libcudart located via dpkg -L)",
            f"cuda.version ?= {version}",
            f"cuda.dir ?= {self._dpkgAnchor(cudaDir, prefix)}",
            f"cuda.libpath ?= {self._dpkgAnchor(libdir, prefix)}",
        ]
        # hand back the version (for the report) and the lines
        return version, lines

    def _queryPythonExpression(self, expression, *, python=sys.executable):
        """
        Evaluate a python expression in the given interpreter and return its stdout,
        or None if the evaluation fails
        """
        # run the expression in the requested interpreter
        result = subprocess.run(
            [str(python), "-c", expression],
            capture_output=True,
            text=True,
        )
        # return the output on success, None on failure
        return result.stdout.strip() if result.returncode == 0 else None

    def _condaBldroot(self):
        """
        Assemble the staging area path for a {conda} build; the environment name is always
        included to keep builds for different environments from colliding
        """
        # start with the user's opinion, falling back to the project tree
        bldroot = self.bldroot or (self._root / "builds")
        # always fold in the environment name; it plays the role that {tag} plays in dev mode
        bldroot /= self.environment
        # append the build variant tag and return it
        return bldroot / self._bldTag

    def _condaAgent(self):
        """
        Resolve the conda/mamba/micromamba executable. Installers expose the agent as a shell
        function that finds the real binary through {$MAMBA_EXE} (micromamba, mamba) or
        {$CONDA_EXE} (conda), so the binary is usually not on {PATH}; consult those exported
        locations first, then fall back to a {PATH} search
        """
        # the installer-exported binary locations, in order of preference
        for variable in ("MAMBA_EXE", "CONDA_EXE"):
            # look it up
            executable = os.environ.get(variable)
            # if it's set and points at something runnable
            if executable and os.access(executable, os.X_OK):
                # use it
                return executable
        # otherwise fall back to a {PATH} search, preferring micromamba
        return (
            shutil.which("micromamba") or shutil.which("mamba") or shutil.which("conda")
        )

    def _condaPrefix(self):
        """
        Resolve the installation prefix for a {conda} build; the prefix is the root of the
        named conda environment, and {pycPrefix} is set to the environment's site-packages
        """
        # get the environment name
        envName = self.environment
        # find the conda agent
        agent = self._condaAgent()
        # if none found
        if not agent:
            # make a channel
            channel = journal.error("mm.conda")
            # complain
            channel.line("no conda agent found")
            channel.line(
                "set $MAMBA_EXE or $CONDA_EXE, or put micromamba/mamba/conda on PATH"
            )
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return None
        # ask the agent for all known environments
        result = subprocess.run(
            [agent, "env", "list", "--json"],
            capture_output=True,
            text=True,
        )
        # if the query failed
        if result.returncode != 0:
            # make a channel
            channel = journal.error("mm.conda")
            # complain
            channel.line(f"failed to query conda environments")
            channel.line(f"agent: {agent}")
            channel.line(result.stderr.strip())
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return None
        # parse the result; each entry is a path whose basename is the environment name
        envs = json.loads(result.stdout).get("envs", [])
        # go through the prefixes
        for prefix in envs:
            # convert them to paths
            prefix = pyre.primitives.path(prefix)
            # if it's the target environment
            if prefix.name == envName:
                # we've found it
                break
        # otherwise
        else:
            # make a channel
            channel = journal.error("mm.conda")
            # complain
            channel.line(f"conda environment '{envName}' not found")
            channel.line(
                f"known environments: {', '.join(pyre.primitives.path(p).name for p in envs)}"
            )
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return None

        # verify the prefix actually exists on disk
        if not prefix.isDirectory():
            # make a channel
            channel = journal.error("mm.conda")
            # complain
            channel.line(f"conda environment '{envName}' prefix does not exist")
            channel.line(f"expected: {prefix}")
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return None
        # query the Python version from the environment's own interpreter
        version = self._queryPythonExpression(
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
            python=prefix / "bin" / "python",
        )
        # if the query failed
        if not version:
            # make a channel
            channel = journal.error("mm.conda")
            # complain
            channel.line(f"unable to determine the version of the python interpreter")
            channel.line(f"in the '{envName}' conda environment")
            channel.line(f"so i don't have a place to deposit pythonpackages")
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return None
        # otherwise, set the python package prefix to the site-packages location
        self._pycPrefix = pyre.primitives.path(f"lib/python{version}/site-packages")
        # all done
        return prefix

    def _macportsBldroot(self):
        """
        Assemble the staging area path for a {macports} build; a fixed {macports} segment
        discriminates these builds from dev builds in the same bldroot tree
        """
        # start with the user's opinion, falling back to the project tree
        bldroot = self.bldroot or (self._root / "builds")
        # fold in a fixed discriminator and the build variant tag
        return bldroot / "macports" / self._bldTag

    def _macportsPrefix(self):
        """
        Resolve the installation prefix for a {macports} build; the prefix is the MacPorts
        root, write access is verified, and {pycPrefix} is set from the selected python3
        """
        # find the port executable
        port = shutil.which("port")
        # if not found, macports is not installed
        if not port:
            # make a channel
            channel = journal.error("mm.macports")
            # complain
            channel.line("could not find the 'port' executable")
            channel.line("make sure MacPorts is installed and 'port' is on your PATH")
            # flush
            channel.log()
            # bail
            return None
        # the MacPorts prefix is the grandparent of the {port} executable
        prefix = pyre.primitives.path(port).parent.parent
        # warn that installing into the MacPorts tree requires elevated privileges;
        # make will fail loudly at the install step if mm is not run with sudo
        if not os.access(str(prefix), os.W_OK):
            # make a channel
            channel = journal.warning("mm.macports")
            # warn
            channel.line(f"no write access to the MacPorts prefix '{prefix}'")
            channel.line(
                "installing will fail unless mm is run with elevated privileges:"
            )
            channel.line("  sudo mm")
            # flush
            channel.log()
        # ask port which python3 version is currently selected
        result = subprocess.run(
            [port, "select", "--show", "python3"],
            capture_output=True,
            text=True,
        )
        # if the query failed or no version is selected
        if result.returncode != 0 or "none" in result.stdout:
            # make a channel
            channel = journal.error("mm.macports")
            # complain
            channel.line("no python3 version selected in MacPorts")
            channel.line("select one and retry, e.g.:")
            channel.line("  sudo port select python3 python312")
            # flush
            channel.log()
            # bail
            return None
        # parse the selected version name, e.g. "python312" -> "3.12"
        match = re.search(r"python(\d)(\d+)", result.stdout)
        # if we couldn't parse it
        if not match:
            # make a channel
            channel = journal.error("mm.macports")
            # complain
            channel.line(
                "could not parse the selected python3 version from 'port select'"
            )
            channel.line(f"output: {result.stdout.strip()}")
            # flush
            channel.log()
            # bail
            return None
        # reconstruct the version string and the interpreter path
        pyVersion = f"{match.group(1)}.{match.group(2)}"
        python = prefix / "bin" / f"python{pyVersion}"
        # verify the interpreter actually exists
        if not python.exists():
            # make a channel
            channel = journal.error("mm.macports")
            # complain
            channel.line(f"expected python interpreter not found: {python}")
            channel.line(
                "check your MacPorts python3 selection with 'port select --show python3'"
            )
            # flush
            channel.log()
            # bail
            return None
        # query the site-packages path from the interpreter itself
        version = self._queryPythonExpression(
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
            python=python,
        )
        # if the query succeeded, set the python package prefix to the site-packages location
        if version:
            self._pycPrefix = pyre.primitives.path(f"lib/python{version}/site-packages")
        # all done
        return prefix

    def _ubuntuBldroot(self):
        """
        Assemble the staging area path for an {ubuntu} build; a fixed {ubuntu} segment
        discriminates these builds from dev builds in the same bldroot tree
        """
        # start with the user's opinion, falling back to the project tree
        bldroot = self.bldroot or (self._root / "builds")
        # fold in a fixed discriminator and the build variant tag
        return bldroot / "ubuntu" / self._bldTag

    def _ubuntuPrefix(self):
        """
        Resolve the installation prefix for an {ubuntu} build; defaults to {/usr} so builds
        integrate with the system layout in docker containers; {pycPrefix} is derived from
        the system Python's {sysconfig} to handle Debian's {dist-packages} convention
        """
        # default to the system prefix; the user can override with --prefix
        prefix = self.prefix or pyre.primitives.path("/usr")
        # query the system Python for the correct package installation directory
        platlib = self._queryPythonExpression(
            "import sysconfig; print(sysconfig.get_path('platlib'))"
        )
        # if the query succeeded, make {platlib} relative to the prefix
        if platlib:
            try:
                # strip the prefix to get the relative path (e.g. lib/python3.12/dist-packages)
                self._pycPrefix = pyre.primitives.path(platlib).relativeTo(prefix)
            # if {platlib} isn't under the prefix, something is unusual; use it as-is
            except ValueError:
                self._pycPrefix = pyre.primitives.path(platlib)
        # all done
        return prefix

    def _devBldroot(self):
        """
        Assemble the staging area path for a {dev} build
        """
        # {dev} is the bare local layout, so it injects no mode discriminator
        return self._localBldroot()

    def _releaseBldroot(self):
        """
        Assemble the staging area path for a {release} build
        """
        # {release} is a local build that lives under its own discriminator so its
        # artifacts never mix with the {dev} ones
        return self._localBldroot(discriminator="release")

    def _localBldroot(self, *, discriminator=None):
        """
        Assemble the staging area path for a local ({dev} or {release}) build
        """
        # start with the user's opinion, falling back to the project tree
        bldroot = self.bldroot or (self._root / "builds")
        # a non-{dev} local mode
        if discriminator:
            # keeps its products apart by carrying a discriminator
            bldroot /= discriminator
        # get the compiler suite
        suite = self._suite
        # if it is set
        if suite:
            # add it to the path to separate ABI-incompatible builds
            bldroot /= suite
        # get the branch tag
        tag = self.tag
        # if it is set, use it to discriminate the build context
        if tag:
            # include the build variant so builds for different targets land separately
            return bldroot / tag / self._bldTag
        # otherwise, append just the build variant tag
        return bldroot / self._bldTag

    def _devPrefix(self):
        """
        Assemble the installation path for a {dev} build
        """
        # {dev} is the bare local layout, so it injects no mode discriminator
        return self._localPrefix()

    def _releasePrefix(self):
        """
        Assemble the installation path for a {release} build
        """
        # {release} installs under its own discriminator so it never mixes with {dev}
        return self._localPrefix(discriminator="release")

    def _localPrefix(self, *, discriminator=None):
        """
        Assemble the installation path for a local ({dev} or {release}) build
        """
        # start with the user's opinion, falling back to the project tree
        prefix = self.prefix or (self._root / "products")
        # a non-{dev} local mode
        if discriminator:
            # keeps its installs apart by carrying a discriminator
            prefix /= discriminator
        # get the compiler suite
        suite = self._suite
        # if a compiler suite is set
        if suite:
            # add it to the path to separate ABI-incompatible installs
            prefix /= suite
        # get the tag
        tag = self.tag
        # if a branch tag is set, use it to discriminate the build context
        if tag:
            # include the build variant so installs for different targets land separately
            return prefix / tag / self._bldTag
        # otherwise, use the default location
        return prefix / self._bldTag


# end of file
