#!/usr/bin/env sh

# match one or more ::-separated identifiers which may be templates,
# but must start at column zero,
# followed by an identifier which ends with an open-parenthesis
# insert a break between these groups, after the final ::
sed 's/^\(\([A-Za-z][A-Za-z0-9_ <>,]*::\)\+\)\([A-Za-z0-9_]*\)(/\1\n\3(/g' $*
