#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The fileserver tells apart the ways a source can fail to open: a source that is not there, a
folder, and a file it may not read, whether named by a local path or through the virtual
filesystem
"""


def test() -> None:
    """
    Open sources that fail in each way, and check what each one raises
    """
    # support
    import os
    import shutil

    # the scratch folder, named after me so i don't disturb other tests that explore this one
    scratch = "fileserver_open_errors.scratch"
    # start clean
    shutil.rmtree(scratch, ignore_errors=True)
    # make it
    os.mkdir(scratch)
    # put a folder in it
    os.mkdir(os.path.join(scratch, "folder"))
    # and a file nobody may read
    locked = os.path.join(scratch, "locked")
    # by making it
    with open(locked, "w") as stream:
        # with some content
        stream.write("locked\n")
    # and taking away its permissions
    os.chmod(locked, 0)
    # a user who reads it anyway, such as {root}, cannot tell an unreadable file apart
    unreadable = not os.access(locked, os.R_OK)

    # boot pyre now, so that its virtual filesystem finds my scratch folder when it mounts
    # the current directory
    import journal
    import pyre

    # get the fileserver
    fileserver = pyre.executive.fileserver
    # the current directory is explored one level deep when it is mounted, so explore my
    # scratch folder, for the virtual filesystem to see its contents
    fileserver[f"/__pyre/startup/{scratch}"].discover()
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.framework.fileserver")

    # the sources, and the error each one must raise
    cases = [
        ("missing", fileserver.SourceNotFoundError),
        ("folder", fileserver.IsFolderError),
    ]
    # unless i can read anything
    if unreadable:
        # the locked file must be refused for what it is
        cases.append(("locked", fileserver.SourceUnreadableError))
    # go through them
    for name, expected in cases:
        # name each one as a local path and through the virtual filesystem
        for uri in [f"{scratch}/{name}", f"vfs:/__pyre/startup/{scratch}/{name}"]:
            # carefully
            try:
                # open it
                stream = fileserver.open(uri=uri)
            # if it raises the expected error, and not one of its relatives
            except pyre.PyreError as error:
                # if it is the wrong one
                if type(error) is not expected:
                    # say what went wrong
                    channel.line(f"opening {uri!r} raised the wrong error")
                    # and the details
                    channel.indent()
                    channel.line(f"expected: {expected.__name__}")
                    channel.line(f"raised: {type(error).__name__}: {error}")
                    channel.line("look in: framework/FileServer.py, FileServer.open")
                    channel.outdent()
            # if it opens
            else:
                # close it
                stream.close()
                # and say so
                channel.line(f"opening {uri!r} succeeded")

    # restore the permissions of the locked file so it can be removed
    os.chmod(locked, 0o644)
    # and clean up
    shutil.rmtree(scratch)

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
