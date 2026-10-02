#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import datetime
import os
import shutil
import subprocess
import sys
import tempfile

# the checker under test, next to this file
CHECKER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check.py")
# the c++ formatting rules of the repository, which the scratch repositories borrow
CLANG_FORMAT = os.path.join(os.path.dirname(CHECKER), "..", "..", "..", ".clang-format")
# the current year, which the preamble of a touched file must carry
YEAR = datetime.date.today().year
# a misspelling for the spell checker to catch, assembled here so the source that plants it
# does not trip the spell check of this repository
MISSPELLING = "t" + "eh"


class SelfTestError(Exception):
    """
    The checker did not report what it should have
    """


def preamble(*, comment: str, language: str) -> str:
    """
    The standard preamble of a source file, in the given {comment} syntax
    """
    # assemble it line by line
    return (
        f"{comment} -*- {language} -*-\n"
        f"{comment} -*- coding: utf-8 -*-\n"
        f"{comment}\n"
        f"{comment} michael a.g. aïvázis <michael.aivazis@para-sim.com>\n"
        f"{comment} (c) 1998-{YEAR} all rights reserved\n"
    )


def git(*args: str, cwd: str) -> str:
    """
    Run git in {cwd} and hand back what it says
    """
    # run it, failing loudly, since a scratch repository that cannot be built tests nothing
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    # hand off its output
    return result.stdout


def write(*, root: str, name: str, text: str) -> None:
    """
    Write {text} to the file {name} under {root}
    """
    # make room for it
    os.makedirs(os.path.dirname(os.path.join(root, name)) or root, exist_ok=True)
    # and write it
    with open(os.path.join(root, name), mode="w", encoding="utf-8") as stream:
        # all at once
        stream.write(text)
    # all done
    return


def scaffold(*, root: str) -> None:
    """
    Lay out a scratch repository whose single commit satisfies every convention
    """
    # make the repository
    git("init", "--quiet", "--initial-branch=main", cwd=root)
    # with an identity for its commits
    git("config", "user.name", "self test", cwd=root)
    git("config", "user.email", "selftest@example.com", cwd=root)
    # the configuration the checks read
    write(
        root=root,
        name="pyproject.toml",
        text=preamble(comment="#", language="toml")
        + '\n\n[tool.black]\nline-length = 100\n\n[tool.codespell]\nignore-words = "words.txt"\n'
        + '\n[tool.conventions]\nexempt = ["vendor/*"]\n'
        + "\n\n# end of file\n",
    )
    # an empty list of known good words
    write(root=root, name="words.txt", text="")
    # the c++ formatting rules
    shutil.copy(CLANG_FORMAT, os.path.join(root, ".clang-format"))
    # a python source that follows the conventions
    write(
        root=root,
        name="good.py",
        text=preamble(comment="#", language="python")
        + '\n\ndef answer():\n    """\n    The answer\n    """\n    # hand it off\n    return 42\n'
        + "\n\n# end of file\n",
    )
    # and a c++ one
    write(
        root=root,
        name="good.cc",
        text=preamble(comment="//", language="c++")
        + "\n\n// the answer\nint\nanswer()\n{\n    // hand it off\n    return 42;\n}\n\n\n// end of file\n",
    )
    # commit them
    git("add", "pyproject.toml", "words.txt", ".clang-format", "good.py", "good.cc", cwd=root)
    git("commit", "--quiet", "-m", "base: the starting point", cwd=root)
    # all done
    return


def check(*, root: str, base: str | None = None) -> tuple:
    """
    Run the checker in {root} and hand back its exit status and report
    """
    # the command line
    command = [sys.executable, CHECKER] + (["--base", base] if base else [])
    # run it
    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
    # hand off the verdict
    return result.returncode, result.stdout


def expect(*, report: str, check: str, needle: str) -> None:
    """
    Make sure the {check} section of {report} mentions {needle}
    """
    # find the section of the check
    lines = report.split("\n")
    # its header
    start = next((i for i, line in enumerate(lines) if line.startswith(f"{check}:")), None)
    # a check that did not report at all
    if start is None:
        # is a failure
        raise SelfTestError(f"'{check}' did not report:\n{report}")
    # its details are the indented lines that follow
    details = []
    # collect them
    for line in lines[start + 1 :]:
        # until the next section
        if not line.startswith("    "):
            # which ends this one
            break
        # otherwise, keep it
        details.append(line)
    # the needle has to be among them
    if not any(needle in line for line in details):
        # or else the check missed what it was supposed to catch
        raise SelfTestError(f"'{check}' did not mention '{needle}':\n{report}")
    # all done
    return


