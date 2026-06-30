# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# externals
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import typing
import urllib.error
import urllib.request

# the framework, imported straight out of this archive via {zipimport}
import journal
import pyre
import merlin

# the build strategies understood by {mm}; mirrors the {mode} trait validator in {merlin.shells.MM}
modes = ("dev", "release", "conda", "macports", "ubuntu")

# optional features and the external package each one needs; the core framework needs none
features = (
    ("h5 extension", "hdf5", ("h5c++", "h5cc")),
    ("postgres extension", "libpq", ("pg_config",)),
    ("mpi support", "mpi", ("mpic++", "mpicxx")),
    ("gsl support", "gsl", ("gsl-config",)),
    ("cuda support", "cuda", ("nvcc",)),
)


# the app
class Boot(pyre.application, family="pyre.applications.boot", namespace="boot"):
    """
    Fetch the pyre source that matches this archive and build it with the embedded {mm}
    """

    # user configurable state
    target = pyre.properties.path()
    target.default = None
    target.doc = "the directory to populate with the pyre source"

    source = pyre.properties.str()
    source.default = None
    source.doc = "the release tag to pull, or {head} for the tip; defaults to this archive's own tag"

    mode = pyre.properties.str(default="dev")
    mode.validators = pyre.constraints.isMember(*modes)
    mode.doc = "the strategy {mm} uses to lay out the build products"

    repo = pyre.properties.str(default="https://github.com/pyre/pyre")
    repo.doc = "the source repository to pull from"

    interactive = pyre.properties.bool(default=True)
    interactive.doc = "prompt for any choices left unset on the command line"

    # application obligations
    @pyre.export
    def main(self, *args, **kwds) -> int:
        """
        Walk the user through fetching the matching source and building it with {mm}
        """
        # figure out which release this archive was cut from
        tag, human = self.release()
        self.info.log(f"pyre bootstrapper — release {human} ({tag})")

        # settle which version to pull, defaulting to this archive's own tag
        self.source = self.pick(default=tag)
        # then where it should land and how to build it
        self.target = self.ask(
            question="where should I put the source",
            default=str(
                self.target or pyre.primitives.path.cwd() / f"pyre-{self.source}"
            ),
        )
        self.mode = self.ask(question="which build mode", default=self.mode)

        # resolve the destination once, now that it is final
        target = pyre.primitives.path(self.target).resolve()

        # explain what this machine can build before touching anything
        self.audit()

        # give the user a chance to back out
        if self.ask(question="proceed", default="yes").lower() not in ("y", "yes"):
            self.info.log("nothing done")
            return 0

        # stage the source, lend a hand with conda, then build
        self.stage(target=target)
        if self.mode == "conda":
            self.conda(target=target)
        self.build(target=target)

        # done
        self.info.log(f"pyre is built; the source lives in '{target}'")
        return 0

    # implementation details
    def release(self) -> typing.Tuple[str, str]:
        """
        Report the version this archive was cut from, as a {(tag, human)} pair
        """
        # unpack the embedded version stamp
        major, minor, micro, revision = pyre.meta.version
        # the git tag, and a friendly rendering
        return f"v{major}.{minor}.{micro}", f"{major}.{minor}.{micro} rev {revision}"

    def pick(self, *, default: str) -> str:
        """
        Settle on the version to pull: honor an explicit choice, else offer what GitHub publishes
        """
        # a value supplied on the command line wins outright
        if self.source:
            return self.source
        # in batch mode with nothing set, fall back to this archive's own tag
        if not self.interactive:
            return default
        # otherwise show what is actually available, newest first
        tags = self.catalog()
        if tags:
            shown = ", ".join(tags[:8])
            self.info.log(f"available releases: {shown}{' …' if len(tags) > 8 else ''}")
        # the development tip is always on offer alongside the published tags
        self.info.log("use a tag from the list, or 'head' for the tip of development")
        return self.ask(question="which version", default=default)

    def catalog(self) -> typing.List[str]:
        """
        Query GitHub for the published release tags, newest first; empty on any failure
        """
        # derive the API endpoint from the repository url
        slug = self.repo.rstrip("/").removeprefix("https://github.com/")
        url = f"https://api.github.com/repos/{slug}/releases"
        # ask politely, tolerating any network or rate-limit failure
        try:
            request = urllib.request.Request(
                url, headers={"Accept": "application/vnd.github+json"}
            )
            with urllib.request.urlopen(request) as istream:
                payload = json.load(istream)
        except (urllib.error.URLError, json.JSONDecodeError) as error:
            # a missing catalog is not fatal; the embedded tag still works
            self.warning.log(f"could not reach GitHub for the release list ({error})")
            return []
        # pull out the tag names, preserving GitHub's newest-first ordering
        return [release["tag_name"] for release in payload]

    def ask(self, *, question: str, default: str) -> str:
        """
        Prompt for a value when running interactively; otherwise accept {default} silently
        """
        # in batch mode the configured value stands as is
        if not self.interactive:
            return default
        # otherwise offer {default} and take whatever the user types
        reply = input(f"{question} [{default}]: ").strip()
        return reply or default

    def audit(self) -> None:
        """
        Probe the host for a toolchain and optional dependencies, explaining what is buildable
        """
        # narrate through a channel dedicated to this concern
        channel = journal.info("pyre.boot.audit")
        channel.line("checking what this machine can build:")

        # the core needs nothing but a C++ toolchain and the python development headers
        cxx = self.compiler()
        if cxx is None:
            channel.line(
                "  ✗ core framework — no C++ compiler found (set CXX or install one)"
            )
        else:
            channel.line(
                f"  ✓ core framework (pyre, journal, merlin + extensions) via {cxx}"
            )

        # every other feature is gated on an external package
        for name, package, commands in features:
            available = any(shutil.which(command) is not None for command in commands)
            mark = "✓" if available else "✗"
            note = "available" if available else f"needs {package}"
            channel.line(f"  {mark} {name} — {note}")

        # set expectations: a bare toolchain already yields a fully usable framework
        channel.line("")
        channel.line(
            "  the core builds with no extra packages; optional features light up"
        )
        channel.line("  automatically once their dependency is on your PATH")
        channel.log()

    def compiler(self) -> typing.Optional[str]:
        """
        Locate a C++ compiler, honoring {CXX} before falling back to the usual suspects
        """
        # prefer an explicit choice from the environment, then the common driver names
        for candidate in filter(None, (os.environ.get("CXX"), "c++", "g++", "clang++")):
            found = shutil.which(candidate)
            if found is not None:
                return found
        # nothing usable
        return None

    def stage(self, *, target: "pyre.primitives.path") -> None:
        """
        Populate {target} with the pyre source: a fresh checkout, or the chosen release tag
        """
        # refuse to clobber an existing, non-empty destination
        if target.exists() and any(target.contents):
            self.error.log(f"'{target}' already exists and is not empty")

        # pulling the tip of development
        if self.source == "head":
            # which requires git
            if shutil.which("git") is None:
                self.error.log(
                    "git is required to pull head; install it or choose a release"
                )
            self.info.log(f"cloning {self.repo} into '{target}'")
            # a full clone, so the user can actually work in the tree they just pulled
            outcome = subprocess.run(["git", "clone", self.repo, str(target)])
            if outcome.returncode != 0:
                self.error.log(f"git clone failed with status {outcome.returncode}")
            return

        # otherwise stage the tarball for the chosen tag
        url = f"{self.repo}/archive/refs/tags/{self.source}.tar.gz"
        self.info.log(f"downloading {url}")
        self.untar(url=url, target=target)

    def untar(self, *, url: str, target: "pyre.primitives.path") -> None:
        """
        Download the source tarball at {url} and unpack its single top-level tree into {target}
        """
        # work in a scratch directory that cleans itself up
        with tempfile.TemporaryDirectory() as scratch:
            archive = os.path.join(scratch, "source.tar.gz")
            # grab the bytes, turning a bad tag or a network hiccup into a clean error
            try:
                with urllib.request.urlopen(url=url) as istream, open(
                    archive, "wb"
                ) as ostream:
                    shutil.copyfileobj(istream, ostream)
            except urllib.error.URLError as error:
                self.error.log(f"failed to download {url}: {error}")
            # unpack it; {filter} keeps modern python from warning, and is harmless data hygiene
            with tarfile.open(archive) as tar:
                try:
                    tar.extractall(scratch, filter="data")
                except TypeError:
                    # {filter} predates this interpreter; fall back to the classic extraction
                    tar.extractall(scratch)
            # the github tarball wraps everything in a single {pyre-x.y.z} directory
            roots = [entry for entry in os.listdir(scratch) if entry != "source.tar.gz"]
            if len(roots) != 1:
                self.error.log(f"unexpected tarball layout: {roots}")
            # promote that directory to the destination the user picked
            shutil.move(os.path.join(scratch, roots[0]), str(target))

    def conda(self, *, target: "pyre.primitives.path") -> None:
        """
        Help the user line up a conda environment when building in conda mode
        """
        # conda has to be on the PATH for any of this to work
        if shutil.which("conda") is None:
            self.warning.log(
                "conda mode selected, but no 'conda' on your PATH; install miniforge"
            )
            return

        # an already-active environment is the happy path
        active = os.environ.get("CONDA_PREFIX")
        if active:
            self.info.log(f"building into the active conda environment at '{active}'")
            return

        # otherwise point the user at the environment file the repo ships, if any
        for relative in (
            ".conda/environment.yml",
            "etc/environment.yml",
            "environment.yml",
        ):
            spec = target / relative
            if spec.exists():
                self.info.log(
                    f"no environment active; create one with: conda env create -f {spec}"
                )
                return

        # no shipped spec; give generic guidance rather than guessing package names
        self.warning.log(
            "no conda environment is active; create and activate one before building"
        )

    def build(self, *, target: "pyre.primitives.path") -> None:
        """
        Drive the embedded {mm} builder against the freshly staged tree
        """
        # in a source checkout, the engine and portinfo headers sit beside the {bin} driver
        engine = target / "share" / "mm" / "make"
        portinfo = target / "include" / "mm"

        self.info.log(f"building pyre in '{self.mode}' mode from '{target}'")
        # {mm} keys off the project's local {.mm} configuration, so run from the tree root
        here = pyre.primitives.path.cwd()
        os.chdir(str(target))
        try:
            # instantiate the embedded builder, pointed at the staged engine
            app = merlin.shells.mm(
                name="mm", engine=engine, portinfo=portinfo, mode=self.mode
            )
            # and let it build the default target
            status = app.run()
        finally:
            # always return to where we started
            os.chdir(str(here))

        # surface a non-zero build status as a real failure
        if status != 0:
            self.error.log(f"the build exited with status {status}")


# bootstrap: this module is staged as the archive's {__main__.py}, so it is the entry point
if __name__ == "__main__":
    # instantiate the app
    app = Boot(name="pyre-boot")
    # launch it
    status = app.run()
    # share the exit code with the shell
    raise SystemExit(status)


# end of file
