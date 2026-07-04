#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the toolkit under demonstration
import survey


def main():
    """
    A small project-scaffolding wizard that walks through everything {survey} can do today
    """
    # style the prompts: a cool blue for the questions, a warm orange for the current choice
    survey.set_theme(
        survey.Theme(
            message=survey.chroma.hsl(210, 0.85, 0.62),
            selected=survey.chroma.hsl(28, 0.90, 0.55),
        )
    )

    # set the scene
    print("── pyre project wizard ─────────────────────────────")
    print("a quick tour of survey's prompts; press ctrl-c to bail\n")

    # a plain line of text, offering a default the user can accept with a bare enter
    name = survey.text(message="project name", default="my-project")

    # a single choice from a list, driven by the arrow keys on a real terminal
    language = survey.select(
        message="primary language",
        options=["python", "c++", "cuda", "fortran"],
        default="c++",
    )

    # another selection, this time defaulting to the first entry
    license = survey.select(
        message="license",
        options=["BSD-3-Clause", "MIT", "Apache-2.0", "GPL-3.0", "none"],
    )

    # a yes/no question, defaulting to yes
    tests = survey.confirm(message="include a test suite", default=True)

    # the same, but built from the class directly rather than the convenience function,
    # to show the two ways of reaching a prompt
    docs = survey.Confirm(message="include documentation stubs", default=False).ask()

    # lay out everything we gathered
    print("\n── summary ─────────────────────────────────────────")
    for label, value in (
        ("name", name),
        ("language", language),
        ("license", license),
        ("tests", "yes" if tests else "no"),
        ("docs", "yes" if docs else "no"),
    ):
        print(f"  {label:10} {value}")

    # the final gate, exactly the shape the boot app uses
    if not survey.confirm(message="\ncreate this project", default=True):
        # respect a decline by doing nothing
        print("nothing created")
        return 0

    # nothing here actually touches disk; this is a tour, not a generator
    print(f"would scaffold '{name}' ({language}, {license})")
    return 0


# driver
if __name__ == "__main__":
    # run the wizard, treating ctrl-c as a clean, quiet exit
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        # the user bailed; leave the terminal on a fresh line
        print("\ncancelled")
        raise SystemExit(1)


# end of file
