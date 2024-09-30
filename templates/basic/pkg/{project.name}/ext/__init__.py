# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# attempt to
try:
    # pull the extension module
    from . import {project.name} as lib{project.name}
# if this fails
except ImportError:
    # indicate the bindings are not accessible
    lib{project.name} = None


# end of file 
