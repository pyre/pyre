# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved

# externals
import os
import re
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
    copyright 1998-2003 all rights reserved
    """

    # project configuration
    version = pyre.properties.str()
    version.default = None
    version.doc = "the project version; try to deduce it, if not set"

    prefix = pyre.properties.path()
    prefix.default = None
    prefix.doc = "the path to the installation directory"

    bldroot = pyre.properties.path()
    bldroot.default = None
    bldroot.doc = "the path to the intermediate build products"

    target = pyre.properties.strings()
    target.default = ["debug", "shared"]
    target.doc = "the list of target variants to build"

    compilers = pyre.properties.strings()
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
    LD_LIBRARY_PATH = pyre.properties.envpath(variable="LD_LIBRARY_PATH")
    PYTHONPATH = pyre.properties.envpath(variable="PYTHONPATH")
    MM_INCLUDES = pyre.properties.envpath(variable="MM_INCLUDES")
    MM_LIBPATH = pyre.properties.envpath(variable="MM_LIBPATH")

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
        # otherwise, launch the build
        return self.launch()

    # metamethods
    def __init__(self, home, **kwds):
        # chain up
        super().__init__(**kwds)
        # N.B.:
        #   the {explore} step could happen here
        #   there were some corner cases that were raising exceptions
        #   investigate and rethink
        # get the current user
        self.user = self.pyre_executive.user
        # record the mm installation directory
        self._home = home
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
        # the path to the intermediate products of the build
        self._bldroot = None
        # the target identification
        self._bldTarget = None
        self._bldVariants = None
        self._bldTag = None
        # and the install directory
        self._prefix = None
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
            "LD_LIBRARY_PATH": os.pathsep.join(map(str, self.LD_LIBRARY_PATH)),
            "PYTHONPATH": os.pathsep.join(map(str, self.PYTHONPATH)),
            "MM_INCLUDES": os.pathsep.join(map(str, self.MM_INCLUDES)),
            "MM_LIBPATH": os.pathsep.join(map(str, self.MM_LIBPATH)),
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
        # get the name of the package database manager
        name = self.pkgdb
        # get the temporary staging area
        stage = self.locateBuildRoot()
        # construct the build tag
        _, _, tag = self.assembleBuildTarget()
        # the location of the package database
        db = stage / tag / f"pkg-{name}.db"
        # if this the adhoc manager
        if name == "adhoc":
            # assume that the user already has setup a custom package database
            # in some configuration file, as is current mm practice; just create the db file
            open(db, "w")
            # and move on
            return 0

        #
        # THIS SECTION IS CURRENTLY UNDER DEVELOPMENT
        #

        # grab a channel
        channel = journal.info("mm.pkgdb")
        # show me
        channel.line(f"setting up the package database")
        channel.indent()
        channel.line(f"package manager: {name}")
        channel.line(f"db: {db}")
        channel.outdent()
        # flush
        channel.log()

        hdf5 = pyre.externals.hdf5().default()
        # show me
        channel.line(f"hdf5:")
        channel.indent()
        channel.line(f"version: {hdf5.version}")
        channel.line(f"inc: {', '.join(map(str, hdf5.incdir))}")
        channel.line(f"lib: {', '.join(map(str, hdf5.libdir))}")
        channel.outdent()
        # flush
        channel.log()

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
        # figure out where to put the intermediate products of the build
        self._bldroot = self.locateBuildRoot()
        # construct the build tag
        self._bldTarget, self._bldVariants, self._bldTag = self.assembleBuildTarget()
        # figure out the install directory
        self._prefix = self.locatePrefix()
        # adjust my envpaths with the build configuration
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
            channel.line(f"check your setting for my 'merlin' property")
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
                    channel.line(f"you need GNU make 4.2.1 or higher")
                    channel.outdent()
                    channel.line(f"check your setting for my 'make' property")
                    # flush
                    channel.log()
                    # and bail, just in case errors aren't fatal
                    return
                # get the version info
                major, minor, micro = map(int, match.groups(default=0))
                # we need 4.2.1 or higher
                if (major, minor, micro) < (4, 2, 1):
                    # we have a problem
                    channel = journal.error("mm.gnu")
                    # complain
                    channel.line(f"your version of GNU make is too old")
                    channel.line(f"while verifying my installation")
                    channel.indent()
                    channel.line(f"you need GNU make 4.2.1 or higher")
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
        # get the user's opinion
        bldroot = self.bldroot
        # if there is one
        if bldroot is not None:
            # we are done
            return bldroot
        # otherwise, put things in a subdirectory of the project root
        return self._root / "builds"

    def assembleBuildTarget(self):
        """
        Construct the build tag that used to indicate platform and build characteristics
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

    def locatePrefix(self):
        """
        Figure out where to put the build products
        """
        # get the user's opinion
        prefix = self.prefix
        # if there is one
        if prefix is not None:
            # we are done
            return prefix
        # otherwise, put things in a subdirectory of the project root
        return self._root / "products"

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
        self.LD_LIBRARY_PATH = self.inject(
            var=self.LD_LIBRARY_PATH, path=(prefix / "lib")
        )
        # the python path
        self.PYTHONPATH = self.inject(var=self.PYTHONPATH, path=(prefix / "packages"))
        # configure mm
        # update the compiler include path
        self.MM_INCLUDES = self.inject(var=self.MM_INCLUDES, path=(prefix / "include"))
        self.MM_INCLUDES = self.inject(var=self.MM_INCLUDES, path=self.portinfo)
        # update the linker library path
        self.MM_LIBPATH = self.inject(var=self.MM_LIBPATH, path=(prefix / "lib"))
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
        yield f"--jobs={self.computeSlots()}"
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
        yield f"builder.dest.pyc={self._prefix / self.pycPrefix}/"
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
        # and email
        yield f"user.email={user.email}"
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

    def configureBuilder(self):
        """
        Configure the engine
        """
        # record how mm was invoked
        yield f"mm={sys.executable} {__file__}"
        # the version
        yield f"mm.version={self._version}"
        # the mm installation location
        yield f"mm.home={self._home}"
        # the path to the top level makefile
        yield f"mm.merlin={self._makefile}"
        # the location of the built-in package database
        yield f"mm.extern={self.engine / 'extern'}"
        # the package manager
        yield f"mm.pkgdb={self.pkgdb}"
        # the list of compilers
        yield f"mm.compilers={' '.join(self.compilers)}"
        # form the list of paths with headers to add to the compiler command line
        yield f"mm.incpath={' '.join(map(str, self.MM_INCLUDES))}"
        # form the list of paths with headers to add to the compiler command line
        yield f"mm.libpath={' '.join(map(str, self.MM_LIBPATH))}"
        # indicate whether the output should be colorized
        yield f"mm.color={'' if self.color else 'no'}"
        # and the palette to use
        yield f"mm.palette={self.palette}"
        # all done
        return

    # framework hooks
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
        Ensure {path} is in {var}
        """
        # if {path} is already in {var}
        if path in var:
            # return it unchanged
            yield from var
            # and done
        # otherwise, add {path} to the pile
        yield path
        # followed by the original list
        yield from var
        # and done
        return

    def computeSlots(self):
        """
        Choose the number of jobs tha GNU make will execute in parallel
        """
        # if the user doesn't want any parallelism
        if self.serial:
            # execute only one recipe at a tie
            return 1
        # get the user choice
        slots = self.slots
        # and the number of cores of the host on which mm is running
        # N.B.:
        #     that's not {self.host}, which is meant to be the machine we're building for
        cores = pyre.executive.host.cpus.cpus
        # clip it from below and default to as many slots as there are cores
        return max(1, cores if slots is None else slots)

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
            if int(ahead) == 0:
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

    # framework hooks
    def pyre_banner(self):
        """
        Generate the application banner
        """
        # sign on
        yield "  mm {}.{}.{} rev {}".format(*merlin.meta.version)
        # all done
        return

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


# bootstrap
if __name__ == "__main__":
    # instantiate the app
    app = Builder(name="mm")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
