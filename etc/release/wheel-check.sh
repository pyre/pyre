#!/usr/bin/env bash
# -*- bash -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# check what a pyre wheel delivers, in a throwaway environment that holds nothing but python: the
# compiled extensions it ships and the bindings the packages publish, which implementation of the
# journal answers, the templates {smith.pyre} uses, and a toy built against the headers and the
# libraries it installs
#
#   usage: wheel-check.sh {wheel} {python version} {c++ compiler}
#
# the environment is made and removed with micromamba

# the wheel, with its full path, since the checks run elsewhere
wheel="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
# the interpreter it is for
python="$2"
# and the compiler for the toy
cxx="$3"
# the throwaway environment
env="pyre-wheelcheck-$$"
# and the scratch area the checks run in, outside any source tree
scratch="$(mktemp -d)"
# micromamba, wherever this machine keeps it
mm="$(command -v micromamba || echo "$HOME/.local/bin/micromamba")"

# make the environment, with nothing but python and pip
"$mm" create -y -q -n "$env" -c conda-forge "python=$python" pip >/dev/null || exit 1
# find out where it went
prefix="$("$mm" run -n "$env" python -c 'import sys; print(sys.prefix)')"
# install the wheel
"$mm" run -n "$env" pip install -q "$wheel" || exit 2
# say what is under test
echo "wheel:  $(basename "$wheel")"
echo "prefix: $prefix"

# the python checks run in the scratch area, with no inherited PYTHONPATH
cd "$scratch"
env -u PYTHONPATH "$mm" run -n "$env" python - <<'EOF'
# support
import importlib
import importlib.metadata
import pathlib

# the files the wheel installed
files = importlib.metadata.distribution("pyre").files
# the compiled extensions among them, by module name, leaving out the libraries the repair tools
# bundled and the files that went to the data tree
extensions = sorted(
    str(f.with_suffix("")).split(".")[0].replace("/", ".")
    for f in files
    if f.suffix == ".so" and not str(f).startswith(("..", "pyre.libs", "pyre/.dylibs"))
)
# import each one
print("extensions:")
for name in extensions:
    # carefully
    try:
        importlib.import_module(name)
        print(f"  ok      {name}")
    # and report the ones that fail
    except Exception as error:
        print(f"  FAILED  {name}: {type(error).__name__}: {error}")

# the bindings as the packages publish them
import pyre, journal

print("bindings:")
print(f"  pyre.libpyre        {pyre.libpyre is not None}")
print(f"  journal.libjournal  {journal.libjournal is not None}")
# and the optional ones
for package, attribute in (("pyre.h5", "libh5"), ("gsl", "gsl"), ("mpi", "libmpi")):
    # carefully, since a package may refuse to import without its bindings
    try:
        module = importlib.import_module(package)
        print(f"  {f'{package}.{attribute}':<20}{getattr(module, attribute, None) is not None}")
    # and report the ones that do
    except Exception as error:
        print(f"  {f'{package}.{attribute}':<20}FAILED: {type(error).__name__}: {error}")

# the implementation of the journal that answers: the bindings, or the pure python one
print(f"journal implementation: {type(journal.info('check')).__module__}")

# the templates {smith.pyre} makes projects from
templates = pathlib.Path(str(pyre.prefix)) / "share" / "pyre" / "templates"
print(f"pyre.prefix: {pyre.prefix}")
print(f"templates: {templates} {'present' if templates.is_dir() else 'MISSING'}")
EOF

# make a project from the templates
env -u PYTHONPATH "$mm" run -n "$env" smith.pyre --project.name=toy >smith.log 2>&1
# smith commits and tags the project only after it has generated every file, so the tag is how
# a complete project is recognized; a folder alone may be what a failure left behind
if git -C toy rev-parse -q --verify v0.0.1 >/dev/null 2>&1; then
    # count what it committed, which leaves out anything that should not be in the project
    echo "smith.pyre: made and committed the project toy, $(git -C toy ls-files | wc -l | tr -d ' ') files"
# otherwise
else
    # say so, and show why
    echo "smith.pyre: FAILED"
    tail -5 smith.log
fi

# a toy that writes to the journal
cat >hello.cc <<'EOF'
#include <pyre/journal.h>
int main() {
    auto channel = pyre::journal::info_t("toy.hello");
    channel << pyre::journal::at() << "hello from a pyre wheel" << pyre::journal::endl;
    return 0;
}
EOF
# the libraries of the wheel land in {lib}, or in {lib64} on some linux layouts
libdir="$prefix/lib"
[ -e "$prefix/lib64/libjournal.so" ] && libdir="$prefix/lib64"
echo "toy: libraries in $libdir"
# build it against the headers and the libraries the wheel installed
if "$cxx" -std=c++20 -I"$prefix/include" -L"$libdir" hello.cc -ljournal -Wl,-rpath,"$libdir" -o hello >cxx.log 2>&1; then
    # say so
    echo "toy: compiled and linked"
    # and run it
    if ./hello >run.log 2>&1; then
        echo "toy: ran"
    else
        echo "toy: FAILED to run"
        head -3 run.log
    fi
# otherwise
else
    # show why not
    echo "toy: FAILED to build"
    tail -5 cxx.log
fi

# remove the scratch area
cd /
rm -rf "$scratch"
# and the environment
"$mm" env remove -y -q -n "$env" >/dev/null
echo "removed $env"


# end of file
