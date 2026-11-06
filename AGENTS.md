<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# Contributing to pyre

These are the conventions of the repository. They apply to everyone who contributes, person or
agent, and this file is meant to be complete: everything a contribution is held to is written
here. The mechanical rules are checked on every pull request by
`.github/workflows/pr-conventions.yaml`; run the same checks before pushing:

```
pip install -r etc/ci/conventions/requirements.txt
python3 etc/ci/conventions/check.py --base origin/main
```

The checker examines the files touched by the commits between the base and `HEAD`, reading them
from disk: run it after committing, since before the first commit it sees nothing and reports
every check as passing. A word it flags that is spelled correctly goes in
`etc/ci/conventions/codespell-words.txt`, and a line that is right as it stands in
`etc/ci/conventions/codespell-lines.txt`.

The rest of the rules are matters of judgment, and reviewers hold contributions to them.

## The attitude

The goal of every change is to leave the code better than it was. A problem found along the way,
whether a failing test, a file that `black` or `clang-format` would change, a stale comment, or a
latent bug, is not dismissed because it predates the change at hand. It is fixed, or, when fixing
it would derail the work, recorded in an issue with everything that is known about it: the
symptoms, how to reproduce it, what was ruled out, the suspected cause, and where in the code it
lives. A defect in shared code is never worked around silently in a client; it is fixed where it
lives, or raised.

Every file a change touches is brought up to the current rules: its formatting, its preamble and
closing marker, the year in its copyright line, its comments, and any deprecated interface it
uses. The code base spans decades, so new code follows these rules rather than the older code
around it.

pyre is a framework whose clients are mostly outside this repository. Every published interface
is treated as load bearing, whether or not anything in the repository calls it; how often a
feature is used here says nothing about how important it is, and no interface is labeled "older",
"legacy" or "superseded" on that basis. A capability added at one tier is carried through every
sibling surface that publishes the same vocabulary, the library, its bindings, and the python
package, or the pull request says which surface is left out and why.

pyre provides mechanism and leaves policy to the application. It records, checks and reports, and
never decides on the application's behalf whether to stop: a misconfigured application must still
be able to start, if only to report what is wrong with it.

When something fails, suspect the environment before the code: the build context, the paths, the
installed versions, and which installed files the failing step actually picked up. A failure the
environment causes is fixed in the environment.

## File layout

Every file opens with the same preamble, in the comment syntax of its language, and ends with a
closing marker:

```python
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# ... the file ...


# end of file
```

- The first line names the mode of the file, in lower case and with one spelling per language:
  `python`, `c++`, `c`, `web` (JavaScript and TypeScript), `makefile`, `yaml`, `toml`, `cmake`,
  `bash`, `latex`, `markdown`, `mdx`, `html`, `xml`, `css`, and `pyre` for `.pfg` files.
- The comment syntax is the language's own: `#` for python, yaml, toml, cmake, bash and
  makefiles, `//` for C++ and JavaScript, `/* ... */` for CSS and C. Markdown has no comments, so
  a `.md` file carries the preamble as a single HTML comment block and ends with
  `<!-- end of file -->`. An `.mdx` file rejects HTML comments, so it carries the same text in a
  JSX comment, `{/* ... */}`, and ends with `{/* end of file */}`.
- A shebang, an `<?xml ...?>` declaration, or a doctype stays above the preamble.
- The author line names the author of the file; new files by other contributors carry their own
  name.
- The copyright range ends in the current year in every file a change adds or modifies.
- Two blank lines follow the preamble, then the imports, then the code. In `.h` and `.icc` files a
  single blank line separates the preamble from `#pragma once`.
- Every file ends with two blank lines and the closing marker, followed by a single newline; for
  python, `black` has the last word, so a module that ends with imports keeps one blank line
  before the marker.
- One blank line separates top level definitions, and two separate classes.
- No decorative separator comments, no placeholder sections, no empty blocks, and no
  `TODO: implement me`.

