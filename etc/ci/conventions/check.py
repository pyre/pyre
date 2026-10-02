#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import argparse
import datetime
import fnmatch
import os
import re
import subprocess
import sys
import tomllib

# the description of the program, for the help screen
DESCRIPTION = """
Check a checkout against the conventions of the repository: spelling, the formatting of python
and c++ sources, file preambles and closing markers, and, given the branch the work is based on,
the commits on top of it and the copyright year of the files they touch. The same checks run on
every pull request; running them before pushing saves a round trip
"""

# the checks, in the order they run
CHECKS = ("spelling", "python", "cxx", "preambles", "commits")

# the files whose preambles and closing markers are not checked, by extension, unless they carry
# a preamble anyway: binaries, and formats that cannot carry comments
OPAQUE = (
    ".png",
    ".jpg",
    ".gif",
    ".ico",
    ".svg",
    ".pdf",
    ".graffle",
    ".numbers",
    ".nb",
    ".odb",
    ".ttf",
    ".woff",
    ".woff2",
    ".dylib",
    ".json",
    ".ipynb",
    ".csv",
    ".txt",
    ".dict",
    ".dat",
    ".data",
    ".pub",
    ".plist",
)
# the c++ sources clang-format looks after
CXX = (".h", ".icc", ".cc", ".cpp", ".cu")
# the copyright line, with whatever comment marker precedes it
COPYRIGHT_LINE = re.compile(r"^(?P<prefix>.*?)\(c\) 1998-\d{4} all rights reserved$")
# the lines that open a block comment preamble, and the ones that close it
OPENERS = ("<!--", "{/*", "/*")
CLOSERS = ("-->", "*/}", "*/")
# the lines that may precede the preamble: interpreters, xml declarations and doctypes, along
# with their indented continuations, the magic lines of environment modules and zsh completion
# functions, and the mode line of a stylesheet, which sits outside its block
PRELUDE = re.compile(
    r"^(#!|<\?xml |(?i:<!doctype )|\s+\S|#%Module|#compdef |/\*\s+-\*- [a-z]+ -\*-\s+\*/$)"
)
# the mode line; the mode is in lower case, unless it carries variables, like the image name of
# a dockerfile, whose double marker it keeps
MODE = re.compile(r"^#?(?P<marker>.*?)-\*- (?P<mode>[a-z0-9+\-]+|[a-z\-]+: .+) -\*-$")

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
    The files git tracks under {root}, narrowed to {extensions} and outside the {exempt} patterns
    """
    # ask git
    names = run(command=["git", "ls-files"], cwd=root).stdout.split("\n")
    # keep the ones of interest
    return [
        name
        for name in names
        if name
        and (not extensions or name.endswith(extensions))
        and not any(fnmatch.fnmatch(name, pattern) for pattern in exempt)
        and os.path.isfile(os.path.join(root, name))
    ]


def exemptions(*, root: str) -> tuple:
    """
    The patterns of the files the preamble and c++ formatting checks leave alone, as listed in
    the {exempt} table of {tool.conventions} in {pyproject.toml}
    """
    # the configuration of the repository
    path = os.path.join(root, "pyproject.toml")
    # a repository without one
    if not os.path.isfile(path):
        # exempts nothing
        return ()
    # read it
    with open(path, mode="rb") as stream:
        # all of it
        configuration = tomllib.load(stream)
    # hand off the patterns
    return tuple(configuration.get("tool", {}).get("conventions", {}).get("exempt", []))


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
    files = tracked(root=root, extensions=CXX, exempt=exemptions(root=root))
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
    Check that every tracked file opens with the standard preamble and closes with an end of
    file marker, and that the files touched since {base} carry the current year
    """
    # the complaints
    problems = []
    # the files, minus the exemptions of the repository
    files = tracked(root=root, exempt=exemptions(root=root))
    # the files touched since the base, when there is one
    touched = set(changed(root=root, base=base)) if base else set()
    # the current year
    year = str(datetime.date.today().year)
    # go through the files
    for name in files:
        # attempt to
        try:
            # read the file
            with open(os.path.join(root, name), encoding="utf-8") as stream:
                # all of it
                text = stream.read()
        # a file that is not text
        except UnicodeDecodeError:
            # has no preamble to check
            continue
        # an opaque format is checked only when the file carries a preamble anyway, as a
        # makefile named for the data it builds or a python source named for its role does
        if name.endswith(OPAQUE) and not any(
            COPYRIGHT_LINE.match(line) for line in text.split("\n")[:15]
        ):
            # the rest are left alone
            continue
        # check its layout
        problems.extend(f"{name}: {problem}" for problem in layout(name=name, text=text))
        # the copyright line sits in the preamble, near the top
        copyright = next(
            (COPYRIGHT.search(line) for line in text.split("\n")[:15] if COPYRIGHT.search(line)),
            None,
        )
        # a file touched by the work
        if copyright is not None and name in touched and copyright.group(1) != year:
            # carries the current year
            problems.append(f"{name}: touched, but its copyright ends in {copyright.group(1)}")
    # hand off the complaints
    return problems


