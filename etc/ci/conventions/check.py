#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import argparse
import datetime
import os
import re
import subprocess
import sys

# the description of the program, for the help screen
DESCRIPTION = """
Check a checkout against the conventions of the repository: spelling, the formatting of python
and c++ sources, file preambles and closing markers, and, given the branch the work is based on,
the commits on top of it and the copyright year of the files they touch. The same checks run on
every pull request; running them before pushing saves a round trip
"""

# the checks, in the order they run
CHECKS = ("spelling", "python", "cxx", "preambles", "commits")

# the sources whose preambles and closing markers are checked, by extension
SOURCES = (
    ".py",
    ".h",
    ".icc",
    ".cc",
    ".cpp",
    ".cu",
    ".js",
    ".ts",
    ".tsx",
    ".mm",
    ".yaml",
    ".cmake",
)
# the c++ sources clang-format looks after
CXX = (".h", ".icc", ".cc", ".cpp", ".cu")
# the trees that are exempt from the preamble and c++ formatting checks: project templates hold
# substitution markers that are not valid c++ until they are expanded
EXEMPT = ("templates/",)

# a commit subject names the area it touches, then says what the commit does: an area is a
# path, a package, or a c++ namespace, and several can be listed separated by commas
AREA = r"[A-Za-z0-9_.{}/+\-]+(::[A-Za-z0-9_.{}/+\-]+)*"
SUBJECT = re.compile(rf"^{AREA}(, ?{AREA})*: \S")
# the authors whose commits the commit check leaves alone: bots whose messages are beyond our
# control, such as the dependency updates dependabot proposes
BOTS = ("dependabot[bot]",)
# the copyright line, with any closing year
COPYRIGHT = re.compile(r"\(c\) 1998-(\d{4}) all rights reserved")


class ConventionError(Exception):
    """
    The base class of the reasons a check could not run
    """


class ToolError(ConventionError):
    """
    A tool a check relies on is missing
    """


def run(*, command: list, cwd: str) -> subprocess.CompletedProcess:
    """
    Run {command} in {cwd} and capture what it says, complaining if the tool is missing
    """
    # attempt to
    try:
        # run the command
        return subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    # if the tool is not installed
    except FileNotFoundError as error:
        # say which one, and where to get it
        raise ToolError(
            f"'{command[0]}' is not installed; see etc/ci/conventions/requirements.txt"
        ) from error


def tracked(*, root: str, extensions: tuple = (), exempt: tuple = ()) -> list:
    """
    The files git tracks under {root}, narrowed to {extensions} and outside the {exempt} trees
    """
    # ask git
    names = run(command=["git", "ls-files"], cwd=root).stdout.split("\n")
    # keep the ones of interest
    return [
        name
        for name in names
        if name
        and (not extensions or name.endswith(extensions))
        and not name.startswith(exempt)
        and os.path.isfile(os.path.join(root, name))
    ]


def spelling(*, root: str, base: str | None) -> list:
    """
    Spell check the prose of every tracked file, with the exclusions in {pyproject.toml}
    """
    # the files
    files = tracked(root=root)
    # check them
    result = run(command=["codespell", "--toml", "pyproject.toml", *files], cwd=root)
    # every line of output is a misspelling
    problems = [line for line in result.stdout.split("\n") if line.strip()]
    # add the advice, if there is anything to advise about
    if problems:
        # a word codespell does not know is either a typo or belongs on the reviewed lists
        problems.append(
            "fix the typos; a real word goes in etc/ci/conventions/codespell-words.txt, and a "
            "line that is right as it is goes in etc/ci/conventions/codespell-lines.txt"
        )
    # hand off the complaints
    return problems


def python(*, root: str, base: str | None) -> list:
    """
    Check that every tracked python source is formatted by black
    """
    # the files
    files = tracked(root=root, extensions=(".py",))
    # check them
    # the exclusions in {pyproject.toml} apply even to files named on the command line
    result = run(command=["black", "--check", *files], cwd=root)
    # black names each file it would change
    problems = [line for line in result.stderr.split("\n") if line.startswith("would reformat")]
    # a failure that named no file is a failure of black itself
    if result.returncode != 0 and not problems:
        # so report what it said, or at least that it failed
        problems = [line for line in result.stderr.split("\n") if line.strip()] or [
            f"black exited with status {result.returncode}"
        ]
    # hand off the complaints
    return problems


def cxx(*, root: str, base: str | None) -> list:
    """
    Check that every tracked c++ source is formatted by clang-format
    """
    # the files
    files = tracked(root=root, extensions=CXX, exempt=EXEMPT)
    # check them
    result = run(command=["clang-format", "--dry-run", *files], cwd=root)
    # clang-format warns once per change it would make; one complaint per file is enough
    names = sorted(
        {line.split(":")[0] for line in result.stderr.split("\n") if ": warning:" in line}
    )
    # hand off the complaints
    return [f"{name}: not formatted by clang-format" for name in names]


