#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the editor reports its backend, and that a request to edit under a scalar or
with an empty path is refused
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # the editor knows whether its backend is there
    available = editor.available()
    # if it is not
    if not available:
        # building one must fail with the right complaint
        try:
            # try
            pyre.config.newYamlEditor()
        # if it complained the way it should
        except editor.MissingBackendError as error:
            # check that the package is named
            assert error.package == "ruamel.yaml"
        # if it didn't complain
        else:
            # that's a bug
            assert False, "unreachable"
        # nothing else to check
        return None
    # otherwise, build an editor over some text
    editor = pyre.config.newYamlEditor(text="scalar: 1\n")
    # an empty path names nothing
    try:
        # try
        editor.set(value=1)
    # if it complained the way it should
    except editor.EditingError:
        # all good
        pass
    # if it didn't complain
    else:
        # that's a bug
        assert False, "unreachable"
    # a key cannot be placed under a scalar
    try:
        # try
        editor.set("scalar", "key", value=1)
    # if it complained the way it should
    except editor.EditingError:
        # all good
        pass
    # if it didn't complain
    else:
        # that's a bug
        assert False, "unreachable"
    # a document without a location cannot be saved without one
    try:
        # try
        editor.save()
    # if it complained the way it should
    except editor.EditingError:
        # all good
        pass
    # if it didn't complain
    else:
        # that's a bug
        assert False, "unreachable"
    # all done
    return editor


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
