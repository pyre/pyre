#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A yaml file with a tag the reader does not know, a python tag among them, is reported as a
decoding error that says where the tag is, and none of its settings are applied; a merge key,
whose tag the reader folds into the map it builds, is not refused
"""


def test() -> None:
    """
    Load a file with a python tag, a file with an unknown tag and a file with a merge key, and
    check what is reported and what is applied
    """
    # support
    import journal
    import pyre
    from pyre.config.exceptions import DecodingError

    # get the executive
    executive = pyre.executive
    # and its nameserver
    nameserver = executive.nameserver
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.config.yaml.tags")
    # the files i load are refused on purpose, and the executive says so; the checks below
    # read its pile of errors, so its warnings are not needed on the screen
    journal.warning("pyre.configuration").device = journal.trash()

    # go through the kinds of tag, and the way each file spells its tag
    for kind, tag in [
        ("python", "!!python/object/apply:builtins.len"),
        ("unknown", "!extend"),
    ]:
        # the file
        uri = f"yaml_{kind}_tag.yaml"
        # count the errors
        errors = len(executive.errors)
        # load it
        executive.loadConfiguration(uri=uri)
        # get the errors it added
        found = executive.errors[errors:]
        # there must be exactly one decoding error
        if len(found) != 1 or not isinstance(found[0], DecodingError):
            # if not, say so
            channel.line(f"loading {uri!r} did not report one decoding error")
            # indent the details
            channel.indent()
            # show the errors that came back
            channel.line(f"errors: {[f'{type(error).__name__}: {error}' for error in found]}")
            # and where to look
            channel.line("look in: config/yaml/Parser.py")
            # done with the details
            channel.outdent()
        # that names the file and the line of the tag
        elif uri not in str(found[0]) or "line=13" not in str(found[0]):
            # if not, say so
            channel.line(f"the error from {uri!r} does not say where the tag is")
            # indent the details
            channel.indent()
            # show the error
            channel.line(f"error: {found[0]}")
            # done with the details
            channel.outdent()
        # and says which tag it refuses
        elif f"the tag '{tag}' is not supported" not in str(found[0]):
            # if not, say so
            channel.line(f"the error from {uri!r} does not name the tag {tag!r}")
            # indent the details
            channel.indent()
            # show the error
            channel.line(f"error: {found[0]}")
            # done with the details
            channel.outdent()
        # go through the settings in the file
        for name in ["applied", "called", "extended"]:
            # carefully
            try:
                # look up the setting
                value = nameserver[f"tags.{kind}.{name}"]
            # if it is not there
            except nameserver.UnresolvedNodeError:
                # all is well
                pass
            # if it is
            else:
                # say so
                channel.line(f"the refused {uri!r} set {name!r} to {value!r}")

    # a merge key carries a tag of its own that the reader folds into the map it builds, so the
    # file that holds one is not refused; count the errors
    errors = len(executive.errors)
    # load it
    executive.loadConfiguration(uri="yaml_merge_tag.yaml")
    # if it was refused
    if executive.errors[errors:]:
        # say so
        channel.line("loading 'yaml_merge_tag.yaml' was refused")
        # indent the details
        channel.indent()
        # show the errors that came back
        channel.line(f"errors: {[str(error) for error in executive.errors[errors:]]}")
        # done with the details
        channel.outdent()
    # if the merge did not happen
    elif (derived := nameserver["tags.merge.derived"]) != {"x": 1, "y": 2}:
        # say so
        channel.line(f"the merge gave {derived!r}")

    # if anything went wrong
    if channel.page:
        # complain
        channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
