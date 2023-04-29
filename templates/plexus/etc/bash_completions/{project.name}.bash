# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved

# bash completion script for {project.name}
function _{project.name}() {{
    # get the partial command line
    local line=${{COMP_LINE}}
    local word=${{COMP_WORDS[COMP_CWORD]}}
    # ask {project.name} to provide guesses
    COMPREPLY=($({project.name} complete --word="${{word}}" --line="${{line}}"))
}}

# register the hook
complete -F _{project.name} {project.name}

# end of file