def clean() -> None:
    """
    A repository that follows the conventions passes every check
    """
    # in a scratch directory
    with tempfile.TemporaryDirectory() as root:
        # lay out the repository
        scaffold(root=root)
        # and check it
        status, report = check(root=root, base="main")
        # everything passed
        if status != 0:
            # or else the checker complains about good work
            raise SelfTestError(f"a clean repository failed:\n{report}")
    # all done
    return


def violations() -> None:
    """
    Each kind of violation is caught by the check that looks for it
    """
    # in a scratch directory
    with tempfile.TemporaryDirectory() as root:
        # lay out the repository
        scaffold(root=root)
        # work on a branch
        git("switch", "--quiet", "-c", "work", cwd=root)
        # a python source with a misspelling, bad formatting, and no closing marker
        write(
            root=root,
            name="bad.py",
            text=preamble(comment="#", language="python")
            + f"\n\n# {MISSPELLING} answer\nx=[1,2 ,3]\n",
        )
        # a c++ source that is not formatted
        write(
            root=root,
            name="bad.cc",
            text=preamble(comment="//", language="c++")
            + "\nint answer(){return 42;}\n\n\n// end of file\n",
        )
        # an existing file touched without bringing its year up to date
        with open(os.path.join(root, "good.cc"), encoding="utf-8") as stream:
            # read it
            text = stream.read()
        # age its copyright, and change something in it
        write(
            root=root,
            name="good.cc",
            text=text.replace(f"1998-{YEAR}", "1998-2000").replace("the answer", "the reply"),
        )
        # commit it all with a subject that names no area, and a body
        git("add", "bad.py", "bad.cc", "good.cc", cwd=root)
        git("commit", "--quiet", "-m", "fixed some things", "-m", "a body", cwd=root)
        # check
        status, report = check(root=root, base="main")
        # the checker failed
        if status == 0:
            # or else it let everything through
            raise SelfTestError(f"violations passed:\n{report}")
        # and every check caught its violation
        expect(report=report, check="spelling", needle=MISSPELLING)
        expect(report=report, check="python", needle="bad.py")
        expect(report=report, check="cxx", needle="bad.cc")
        expect(report=report, check="preambles", needle="bad.py: does not end")
        expect(report=report, check="preambles", needle="good.cc: touched")
        expect(report=report, check="commits", needle="is not of the form")
        expect(report=report, check="commits", needle="has a body")
    # all done
    return


