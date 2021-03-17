#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# the driver
def test():
    """
    Sanity check: attempt to access the package
    """
    # access check
    import {project.name}
    # all done
    return 0


# bootstrap
if __name__ == "__main__":
    # invoke the driver
    status = test()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