def layout(*, name: str, text: str) -> list:
    """
    Check the preamble and postamble of the file {name}, whose contents are {text}: the mode,
    coding, spacer, author and copyright lines, two blank lines before the body, and two more
    before the end of file marker
    """
    # an empty file
    if not text:
        # has no preamble to speak of
        return ["no preamble"]
    # the complaints
    problems = []
    # the file ends with a single newline
    if not text.endswith("\n") or text.endswith("\n\n"):
        # or else its last line is not where it should be
        problems.append("does not end with exactly one newline")
    # split into lines, without the empty one after the final newline
    lines = text.rstrip("\n").split("\n")
    # the copyright line sits in the preamble, near the top
    idx = next((i for i, line in enumerate(lines[:15]) if COPYRIGHT_LINE.match(line)), None)
    # a file without one
    if idx is None:
        # is missing its preamble, and nothing else can be said about it
        return problems + ["no '(c) 1998-YYYY all rights reserved' in its preamble"]
    # the comment marker is whatever precedes the copyright
    prefix = COPYRIGHT_LINE.match(lines[idx]).group("prefix")
    # a block comment preamble opens on a line of its own
    opener = next((i for i in range(idx - 1, -1, -1) if lines[i].strip() in OPENERS), None)
    # the comment lines start right after the opener, or with the first line that carries the
    # marker, past the lines that may precede the preamble
    start = opener + 1 if opener is not None else 0
    # skip the prelude of a line comment preamble
    while opener is None and start < idx and PRELUDE.match(lines[start]):
        # one line at a time
        start += 1
    # every line before the comment, other than the opener, belongs in the prelude
    prelude = [line for line in lines[: opener if opener is not None else start] if line]
    # so anything else
    if not all(PRELUDE.match(line) for line in prelude):
        # is out of place
        problems.append("unexpected lines above the preamble")
    # the comment lines, through the copyright
    comment = lines[start : idx + 1]
    # the marker, without its trailing space
    marker = prefix.rstrip()
    # the mode line can sit in the prelude of a stylesheet
    moded = any("-*-" in line for line in prelude)
    # otherwise, it opens the comment
    if not moded:
        # get it
        mode = MODE.match(comment[0]) if comment else None
        # it must be there, in lower case
        if not mode or not comment[0].startswith(marker):
            # or else the language of the file is not recorded
            problems.append("the preamble does not open with a lower case mode line")
        # move on
        comment = comment[1:]
    # the rest of the comment: coding, spacer, at least one author, and the copyright
    expected = [f"{prefix}-*- coding: utf-8 -*-", marker]
    # compare
    if comment[:2] != expected or len(comment) < 4 or any(not line.strip() for line in comment[2:]):
        # the preamble has lines missing, extra, or out of order
        problems.append("the preamble is not mode, coding, spacer, author, and copyright")
    # past the copyright
    nxt = idx + 1
    # a block comment closes on the next line
    if opener is not None:
        # make sure it does
        if nxt >= len(lines) or lines[nxt].strip() not in CLOSERS:
            # or else the preamble runs on
            problems.append("the preamble block does not close after the copyright")
        # and move past it
        nxt += 1
    # count the blank lines after the preamble
    blanks = 0
    # by walking down
    while nxt + blanks < len(lines) and not lines[nxt + blanks]:
        # one at a time
        blanks += 1
    # the first line of the body
    body = lines[nxt + blanks] if nxt + blanks < len(lines) else ""
    # a c++ header keeps its code guard next to the preamble, as does a markdown document
    gap = 1 if body.startswith("// code guard") or name.endswith(".md") else 2
    # check
    if blanks != gap:
        # and complain
        problems.append(f"{blanks} blank lines after the preamble, instead of {gap}")
    # the last line
    last = lines[-1]
    # is the closing marker
    if "end of file" not in last:
        # or else the file is not closed
        problems.append("does not end with an 'end of file' marker")
        # and its spacing means nothing
        return problems
    # count the blank lines before it
    blanks = 0
    # by walking up
    while blanks < len(lines) - 1 and not lines[-2 - blanks]:
        # one at a time
        blanks += 1
    # black puts a single blank line after imports, so python decides for itself
    allowed = (1, 2) if name.endswith(".py") else (2,)
    # a file with no body shares the blank lines after the preamble
    if len(lines) - 1 - blanks == nxt:
        # so its count is the one that matters
        allowed = (blanks,)
    # check
    if blanks not in allowed:
        # and complain
        problems.append(f"{blanks} blank lines before the end of file marker, instead of 2")
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
