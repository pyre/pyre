#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Every builtin exception of the running python is either one of the ways the evaluation of a
setting can fail, or one that it cannot raise, for a reason recorded here; a python that adds
builtin exceptions fails this test until they are classified
"""


def test() -> None:
    """
    Classify the builtin exceptions of the running python
    """
    # externals
    import builtins
    import sys

    # support
    from pyre.calc.evaluation import errors

    # the builtin exceptions an evaluation cannot raise, by the reason it cannot
    reasons = {
        # the roots of the hierarchy, which nothing raises as such
        "the roots of the hierarchy": ["BaseException", "Exception"],
        # interrupts and exits, which are not mistakes in a setting
        "interrupts and exits are not mistakes in a setting": [
            "GeneratorExit",
            "KeyboardInterrupt",
            "SystemExit",
        ],
        # control flow, which needs functions and statements a setting may not use
        "a setting can't raise, assert, or step through iterators by hand": [
            "AssertionError",
            "BaseExceptionGroup",
            "ExceptionGroup",
            "StopAsyncIteration",
            "StopIteration",
        ],
        # the operating system, which a setting can't reach
        "a setting can't reach files, processes, or the network": [
            "BlockingIOError",
            "BrokenPipeError",
            "ChildProcessError",
            "ConnectionAbortedError",
            "ConnectionError",
            "ConnectionRefusedError",
            "ConnectionResetError",
            "EOFError",
            "EnvironmentError",
            "FileExistsError",
            "FileNotFoundError",
            "IOError",
            "InterruptedError",
            "IsADirectoryError",
            "NotADirectoryError",
            "OSError",
            "PermissionError",
            "ProcessLookupError",
            "TimeoutError",
        ],
        # imports, which a setting can't make
        "a setting can't import": ["ImportError", "ModuleNotFoundError"],
        # the failures of the interpreter itself, which are not mistakes in a setting
        "failures of the interpreter are not mistakes in a setting": [
            "BufferError",
            "MemoryError",
            "NotImplementedError",
            "PythonFinalizationError",
            "ReferenceError",
            "RuntimeError",
            "SystemError",
        ],
    }
    # index them by name
    excluded = {name for names in reasons.values() for name in names}

    # the builtin exceptions of the running python; warnings are never raised as errors here
    exceptions = {
        name: value
        for name, value in vars(builtins).items()
        if isinstance(value, type)
        and issubclass(value, BaseException)
        and not issubclass(value, Warning)
    }
    # the ones that are neither a way an evaluation can fail, nor excluded for a reason
    unclassified = sorted(
        name
        for name, exception in exceptions.items()
        if not issubclass(exception, errors) and name not in excluded
    )
    # there must be none
    assert not unclassified, (
        f"python {sys.version_info.major}.{sys.version_info.minor} has builtin exceptions "
        f"that are not classified: {', '.join(unclassified)}; decide whether the evaluation "
        f"of a setting can raise each one, then add it to {{errors}} in "
        f"packages/pyre/calc/evaluation.py, or to the {{reasons}} of this test, with the "
        f"reason it can't"
    )

    # and none of the excluded ones may be a way an evaluation can fail
    overlap = sorted(
        name for name in excluded if name in exceptions and issubclass(exceptions[name], errors)
    )
    # check
    assert not overlap, f"excluded, yet covered by {{errors}}: {', '.join(overlap)}"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