def layouts() -> None:
    """
    Each departure from the standard preamble and postamble layout is caught, and the files the
    repository exempts are left alone
    """
    # the departures, by file, with what the checker says about each
    cases = {
        # a mode in mixed case
        "upper.py": (
            preamble(comment="#", language="Python") + "\n\nx = 1\n\n\n# end of file\n",
            "lower case mode line",
        ),
        # no coding line
        "coding.sh": (
            "# -*- bash -*-\n#\n# michael a.g. aïvázis\n# (c) 1998-2026 all rights reserved\n"
            + "\n\necho\n\n\n# end of file\n",
            "mode, coding, spacer, author, and copyright",
        ),
        # a single blank line after the preamble
        "tight.yaml": (
            preamble(comment="#", language="yaml") + "\nkey: value\n\n\n# end of file\n",
            "1 blank lines after the preamble",
        ),
        # a single blank line before the closing marker of a c++ source
        "short.cc": (
            preamble(comment="//", language="c++") + "\n\nint x = 0;\n\n// end of file\n",
            "1 blank lines before the end of file marker",
        ),
        # two blank lines between the preamble and the code guard of a header
        "guard.h": (
            preamble(comment="//", language="c++")
            + "\n\n// code guard\n#pragma once\n\n\n// end of file\n",
            "2 blank lines after the preamble, instead of 1",
        ),
        # a makefile named for the data it builds, whose extension is otherwise left alone
        "build.data": (
            preamble(comment="#", language="makefile") + "\nall:\n\n\n# end of file\n",
            "1 blank lines after the preamble",
        ),
        # extra blank lines at the end
        "trail.toml": (
            preamble(comment="#", language="toml") + "\n\nkey = 1\n\n\n# end of file\n\n",
            "exactly one newline",
        ),
    }
    # the departures the checker must not flag: a header with its code guard, a markdown
    # document, a dockerfile, a script, a stylesheet, and a file the repository exempts
    fine = {
        "guard.icc": preamble(comment="//", language="c++")
        + "\n// code guard\n#pragma once\n\n\n// end of file\n",
        "doc.md": "<!--\n-*- markdown -*-\n-*- coding: utf-8 -*-\n\n"
        + "michael a.g. aïvázis <michael.aivazis@para-sim.com>\n"
        + f"(c) 1998-{YEAR} all rights reserved\n-->\n\n# title\n\n\n<!-- end of file -->\n",
        "Dockerfile": '## -*- docker-image-name: "x:y" -*-\n'
        + preamble(comment="#", language="x").split("\n", 1)[1]
        + "\n\nFROM ubuntu\n\n\n# end of file\n",
        "run.sh": "#!/bin/bash\n"
        + preamble(comment="#", language="bash")
        + "\n\necho\n\n\n# end of file\n",
        "look.css": "/*  -*- css -*-  */\n/*\n * -*- coding: utf-8 -*-\n *\n"
        + " * michael a.g. aïvázis <michael.aivazis@para-sim.com>\n"
        + f" * (c) 1998-{YEAR} all rights reserved\n */\n\n\na {{\n}}\n\n\n/* end of file */\n",
        "_complete": "#compdef complete\n"
        + preamble(comment="#", language="zsh")
        + "\n\n_arguments\n\n\n# end of file\n",
        "page.html": "<!DOCTYPE html>\n\n<!--\n-*- html -*-\n-*- coding: utf-8 -*-\n\n"
        + "michael a.g. aïvázis <michael.aivazis@para-sim.com>\n"
        + f"(c) 1998-{YEAR} all rights reserved\n-->\n\n\n<html>\n</html>\n\n\n<!-- end of file -->\n",
        "vendor/theirs.js": "// no preamble here\n",
        "values.csv": "1,2,3\n",
    }
    # in a scratch directory
    with tempfile.TemporaryDirectory() as root:
        # lay out the repository
        scaffold(root=root)
        # add the files
        for name, text in [(name, text) for name, (text, _) in cases.items()] + list(fine.items()):
            # one by one
            write(root=root, name=name, text=text)
        # and let git know about them
        git("add", *cases, *fine, cwd=root)
        # check the preambles
        result = subprocess.run(
            [sys.executable, CHECKER, "--only", "preambles"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        # every departure was caught
        for name, (_, needle) in cases.items():
            # with the right complaint on its own line
            if not any(
                f"{name}: " in line and needle in line for line in result.stdout.split("\n")
            ):
                # or else the checker missed it
                raise SelfTestError(f"'{name}' was not flagged for '{needle}':\n{result.stdout}")
        # and nothing else was
        for name in fine:
            # by name
            if f"{name}: " in result.stdout:
                # or else the checker complains about good work
                raise SelfTestError(f"'{name}' was flagged:\n{result.stdout}")
    # all done
    return


def bots() -> None:
    """
    The commits of a bot are not held to the commit conventions, and the same message from a
    person still is
    """
    # in a scratch directory
    with tempfile.TemporaryDirectory() as root:
        # lay out the repository
        scaffold(root=root)
        # work on a branch
        git("switch", "--quiet", "-c", "work", cwd=root)
        # the message a dependency update comes with: no area, and a body
        message = ["-m", "Bump black from 26.5.1 to 26.6.0", "-m", "the release notes"]
        # a bot commits a change with it
        write(root=root, name="words.txt", text="tread\n")
        git("add", "words.txt", cwd=root)
        git("-c", "user.name=dependabot[bot]", "commit", "--quiet", *message, cwd=root)
        # which passes
        status, report = check(root=root, base="main")
        # every check
        if status != 0:
            # or else the bot is held to conventions it cannot follow
            raise SelfTestError(f"a bot commit failed:\n{report}")
        # a person commits another change with the same message
        write(root=root, name="words.txt", text="tread\nraison\n")
        git("add", "words.txt", cwd=root)
        git("commit", "--quiet", *message, cwd=root)
        # which does not pass
        status, report = check(root=root, base="main")
        # the commit check catches it
        expect(report=report, check="commits", needle="is not of the form")
    # all done
    return


def main() -> int:
    """
    Run the self tests
    """
    # attempt to
    try:
        # check a clean repository
        clean()
        # one full of violations
        violations()
        # one with every kind of preamble departure
        layouts()
        # and one with commits by a bot
        bots()
    # if the checker misbehaved
    except SelfTestError as error:
        # say how
        print(f"selftest: {error}")
        # and fail
        return 1
    # all good
    return 0


# entry point
if __name__ == "__main__":
    # run the self tests and report their verdict
    sys.exit(main())


# end of file
