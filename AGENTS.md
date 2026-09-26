<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# Contributing to pyre

These are the conventions of the repository. They apply to everyone who contributes, and they
are written so that coding agents, which read this file automatically, can follow them too. The
mechanical ones are checked on every pull request by `.github/workflows/pr-conventions.yaml`;
run the same checks before pushing:

```
pip install -r etc/ci/conventions/requirements.txt
python3 etc/ci/conventions/check.py --base origin/main
```

The rest are matters of judgment, and reviewers hold contributions to them.

## The attitude

The goal of every change is to leave the code better than it was. A problem found along the way,
whether a failing test, a file that `black` or `clang-format` would change, a stale comment, or a
latent bug, is not dismissed because it predates the change at hand. It is fixed, or, when fixing
it would derail the work, recorded in an issue with everything that is known about it: the
symptoms, how to reproduce it, what was ruled out, the suspected cause, and where in the code it
lives. A defect in shared code is never worked around silently in a client; it is fixed where it
lives, or raised.

pyre is a framework whose clients are mostly outside this repository. Every published interface
is treated as load bearing, whether or not anything in the repository calls it; how often a
feature is used here says nothing about how important it is.

## File layout

Every source file opens with the same preamble, in the comment syntax of its language, and ends
with a closing marker:

```python
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# ... the file ...


# end of file
```

- The author line names the author of the file; new files by other contributors carry their own
  name.
- The copyright range ends in the current year in every file a change adds or modifies.
- One blank line after the preamble, then the imports, then the code; two blank lines between
  top level definitions; no decorative separator comments; no placeholder sections, empty
  blocks, or `TODO: implement me`.

The directory layout mirrors the namespaces: `lib/pyre/grid/` holds `pyre::grid`, `extensions/`
the bindings, `packages/` the python packages, `tests/` the test suites, `etc/` the support files
for development and CI, and `share/` what end users need at run time.

## Comments

Comments are read first, as the specification, and then compared against the code; a mismatch
between the two is how defects are found. They are therefore dense and complete:

- **One comment line per line of code.** Nearly every statement gets a comment on the line above
  it: each assignment, call, branch, and return. A statement that spans several lines gets one
  comment for the whole statement.
