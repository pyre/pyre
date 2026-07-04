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
import sys
import tarfile
import tempfile
import typing
import urllib.error
import urllib.request

# the framework, imported straight out of this archive via {zipimport}
import journal
import pyre

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

    branch = pyre.properties.str()
    branch.default = None
    branch.doc = "the branch to clone when building the bleeding edge; defaults to {main}"

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
        # find out which release this archive was cut from, so we can offer it as the default
        tag, human = self.release()
        # and greet the user with that provenance
        self.info.log(f"pyre bootstrapper — release {human} ({tag})")

        # settle what to build: a stable tag, or the tip of a development branch
        self.source = self.pick(default=tag)
        # decide where the source should land, defaulting to a sibling named for the choice
        self.target = self.ask(
            question="where should I put the source",
            default=str(
                self.target
                or pyre.primitives.path.cwd() / f"pyre-{self.branch or self.source}"
            ),
        )
        # and settle on the layout strategy {mm} will use
        self.mode = self.ask(question="which build mode", default=self.mode)

        # nail down the destination now that the user has had their say
        target = pyre.primitives.path(self.target).resolve()

        # lay out what this machine can build before we touch anything on disk
        self.audit()

        # and give the user a last chance to walk away
        if self.ask(question="proceed", default="yes").lower() not in ("y", "yes"):
            # honoring a decline by doing exactly nothing
            self.info.log("nothing done")
            # and reporting a clean, uneventful exit
            return 0

        # with consent in hand, put the source on disk
        self.stage(target=target)
        # help line up an environment when the chosen mode needs one
        if self.mode == "conda":
            self.conda(target=target)
        # and drive the build to completion
        self.build(target=target)

        # leave the user knowing where their freshly built tree lives
        self.info.log(f"pyre is built; the source lives in '{target}'")
        # and report success
        return 0

    # implementation details
    def release(self) -> typing.Tuple[str, str]:
        """
        Report the version this archive was cut from, as a {(tag, human)} pair
        """
        # read the version stamp baked into the framework at build time
        major, minor, micro, revision = pyre.meta.version
        # and hand back both the git tag and a reader-friendly rendering of it
        return f"v{major}.{minor}.{micro}", f"{major}.{minor}.{micro} rev {revision}"

    def pick(self, *, default: str) -> str:
        """
        Settle on what to build: a published release, or the tip of a development branch
        """
        # an explicit choice on the command line ends the conversation before it starts
        if self.source:
            # so hand it straight back
            return self.source
        # with nothing chosen and no one to prompt, this archive's own release is the safe bet
        if not self.interactive:
            # so fall back to it
            return default
        # the first fork in the road: a stable release, or the bleeding edge?
        edition = self.ask(
            question="build a released version or the bleeding edge",
            default="released",
        )
        # anything that leans toward the edge routes us to a live branch checkout
        if edition.lower() in ("b", "bleeding", "bleeding-edge", "edge", "head", "dev"):
            # so find out which branch to track, defaulting to the mainline
            self.branch = self.ask(question="which branch", default=self.branch or "main")
            # and flag the source as a checkout rather than a tag
            return "head"
        # otherwise we are on the release track, so show what GitHub actually publishes
        tags = self.catalog()
        # and when the catalog came back, put the newest handful in front of the user
        if tags:
            # a compact preview, trailing an ellipsis when there is more than we show
            shown = ", ".join(tags[:8])
            self.info.log(f"available releases: {shown}{' …' if len(tags) > 8 else ''}")
        # then let them settle on the tag to pull
        return self.ask(question="which release", default=default)

    def catalog(self) -> typing.List[str]:
        """
        Query GitHub for the published release tags, newest first; empty on any failure
        """
        # turn the repository url into the releases endpoint of the GitHub API
        slug = self.repo.rstrip("/").removeprefix("https://github.com/")
        # by splicing the slug into the api host
        url = f"https://api.github.com/repos/{slug}/releases"
        # then reach out, treating the network as something that is allowed to fail
        try:
            # ask for the json rendering of the releases
            request = urllib.request.Request(
                url, headers={"Accept": "application/vnd.github+json"}
            )
            # open the connection and read the response
            with urllib.request.urlopen(request) as istream:
                # parsing the payload into python data
                payload = json.load(istream)
        # a network hiccup or a garbled response is not fatal here
        except (urllib.error.URLError, json.JSONDecodeError) as error:
            # so warn that the list is unavailable
            self.warning.log(f"could not reach GitHub for the release list ({error})")
            # and carry on with an empty catalog; the embedded tag still works
            return []
        # otherwise surface just the tag names, keeping GitHub's newest-first ordering
        return [release["tag_name"] for release in payload]

    def ask(self, *, question: str, default: str) -> str:
        """
        Prompt for a value when running interactively; otherwise accept {default} silently
        """
        # in batch mode there is no one to answer, so the configured value stands
        if not self.interactive:
            # returned untouched
            return default
        # otherwise put the question to the user, offering {default} in brackets
        reply = input(f"{question} [{default}]: ").strip()
        # and take what they typed, falling back to {default} on an empty line
        return reply or default

    def audit(self) -> None:
        """
        Probe the host for a toolchain and optional dependencies, explaining what is buildable
        """
        # narrate the whole audit through a channel dedicated to this concern
        channel = journal.info("pyre.boot.audit")
        # open with a heading so the checklist that follows reads as one thought
        channel.line("checking what this machine can build:")

        # the core needs nothing more exotic than a working C++ compiler
        cxx = self.compiler()
        # so if none turned up, mark the core as unbuildable and say how to fix it
        if cxx is None:
            channel.line(
                "  ✗ core framework — no C++ compiler found (set CXX or install one)"
            )
        # and when one is present, confirm the core is good to go and name the compiler
        else:
            channel.line(
                f"  ✓ core framework (pyre, journal, merlin + extensions) via {cxx}"
            )

        # walk the optional features, each gated on its own external package
        for name, package, commands in features:
            # a feature is buildable when any of its probe commands is on the PATH
            available = any(shutil.which(command) is not None for command in commands)
            # pick the checkmark that matches
            mark = "✓" if available else "✗"
            # and the note that either celebrates or names the missing dependency
            note = "available" if available else f"needs {package}"
            # then record the verdict for this feature
            channel.line(f"  {mark} {name} — {note}")

        # close by setting expectations: a bare toolchain already yields a usable framework
        channel.line("")
        # spelling out that the core stands alone
        channel.line(
            "  the core builds with no extra packages; optional features light up"
        )
        # and that the rest arrives for free as dependencies appear
        channel.line("  automatically once their dependency is on your PATH")
        # flush the assembled checklist as a single entry
        channel.log()
        # nothing to report back; the audit speaks through its channel
        return

    def compiler(self) -> typing.Optional[str]:
        """
        Locate a C++ compiler, honoring {CXX} before falling back to the usual suspects
        """
        # try an explicit choice from the environment first, then the common driver names
        for candidate in filter(None, (os.environ.get("CXX"), "c++", "g++", "clang++")):
            # resolving each candidate against the PATH
            found = shutil.which(candidate)
            # and settling on the first one that actually exists
            if found is not None:
                # by handing back its full path
                return found
        # nothing on the list was usable, so report the absence
        return None

    def stage(self, *, target: "pyre.primitives.path") -> None:
        """
        Populate {target} with the pyre source: a live branch checkout, or a release tarball
        """
        # a destination that already holds something is not ours to overwrite
        if target.exists() and any(target.contents):
            # so refuse rather than risk clobbering the user's work
            self.error.log(f"'{target}' already exists and is not empty")

        # the bleeding edge arrives as a git checkout the user can actually work in
        if self.source == "head":
            # and none of that is possible without git on hand
            if shutil.which("git") is None:
                # so say so plainly and stop
                self.error.log(
                    "git is required to pull the bleeding edge; install it or choose a release"
                )
            # start assembling the clone command
            command = ["git", "clone"]
            # narrowing it to the requested branch when one was named
            if self.branch:
                command += ["--branch", self.branch]
            # and landing the work in the destination the user picked
            command += [self.repo, str(target)]
            # narrate what is about to happen, branch and all
            self.info.log(
                f"cloning {self.repo}{f' ({self.branch})' if self.branch else ''} into '{target}'"
            )
            # run the clone and wait for it to finish
            outcome = subprocess.run(command)
            # a failed clone leaves nothing to build, so treat it as fatal
            if outcome.returncode != 0:
                self.error.log(f"git clone failed with status {outcome.returncode}")
            # the checkout is the whole job on this path
            return

        # every other choice is a published tag, delivered as a tarball
        url = f"{self.repo}/archive/refs/tags/{self.source}.tar.gz"
        # announce the download so a slow network does not read as a hang
        self.info.log(f"downloading {url}")
        # then fetch and unpack it into place
        self.untar(url=url, target=target)
        # and that completes the staging
        return

    def untar(self, *, url: str, target: "pyre.primitives.path") -> None:
        """
        Download the source tarball at {url} and unpack its single top-level tree into {target}
        """
        # work in a scratch directory that cleans itself up no matter how we leave
        with tempfile.TemporaryDirectory() as scratch:
            # where the downloaded archive will live
            archive = os.path.join(scratch, "source.tar.gz")
            # grab the bytes, treating a bad tag or a network stumble as recoverable
            try:
                # stream the response straight to disk to keep memory flat
                with urllib.request.urlopen(url=url) as istream, open(
                    archive, "wb"
                ) as ostream:
                    # copying the payload across in chunks
                    shutil.copyfileobj(istream, ostream)
            # a download that never arrives is a clean, explainable failure
            except urllib.error.URLError as error:
                # so report it and stop
                self.error.log(f"failed to download {url}: {error}")
            # open the archive for extraction
            with tarfile.open(archive) as tar:
                # unpack it, asking modern python to sanitize member paths
                try:
                    tar.extractall(scratch, filter="data")
                # the {filter} argument predates older interpreters
                except TypeError:
                    # so fall back to the classic extraction when it is unavailable
                    tar.extractall(scratch)
            # GitHub wraps the whole tree in a single {pyre-x.y.z} directory beside our archive
            roots = [entry for entry in os.listdir(scratch) if entry != "source.tar.gz"]
            # anything other than exactly one wrapper means the layout is not what we assumed
            if len(roots) != 1:
                # so refuse to guess and report the surprise
                self.error.log(f"unexpected tarball layout: {roots}")
            # promote that lone directory to the destination the user picked
            shutil.move(os.path.join(scratch, roots[0]), str(target))
        # the tree is in place; the scratch directory is already gone
        return

    def conda(self, *, target: "pyre.primitives.path") -> None:
        """
        Help the user line up a conda environment when building in conda mode
        """
        # none of this guidance is possible without conda on the PATH
        if shutil.which("conda") is None:
            # so point the user at an installer and bow out
            self.warning.log(
                "conda mode selected, but no 'conda' on your PATH; install miniforge"
            )
            # nothing more we can usefully say
            return

        # an already-active environment is the happy path
        active = os.environ.get("CONDA_PREFIX")
        # so when one is live, just confirm we will build into it
        if active:
            # naming it so the user knows where products will land
            self.info.log(f"building into the active conda environment at '{active}'")
            # and leave the environment untouched
            return

        # with nothing active, look for a spec the repo ships, in order of preference
        for relative in (
            ".conda/environment.yml",
            "etc/environment.yml",
            "environment.yml",
        ):
            # resolve each candidate against the staged tree
            spec = target / relative
            # and on the first one that exists, hand the user the exact command to run
            if spec.exists():
                # so they can create the environment themselves
                self.info.log(
                    f"no environment active; create one with: conda env create -f {spec}"
                )
                # our job here is done
                return

        # no active environment and no shipped spec leaves only generic advice
        self.warning.log(
            "no conda environment is active; create and activate one before building"
        )
        # which is the most we can offer without guessing package names
        return

    def build(self, *, target: "pyre.primitives.path") -> None:
        """
        Drive the freshly staged tree's own {mm} driver in a subprocess
        """
        # announce the build so its mode and source are on the record
        self.info.log(f"building pyre in '{self.mode}' mode from '{target}'")

        # the staged tree ships its own {mm}, which finds its engine and portinfo relative
        # to itself; running it in a fresh process keeps it the sole {pyre.application} and
        # sidesteps the one-application-per-process constraint that would otherwise bite
        driver = target / "bin" / "mm"

        # start from a copy of our own environment so we only add to it
        environment = dict(os.environ)
        # locate the archive we are running from, which is our copy of the framework
        archive = os.path.dirname(__file__)
        # note whatever PYTHONPATH the user already has
        existing = environment.get("PYTHONPATH")
        # then prepend our archive so the child's {import pyre} resolves against it
        # instead of fetching a bootstrap zip of its own
        environment["PYTHONPATH"] = (
            os.pathsep.join((archive, existing)) if existing else archive
        )

        # run the driver from the tree root, where {mm} finds the local {.mm} configuration
        outcome = subprocess.run(
            [sys.executable, str(driver), f"--mode={self.mode}"],
            cwd=str(target),
            env=environment,
        )

        # a non-zero exit from the build is a real failure the user needs to hear about
        if outcome.returncode != 0:
            self.error.log(f"the build exited with status {outcome.returncode}")
        # otherwise the build stands on its own output; nothing to add
        return


# bootstrap: this module is staged as the archive's {__main__.py}, so it is the entry point
if __name__ == "__main__":
    # instantiate the app
    app = Boot(name="pyre-boot")
    # launch it
    status = app.run()
    # share the exit code with the shell
    raise SystemExit(status)


# end of file
