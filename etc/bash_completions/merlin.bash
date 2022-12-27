# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# bash completion script for merlin
function _merlin() {
    # get the partial command line
    local line=${COMP_LINE}
    local word=${COMP_WORDS[COMP_CWORD]}
    # ask merlin to provide guesses
    COMPREPLY=($(merlin complete --word="${word}" --line="${line}"))
}

# register the hook
complete -F _merlin merlin

# end of file