- **Intent, not mechanics.** A comment says what the step is supposed to accomplish ("fold in the
  contribution of this axis", "make a channel"), never a paraphrase of the syntax ("multiply the
  cells by the extents").
- **Timeless.** Comments describe what the code is and does now. No history: not "now", "used to",
  "no longer", "formerly", "replaces"; that belongs in the pull request.
- **Spelled correctly.** The narrative is the specification; spell check it as part of every
  cleanup.
- **Every function ends with an explicit return**, even when it returns nothing: a python function
  ends with `# all done` and a bare `return`, a C++ function returning `void` with `// all done`
  and `return;`.

### Python docstrings

Every module level function, class, and method has a docstring. One or two sentences say what it
does, in the same voice as the comments; a longer explanation is for behavior that is genuinely
involved. Parameters are named in braces, `{name}`, rather than in a parameter list:

```python
def locate(self, product):
    """
    Build a uri to the given {product}
    """
```

### C++

- A declaration in a header gets a comment above it that says what it is or does, written as a
  sentence fragment in the first person of the class where that reads naturally ("my creation
  property list", "the chunk that holds the cell at {origin}"). Longer comments explain the
  contract: what comes back when the answer does not exist, what a caller must not assume.
- Declarations are grouped, in order, as constructors, destructor, operators, interface,
  implementation, and data, each group under a brief comment label such as `// metamethods` or
  `// interface`.
- A definition in a `.icc` or `.cc` file is preceded by a comment line that repeats the purpose
  of the function, followed by the definition with the return type on its own line and the
  fully qualified name on the next:

  ```cpp
  // my size, in bytes
  auto
  pyre::h5::File::bytes() const -> std::optional<hsize_t>
  {
      // make room for the answer
      hsize_t size = 0;
      // ...
      // hand off the size
      return size;
  }
  ```

- Top level blocks, such as a namespace, a group of related free functions, or a table of
  explicit instantiations, get a comment above them that says what the block holds.

## Python

- Type hints on function signatures.
- Keyword arguments throughout: every constructor accepts `**kwds` and chains up with
  `super().__init__(**kwds)`, repeating any argument it consumed so the superclass sees it too.
  Prefer keyword only arguments where a positional call would be ambiguous.
- Paths are `pyre.primitives.path`, never `pathlib.Path`.
- Exceptions are specific: no bare `except:`, no `except Exception:`. Build a hierarchy of
  meaningful exceptions rather than reusing generic built ins.
- f-strings, not `.format()` or `%`.
- Imports in three groups separated by a blank line: the standard library, third party packages,
  and local imports.
- `__init__.py` files publish their names with explicit imports, `from .Foo import Foo`; never
  `__all__`.
- `if __name__ == "__main__":` belongs only in scripts that are entry points.
- An unset value is `None`, never zero: zero is a legitimate value, and `x if x > 0 else default`
  is a bug waiting for the day zero is meant.
- Do not probe for capabilities with `hasattr` or `getattr` to work around a missing method or an
  older version of a dependency. A method that some implementations of a protocol lack is a gap
  in the protocol: make it an obligation and implement it.
- Logging goes through `journal`, never the `logging` module. Open a fresh channel at the call
  site, name it after the activity rather than the class (`pyre.h5.file`, not the module name),
  and stop after a `firewall` or `error` fires.
- Format with `black` at the line length in `pyproject.toml`.

## C++

- One class per trio of files: `Foo.h` for the declarations, `Foo.icc` for the inline definitions,
  `Foo.cc` for the rest; `Foo.h` ends by including `Foo.icc`, and `Foo.icc` opens by including
  `Foo.h`, so every header stands on its own.
- Each namespace directory has a `forward.h` with the forward declarations of its classes, which
  is also where the namespace is set up, and a `public.h` that includes its public headers and
  those of its subdirectories.
- `#pragma once`, never include guards.
- A header includes only what its declarations need, and forward declares the rest. A `.cc` file
  includes its own header first, then the standard library, then third party headers, then local
  ones.
- Every class declares, at the top of its public types, `using self_type = ...;`, and
  `using super_type = ...;` when it has a base class, and an alias with a `_type` suffix for
  every type in its interface.
- The full set of special members is declared explicitly, `= default` or `= delete`; the
  destructor is always declared.
- Private members and implementation details start with an underscore. Functions and methods are
  `camelCase`, types are `PascalCase`, and template parameters follow `{concept}T`, such as
  `gridT` or `cellT`.
- `const` wherever possible, and `auto` wherever the type is clear from context.
- Class declarations in headers use the fully qualified name, `class pyre::h5::DataSet`; `.icc`
  and `.cc` files open the namespace explicitly; never `using namespace` in a header.
- journal entries start with `pyre::journal::at()` for the location and end with a bare
  `pyre::journal::endl`; `endl(__HERE__)` is being retired.
- Format with `clang-format` and the `.clang-format` at the top of the repository.

## Bindings

- Each binding file includes `external.h`, then `forward.h`; helper templates live in the local
  namespace above the main binding function, which is named after the entity it binds.
- One `py::class_<T>` per binding function, assigned to `cls`. Each `cls.def(...)` puts its
  arguments on separate lines, each under a comment that says what it is: the name, the
  implementation, the signature, the docstring.
- Docstrings refer to parameters in braces, `{name}`.
- No C++ exception crosses into python unhandled: recoverable errors go to a
  `pyre::journal::error_t` and return a safe default, and conditions that indicate a bug go to a
  `pyre::journal::firewall_t`.

## Building and testing

- The build system is [mm](https://github.com/aivazis/mm). There is also a cmake build, kept in
  step by listing new sources and tests in `.cmake/`. The `Make.mm` files are vestiges; do not
  create, edit, or rely on them.
- Test against what `mm` installs, never against the source tree: `mm builder.info` shows where
  the installed files are, and running python with the working directory inside `packages/` or
  `tests/` imports the uninstalled sources and litters the tree with `__pycache__`.
- `mm tests` runs every test suite, and `mm <suite>` runs one; a single test runs from its own
  directory as `mm <name>`. A passing test is silent: any output is a failure.
- Tests are small, and each one checks one thing. A test that leaves files behind registers them
  with the clean target of its suite (`.mm/*.tests`) and with the cmake cleanup, so
  `mm tests.clean` removes them.
- A check worth making once is worth keeping: add it to the test suite rather than running a
  throwaway script.
- Tests never assume that memory nobody wrote holds zeros.

## Commits

- Every commit message is a single line, `area: what the commit does`, where the area is a path,
  a package, or a C++ namespace: `pyre.h5: a file reports its size`, `tests: ...`,
  `pyre::grid: ...`. No body. The reasoning goes in the pull request.
- Commit in coherent batches by layer: the library, the bindings, the python package, the tests,
  and the build configuration are separate commits, each of which builds on its own.
- Stage files by name. Look at the index before staging, and read back what is staged before
  committing; never `git add -A`, `git add .`, or `git commit -a`.
- A commit marked `[skip ci]` is never the last one in a batch that needs testing.

## Pull requests and documentation

Pull request descriptions and documentation are written for an experienced, educated audience,
in plain prose that reads like good reference documentation.

- Describe the work; do not sell it. No praise of the change and no editorializing adjectives:
  not "powerful", "elegant", "clean", "robust", "seamless", "blazing fast".
- Open with a short summary of what the work does and why, then give each component a section of
  its own that says what it does.
- Leave out incidental history, such as where the code came from, how many attempts it took, or
  which branch it was salvaged from, unless it matters to the reader.
- Write full sentences in a measured tone. Explain a term of art once, where it first appears.
- No startup vocabulary or mannerisms: not "ship", "unlock", "supercharge", "game changer",
  "leverage", "under the hood", "out of the box". No punchy fragments, no staccato sequences of
  short sentences, no emoji, no exclamation marks.
- Pull request descriptions carry no signatures, session links, or attribution trailers.


<!-- end of file -->
