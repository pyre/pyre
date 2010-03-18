# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
import stat

from .Recognizer import Recognizer

from .BlockDevice import BlockDevice
from .CharacterDevice import CharacterDevice
from .Directory import Directory
from .File import File
from .NamedPipe import NamedPipe
from .Socket import Socket


class StatRecognizer(Recognizer):
    """
    This class provides support for sorting out filesystem entries based on the lowest level of
    metadata available: the actual representation on the hard disk.

    This recognizer uses os.stat for discovering the entries in a given directory. Therefore,
    it handles symbolic links transparently.
    """


    # interface
    def recognize(self, entry):
        """
        The most basic file recognition: convert the name of a file into an Node descendant
        and decorate it with all the metadata available on the disk.
        """

        # pull the information from the hard filesystem
        meta = os.stat(entry)
        mode = meta.st_mode

        # walk through the cases
        if stat.S_ISREG(mode):
            return File(uri=entry, info=meta)
        elif stat.S_ISDIR(mode):
            return Directory(uri=entry, info=meta)
        elif stat.S_ISSOCK(mode):
            return Socket(uri=entry, info=meta)
        elif stat.S_ISBLK(mode):
            return BlockDevice(uri=entry, info=meta)
        elif stat.S_ISCHR(mode):
            return CharacterDevice(uri=entry, info=meta)
        elif stat.S_ISFIFO(mode):
            return NamedPipe(uri=entry, info=meta)

        import journal
        msg = "unknown file type: mode={0}".format(mode)
        return journal.firewall("pyre.filesystem").log(msg)


# end of file 
