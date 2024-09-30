#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


"""
Version check
"""


def test():
    # access the {{{project.name}}} extension
    from {project.name} import lib{project.name}
    # verify that the static and dynamic versions match
    assert lib{project.name}.version.static() == lib{project.name}.version.dynamic()
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