def preambles(*, root: str, base: str | None) -> list:
    """
    Check that every tracked source opens with a copyright line and closes with an end of file
    marker, and that the files touched since {base} carry the current year
    """
    # the complaints
    problems = []
    # the files
    files = tracked(root=root, extensions=SOURCES, exempt=EXEMPT)
    # the files touched since the base, when there is one
    touched = set(changed(root=root, base=base)) if base else set()
    # the current year
    year = str(datetime.date.today().year)
    # go through the files
    for name in files:
        # read the file
        with open(os.path.join(root, name), encoding="utf-8") as stream:
            # as lines
            lines = stream.read().split("\n")
        # the copyright line sits in the preamble, near the top
        copyright = next(
            (COPYRIGHT.search(line) for line in lines[:12] if COPYRIGHT.search(line)), None
        )
        # a file without one
        if copyright is None:
            # is missing its preamble
            problems.append(f"{name}: no '(c) 1998-{year} all rights reserved' in its preamble")
        # a file touched by the work
        elif name in touched and copyright.group(1) != year:
            # carries the current year
            problems.append(f"{name}: touched, but its copyright ends in {copyright.group(1)}")
        # the last line that says anything
        last = next((line.strip() for line in reversed(lines) if line.strip()), "")
        # is the closing marker, in the comment syntax of the file
        if not last.lower().removesuffix("*/").strip().endswith("end of file"):
            # or else the file is not closed
            problems.append(f"{name}: does not end with an 'end of file' marker")
    # hand off the complaints
    return problems


def commits(*, root: str, base: str | None) -> list:
    """
    Check the commits since {base}: a subject that names its area and says what the commit does,
    and nothing after it; the commits of the bots in {BOTS}, whose messages are beyond our
    control, are left out
    """
    # without a base there is nothing to check
    if not base:
        # so say nothing
        return []
    # the commits since the base, oldest first, as hash, author, subject, and body, merges left out
    log = run(
        command=[
            "git",
            "log",
            "--no-merges",
            "--reverse",
            "--format=%h%x00%an%x00%s%x00%b%x01",
            f"{base}..HEAD",
        ],
        cwd=root,
    ).stdout
    # the complaints
    problems = []
    # go through the commits
    for record in log.split("\x01"):
        # skip the separator after the last one
        if not record.strip():
            # by moving on
            continue
        # unpack
        sha, author, subject, body = record.strip("\n").split("\x00")
        # a bot writes its messages its own way, and that way may change without notice
        if author in BOTS:
            # so its commits are not held to the conventions
            continue
        # the subject names its area and says what the commit does
        if not SUBJECT.match(subject):
            # or else it does not read like the rest of the history
            problems.append(f"{sha}: '{subject}' is not of the form 'area: what the commit does'")
        # and the subject is all there is
        if body.strip():
            # the narrative belongs in the pull request, not the commit
            problems.append(f"{sha}: has a body; the subject line is the whole message")
    # hand off the complaints
    return problems


def changed(*, root: str, base: str) -> list:
    """
    The files added or modified since {base}
    """
    # ask git
    result = run(
        command=["git", "diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD"], cwd=root
    )
    # hand off the names
    return [name for name in result.stdout.split("\n") if name]


def parse() -> argparse.Namespace:
    """
    Read the command line
    """
    # make a parser
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    # the base of the work
    parser.add_argument(
        "--base",
        default=None,
        help="the branch the work is based on, e.g. origin/main; enables the commit and year checks",
    )
    # a subset of the checks
    parser.add_argument(
        "--only",
        default=",".join(CHECKS),
        help=f"a comma separated subset of the checks: {', '.join(CHECKS)}",
    )
    # parse and hand off
    return parser.parse_args()


def main() -> int:
    """
    Run the requested checks and report what each one found
    """
    # read the command line
    options = parse()
    # the top of the checkout
    root = run(command=["git", "rev-parse", "--show-toplevel"], cwd=os.getcwd()).stdout.strip()
    # the checks, by name
    table = {name: globals()[name] for name in CHECKS}
    # the requested ones
    requested = [name for name in options.only.split(",") if name]
    # a name that is not a check is a mistake
    unknown = [name for name in requested if name not in table]
    # so refuse it
    if unknown:
        # say which
        print(f"unknown checks: {', '.join(unknown)}; the checks are {', '.join(CHECKS)}")
        # and bail
        return 2
    # the number of checks that found something
    failed = 0
    # go through them
    for name in requested:
        # attempt to
        try:
            # run the check
            problems = table[name](root=root, base=options.base)
        # if it could not run
        except ConventionError as error:
            # it counts as a failure
            problems = [str(error)]
        # report the verdict
        print(f"{name}: {'ok' if not problems else f'{len(problems)} problems'}")
        # and the details
        for problem in problems:
            # one per line
            print(f"    {problem}")
        # tally
        failed += 1 if problems else 0
    # the exit status says whether everything passed
    return 1 if failed else 0


# entry point
if __name__ == "__main__":
    # run the checks and report their verdict
    sys.exit(main())


# end of file