The directory layout mirrors the namespaces: `lib/pyre/grid/` holds `pyre::grid`, `extensions/`
the bindings, `packages/` the python packages, `tests/` the test suites, `etc/` the support files
for development and CI, and `share/` what end users need at run time. Each namespace directory
holds a `forward.h` and a `public.h`, and has a sibling header named after it, such as
`lib/pyre/grid.h` beside `lib/pyre/grid/`, that includes its `public.h`, so a client includes
`<pyre/grid.h>` for the whole of `pyre::grid`.

## Comments and docstrings

Comments are read first, as the specification, and then compared against the code; a mismatch
between the two is how defects are found. A reviewer who has to repair the narrative of a
contribution before it can be merged has to review it twice, so the comments arrive right:

- **One comment per statement.** Nearly every statement gets a comment on the line above it: each
  assignment, call, branch, and return. A statement that spans several lines gets one comment for
  the whole statement. The `narrative` check holds every python file a change touches to this
  rule, the older parts of the file included. The count is the floor, not the goal: read in
  order, the comments must form a coherent paragraph that says what the code is meant to
  accomplish.
- **Intent, not mechanics.** A comment says what the step is supposed to accomplish ("fold in the
  contribution of this axis", "make a channel"), never a paraphrase of the syntax ("multiply the
  cells by the extents"). Labels such as "get reset color", "maximum length" or "header marker"
  name the line instead of explaining it, and are rejected.
- **What a thing is, never what it is not.** "the name the application registered" rather than
  "no metadata".
- **About its own statement.** A comment does not name neighboring code that may change; it
  explains the step it sits above, and leaves the analysis of other code to the comments there.
- **Timeless.** Comments describe what the code is and does now. No history: not "now", "used to",
  "no longer", "formerly", "replaces"; no story of the fix, the client that uncovered a bug, or
  the alternatives considered. That belongs in the pull request.
- **Spelled correctly.** The narrative is the specification; spell check it as part of every
  cleanup.
- **Every function ends with an explicit return**, even when it returns nothing, under a comment
  that tells the reader what is handed off (`# hand off the size`). When there is nothing in
  particular, `# all done` above a bare `return` in python, or `// all done` above `return;` in
  C++, serves.

### Docstrings

Every module level function, class, and method has a docstring. It is the public documentation:
one or two sentences say what the function does for its caller, in the same voice as the
comments, and a longer explanation is for behavior that is genuinely involved. The motivation for
the code and the mechanics of how it works are for the maintainer, and go in the narrative, next
to the statement they explain. Docstrings use the expanded form, with the opening and closing
quotes on lines of their own, never a one-line docstring. Parameters are named in braces,
`{name}`, rather than in a parameter list:

```python
def locate(self, product):
    """
    Build a uri to the given {product}
    """
```

The docstring of an exception, and the message it carries, state the condition that raised it:
"Exception raised when the file does not exist". What the code does afterwards belongs to that
code.

### Messages for end users

Errors and warnings that end users see are prose too, written for people who must understand what
went wrong. They use plain English and the user's own terms: the setting, the file, the value they
typed. They say what is wrong and stop, with no suggested remedy. Framework vocabulary, such as
coerce, node, protocol, binding, or unresolved, stays out of them, and so does the name pyre,
since applications own these messages. Firewalls, which are meant for developers, may stay
technical.

### C++

- A declaration in a header gets a comment above it that says what it is or does, written as a
  sentence fragment in the first person of the class where that reads naturally ("my creation
  property list", "the chunk that holds the cell at {origin}"). Longer comments explain the
  contract: what comes back when the answer does not exist, what a caller must not assume.
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

- Top level blocks, such as a group of related free functions or a table of explicit
  instantiations, get a comment above them that says what the block holds.

## pyre components

Drivers, scripts and tools are pyre applications. Their options are traits, their output goes to
journal channels, and their timings use `pyre.timers`; they do not use `argparse`, `print` for
diagnostics, or `time.perf_counter`. The command line of a pyre application is its list of
traits.

A protocol declares the obligations of its implementers:

```python
# support
import pyre


# the requirements of an archive
class Archive(pyre.protocol, family="pyre.archives"):
    """
    The requirements of an archive
    """

    # the default implementation
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The suggested implementation of the {Archive} protocol
        """
        # pick the local one
        from .Local import Local

        # and hand it off
        return Local

    # obligations
    @pyre.provides
    def locate(self, product):
        """
        Build a uri to the given {product}
        """
```

- A protocol inherits from `pyre.protocol` and takes a `family`, a dotted name that mirrors the
  package and usually ends in a plural noun. Its obligations are marked with `@pyre.provides`, and
  their bodies are empty: the docstring is the specification.
- A protocol nominates its default implementation through `pyre_default`.
- A component inherits from `pyre.component`, takes a `family`, usually ending in a singular noun,
  and names the protocol it satisfies with `implements`. The methods that fulfil obligations are
  marked with `@pyre.export`; other public methods get no decorator.
- One protocol or component per file, named after the class. Protocols live in a `protocols/`
  subpackage, which publishes each one with a lower case initial: `Archive` as `archive`.
- Traits are declared at class level, and their metadata are set one per line after the
  declaration, never as constructor arguments:

  ```python
  # the region where the data reside
  region = pyre.properties.str()
  region.default = "us-west-2"
  region.doc = "the region where the data reside"
  ```

  The common metadata are `default`, `doc`, `aliases`, `converter`, `normalizer`, and `validator`.
- Custom traits derive from `pyre.traits.Trait`, so the component machinery can harvest them. The
  trait classes are reachable through `import pyre`; never `import pyre.traits.Facility` or its
  siblings.
- Configuration values are traits, never constants in the code, so users can override them. A
  component never assumes that a trait holds its default after construction: the configuration
  store may have supplied a value before the component was built.
- Package names and the families that protocols and components register are framework names.
  Configuring a value at one, or naming an instance after one, fires a firewall; the colliding
  code is the bug, and it is fixed there rather than accommodated in pyre.
- Behavior stays on the class even when it uses no instance state: methods are where derived
  classes override behavior. Moving one to module level needs a positive reason, stated in the
  pull request.
- A project built on pyre re-exports pyre's names from its own top level package, and its code
  reaches them through that package.

## Python

- Type hints on function signatures are strongly encouraged.
- Keyword arguments throughout: every constructor accepts `**kwds` and chains up with
  `super().__init__(**kwds)`, repeating a consumed argument in the call only when a superclass is
  known to take the same keyword. Prefer keyword only arguments where a positional call would be
  ambiguous.
- One class per module, named after the file. Older modules that hold several classes are not
  precedent.
- Names are whole words, never abbreviations; names of several words use camelCase
  (`relativePath`); a container takes a plural noun and its loop variable the singular:
  `for candidate in candidates`.
- Paths are `pyre.primitives.path`, never `pathlib.Path` or `os.path`.
- Exceptions are specific: no bare `except:`, no `except Exception:`. Build a hierarchy of
  meaningful exceptions rather than reusing generic built ins; new exception classes are cheap.
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
- Lines go to an open file with `print(text, file=stream)`, and a blank line with
  `print(file=stream)`, rather than `stream.write(text + "\n")`.
- Stand-ins in tests get plain names, without `Fake` or `Mock` prefixes.
- Format with `black` at the line length in `pyproject.toml`.

## journal

All diagnostics go through journal, in python and in C++, never through the `logging` module.

| channel    | active by default | fatal by default |
|------------|-------------------|------------------|
| `debug`    | no                | no               |
| `info`     | yes               | no               |
| `warning`  | yes               | no               |
| `error`    | yes               | yes              |
| `firewall` | yes               | yes              |

- `error` reports a mistake a correct user can fix: a bad configuration value, a missing input, an
  environment that is not set up. `firewall` reports a condition that only a defect in the code can
  produce. Before reaching for a firewall, ask whether a correct user could trigger it; if so, it is
  an error.
- Never assume that an `error` or a `firewall` is fatal: whether it stops the program is the
  user's choice. After one fires, the code does whatever is reasonable to carry on past the
  failure, such as returning a safe value or skipping the item, and never proceeds as if nothing
  had happened.
- Channel names are dotted and rooted at the project, `pyre.h5.file`, and name the activity being
  reported rather than the class doing the work, so that a workflow spread across several
  components can be followed on one channel. They are chosen deliberately, never derived from
  `__name__` or a family.
- Open a fresh channel at the call site every time; never cache one in an attribute.
- In C++, an entry opens with `pyre::journal::here()`, which records where the condition was
  detected, and closes with a bare `pyre::journal::endl`. `at()` is an alias of `here()`;
  `here()` is preferred.
- `__HERE__` and `endl(__HERE__)` are forbidden outside `lib/journal`, which keeps them for older
  clients and for C and Fortran; repairing a non-compliant source file is part of its cleanup.
- `pyre::journal::newline`, `indent` and `outdent` structure an entry of several lines, and each
  `<<` segment sits under a comment that says what it contributes:

  ```cpp
  // make a channel
  auto channel = pyre::journal::error_t("pyre.grid.layout");
  // report
  channel
      // where
      << pyre::journal::here()
      // what
      << "insufficient memory" << pyre::journal::newline
      // the details
      << pyre::journal::indent << "required: " << required << " cells" << pyre::journal::outdent
      // flush
      << pyre::journal::endl;
  ```

- Spell the error channel in full, `pyre::journal::error_t`: glibc declares an `error_t` of its
  own under `_GNU_SOURCE`, so a bare name or a using declaration at file scope breaks the linux
  builds.

## C++

- One class per trio of files: `Foo.h` for the declarations, `Foo.icc` for the inline definitions,
  `Foo.cc` for the rest. `Foo.h` ends by including `Foo.icc`, and `Foo.icc` opens with an include
  of `Foo.h` under a `// my declarations` comment.
- Each namespace directory has a `forward.h` with the forward declarations of its classes, which
  is also where the namespace is set up, and a `public.h` that includes its public headers and
  those of its subdirectories. Namespaces are not reopened elsewhere.
- `#pragma once`, never include guards.
- A header includes only what its declarations need, and forward declares the rest. A `.cc` file
  includes its own header first, then the standard library, then third party headers, then local
  ones.
- Every header compiles on its own. Check it through a wrapper translation unit that includes it,
  since clang ignores `#pragma once` in the main file.
- No two installed headers may be byte identical: gcc treats such headers as one file under
  `#pragma once`, so generated headers name the namespace they serve.
- Every class declares, at the top of its public types, `using self_type = ...;` under a `// me`
  comment, `using super_type = ...;` under `// my superclass` when it has a base class, and an
  alias with a `_type` suffix for every type in its interface. Aliases at namespace scope take the
  `_t` suffix.
- The full set of special members is declared explicitly, `= default` or `= delete`; the
  destructor is always declared.
- Declarations are grouped, in order, as constructors, destructor, operators, interface,
  implementation, and data, each group under a brief comment label such as `// metamethods` or
  `// interface`.
- Private members and implementation details start with an underscore. Functions and methods are
  `camelCase`, types are `PascalCase`, and template parameters follow `{concept}T`, such as
  `gridT` or `cellT`.
- `const` wherever possible, and `auto` wherever the type is clear from context.
- Class declarations in headers use the fully qualified name, `class pyre::h5::DataSet`, and so do
  definitions in `.icc` and `.cc` files, which never open a namespace block. Never
  `using namespace` in a header.
- A project's version lives in a nested namespace, `{project}::version`, and is returned as a
  `version_t` struct whose fields `major`, `minor`, `micro` and `revision` are read by name, never
  as a tuple.
- Template overloads are registered through explicit instantiation lists, one instantiation per
  line, grouped by category under a comment label.
- Format with `clang-format` and the `.clang-format` at the top of the repository.

## Bindings

- Each binding file includes `external.h`, then `forward.h`. Helper templates are `inline` and
  live in a block of the helper namespace above the main binding function, which is named after
  the entity it binds and defined with its fully qualified name:

  ```cpp
  namespace pyre::py::flow {
      // register the channel factories for one cell type
      template <typename cellT>
      inline void complexChannels(catalog_t & catalog) { ... }
  }

  // bind the factories
  void
  pyre::py::flow::factories(py::module & m) { ... }
  ```

- One `py::class_<T>` per binding function, assigned to `cls`. Each `cls.def(...)` puts its
  arguments on separate lines, each under a comment that says what it is:

  ```cpp
  cls.def(
      // the name
      "read",
      // the implementation
      &DataSet::read,
      // the signature
      "data"_a, "origin"_a, "shape"_a,
      // the docstring
      "fill {data} with the tile @{origin}+{shape}");
  ```

  `def_property_readonly` and `def_property_readonly_static` follow the same layout. Template
  overloads are registered at the end of the binding function, grouped by category.
- Docstrings refer to parameters in braces, `{name}`.
- No C++ exception crosses into python unhandled: recoverable errors go to a
  `pyre::journal::error_t` and return a safe default, and conditions that indicate a bug go to a
  `pyre::journal::firewall_t`.

## Optional dependencies

Much of pyre depends on external packages that a given machine may or may not have: CUDA, MPI,
HDF5, libpq, GSL, and others. A build that finds one of them includes the support for it, and a
binary distribution carries that support to machines that may lack the package. Whatever was
present when pyre was built, the installed assets must work on a machine where any optional
package is missing:

- **The core never depends on an optional package.** `libjournal`, `libpyre`, and the `journal`
  and `pyre` extension modules link no optional package, directly or through another library,
  and `import pyre` works on a machine that has none of them. This holds for the mm and the
  cmake builds alike, and for every configuration either one can produce.
- **Each optional package gets shared objects of its own.** The support for a package lives in a
  library such as `libpyre-h5` and in the extension module that binds it; they link that package
  and no other optional one, and they are loaded only when the capability is used. A capability
  is never folded into the core bindings behind a compile time flag, because a flag decides what
  gets built, not what the machine running it has.
- **Support that needs two optional packages** goes in a shared object that needs both, rather
  than into the extension of either one: routines that take MPI communicators do not belong in
  the GSL extension, which would then be unusable on a machine that has GSL but no MPI.
- **Core headers stay clean.** A header of the core library does not include the headers of an
  optional package, even conditionally; the code that needs them lives with the package's own
  library.
- **A missing capability says so.** When the extension module of an optional package cannot be
  loaded, the python package that fronts it raises a specific exception that names the missing
  package, rather than letting its clients fail later on an attribute of `None`.

To check a build, list what the core shared objects need, with `readelf -d` on linux or
`otool -L` on macOS: no optional package may appear.

## Tests

- Tests are small, and each one checks one thing. Drivers are split by behavior rather than by
  class, and each is named so that its failure states the hypothesis: `requirement_ordering.py`
  failing points at ordering before any file is opened.
- A passing test is silent: any output is a failure.
- A driver keeps the files it produces, so they can be inspected after a run. Their removal is
  registered with the harness instead, in both builds: in mm, with a clean entry in the suite's
  `.mm/<suite>` file, such as `tests.pyre.pkg.nexus.fork_leave.clean := fork_leave.retired.*`;
  in cmake, with `pyre_test_python_cleanup` or `pyre_test_driver_cleanup` next to the test's
  registration. A driver never removes its own products, whether with `unlink`, `shutil.rmtree`,
  or a `tempfile.TemporaryDirectory`.
- Run the suite's clean target before staging. A file it leaves behind means a missing clean
  entry, which is fixed in the suite rather than by deleting the file.
- A failing driver that asserts intended behavior is a finding: the code must be fixed, and the
  driver is not adjusted to silence the error.
- Tests never assume that memory nobody wrote holds zeros.
- A check worth making once is worth keeping: add it to the test suite rather than running a
  throwaway script.
- A suite is green only when its tests ran: count them.
- C++ drivers check with `assert`; mm compiles test drivers with assertions enabled in every build
  mode.

## Building and testing

- The build system is [mm](https://github.com/aivazis/mm). The `Make.mm` files are vestiges; do
  not create, edit, or rely on them.
- **Build and test with mm before opening a pull request.** A contribution is compiled and its
  tests are run locally, with `mm` and then `mm tests`, or at least the suites it touches, before
  the pull request is opened. A pull request is not the place to find out whether the code
  compiles.
- **Keep the cmake build in step.** pyre also builds with cmake, and the cmake build lists its
  files explicitly: every compiled source (`.cc`, `.cu`) in the `target_sources` of its
  component in `.cmake/pyre_*.cmake`, and every test in `.cmake/pyre_tests_*.cmake`, with
  `pyre_test_driver` for a C++ driver, `pyre_test_python_testcase` for a python one, and the
  cleanup of the files a test leaves behind. A contribution that adds, renames, or removes a
  source or a test updates those lists in the same pull request; mm finds files on its own, so
  an mm build that passes says nothing about the cmake one. Headers are picked up by directory.
  The cmake build runs on every pull request, in `pr-cmake`.
- Build in an environment whose libraries do not compete with the ones being built: a binary
  looks up all of its libraries in one ordered list of directories, so a second copy of a library
  anywhere on that list, such as another `pyre` or a separately built `hdf5`, can be loaded in
  place of the one the build linked against, whatever the order.
- Test against what `mm` installs, never against the source tree. `mm builder.info` reports the
  install prefix; check it before relying on a result, and point `PATH` and `PYTHONPATH` at its
  `bin` and `packages` directories for anything run outside mm. Running python with the working
  directory inside `packages/` or `tests/` imports the uninstalled sources and litters the tree
  with `__pycache__`.
- `mm tests` runs every test suite, `mm <suite>` runs one, `mm tests.<stem>.<directory>` runs the
  tests in one directory, such as `mm tests.pyre.pkg.ipc`, and a single test runs from its own
  directory as `mm <name>`.

## Commits

- Every commit message is a single line, `area: what the commit does`, where the area is a path,
  a package, or a C++ namespace: `pyre.h5: a file reports its size`, `tests: ...`,
  `pyre::grid: ...`. No body, and no trailers, signatures or attribution. The reasoning goes in
  the pull request.
- A commit that only cleans up has the cleanup as its subject, `<area>: cosmetics` for formatting,
  preambles and interfaces, `<area>: narrative improvements` for comments and docstrings; a commit
  that carries such cleanup alongside its change ends its subject in `; cosmetics` or
  `; narrative improvements`.
- When the formatters change files the work did not touch, revert those changes, commit the work,
  and then format the whole tree in a commit of its own.
- Commit in coherent batches by layer: the library, the bindings, the python package, the tests,
  and the build configuration are separate commits, each of which builds on its own.
- Stage files by name. Look at the index before staging, and read back what is staged before
  committing; never `git add -A`, `git add .`, or `git commit -a`.
- Work that is not in reasonable shape stays uncommitted; a commit is not the place to admit that
  a fix is unfinished.
- A commit marked `[skip ci]` is never the last one in a batch that needs testing.
- Run the conventions checker after committing and before pushing.

## Pull requests and documentation

A change to a published interface starts with an issue that describes the design, so the design
can be settled before the code is written.

Pull request descriptions and documentation are written for an experienced, educated audience,
in plain prose that reads like good reference documentation.

- Describe the work; do not sell it. No praise of the change and no editorializing adjectives:
  not "powerful", "elegant", "clean", "robust", "seamless", "blazing fast".
- Open with a short summary of what the work does and why, then give each component a section of
  its own that says what it does.
- Stay on the change: what it does, why the code needed it, and what the tests check. Leave out
  incidental history, such as where the code came from, how many attempts it took, or which branch
  it was salvaged from, and claims about the code that may not last, such as an interface being
  unused.
- Write full sentences in a measured tone. Explain a term of art once, where it first appears.
- No startup vocabulary or mannerisms: not "ship", "unlock", "supercharge", "game changer",
  "leverage", "under the hood", "out of the box". No punchy fragments, no staccato sequences of
  short sentences, no emoji, no exclamation marks.
- Pull request descriptions carry no signatures, session links, or attribution trailers.
- Prefer independent pull requests off `main`. A pull request stacked on another names the order
  in which they merge.
- A pull request that resolves an issue links it with a closing keyword, `Closes #387`.


<!-- end of file -->
