<!-- -*- Markdown -*-
   -
   - michael a.g. aïvázis <michael.aivazis@para-sim.com>
   - (c) 1998-2026 all rights reserved
   -->

# Cutting a release

A release is a git tag on `main`, a GitHub release built on that tag, and the distributions
that follow from it. The version is derived from the tag everywhere: `setuptools_scm` reads it
for the pip distributions, `.cmake/pyre_init.cmake` and `mm` read it through `git describe`, and
the packages get it stamped into their `meta.py`. Nothing in the source tree records the
version, so a release does not begin with a version bump. What follows is the sequence, in the
order it must happen, with the reason for each step and how to check it.

## Before the tag

1. **Main is green.** Every workflow that runs on push (`mm`, `cmake`, `conda`) has passed on
   the tip of `main`. A red run on a runner hiccup is not a blocker, but it must have gone green
   when rerun.

   ```
   gh run list --branch main --limit 6
   ```

2. **No open pull requests are meant for this release.** Anything half landed waits for the
   next one. When cleaning up after a merge, confirm the merge before deleting the branch:
   `gh pr view N --json mergedAt` must show a time, and `git cherry origin/main <branch>` must
   print nothing. A check that prints nothing after a failed fetch has not run; deleting the
   head branch of an unmerged pull request closes it.

3. **The bootstrap pins name the release about to be cut.** Two scripts download the boot
   bundle from the GitHub release when `pyre` is not importable, and each pins the release it
   fetches:

   - `bin/mm` in this repository: `_pyre_release`
   - `mm` in the `mm` repository (`github.com/aivazis/mm`): `_pyre_release`

   Both must name the tag about to be created. The pin cannot be verified until the release
   exists, so this is the one place a version is written ahead of the tag. The README's
   release tarball link (`archive/refs/tags/vX.Y.Z.tar.gz`) is the third.

4. **The declared python floor matches what is tested.** `requires-python` and the
   classifiers in `pyproject.toml`, `find_package(Python ...)` in `CMakeLists.txt`, and the
   wheel matrix in `.github/workflows/pypi-wheels.yaml` agree with one another and with the
   interpreters CI exercises (`.github/workflows/mm.yaml`). The wheel matrix must not build
   for interpreters below the floor.

   To check an interpreter CI does not cover, build against it the way the conda-forge recipe
   does and run its `ctest` command: `micromamba create` an environment from
   `~/dv/login/conda/pyre.yaml` with the interpreter pinned, then configure with
   `-DPython_EXECUTABLE`, `-DPYRE_DEST_PACKAGES`, and the recipe's flags. Two things fail on
   this host and mean nothing for the floor: multi-rank mpi cases hang on macOS unless
   openmpi is told `--bind-to none`, which cmake makes opt-in through
   `PYRE_MPI_OVERSUBSCRIBE`, so exclude `_8$` or set the flag; and `externals/live.py`
   probes the host's package manager, which fails when the manager itself is broken, e.g.
   macports awaiting `port migrate` after an OS upgrade.

5. **The pip path builds.** The release workflows have no pull request gate (`pr-pypi` is
   disabled), so prove the path by hand before tagging:

   - `python -m build --sdist` from a clean checkout produces `dist/pyre-*.tar.gz`
   - `pip wheel --no-deps dist/pyre-*.tar.gz` builds a wheel from that sdist, which is what pip
     does on a host without a matching wheel
   - **the repaired wheel installs and imports.** Run the repair tool `cibuildwheel` runs,
     `delocate-wheel` on macOS or `auditwheel repair` on Linux, on that wheel; install the
     result into a fresh environment that has no pyre; and import `pyre`, `journal`, and
     `pyre.h5`, checking that `pyre.libpyre`, `journal.libjournal`, and `pyre.h5.libh5` are
     not `None`. The repair tools rewrite the paths from the extension modules to the bundled
     shared libraries against the wheel's layout, and a wheel whose layout misleads them
     imports the pure python package and fails at the first extension, which is what every
     v1.13.0 wheel did; nothing short of installing the repaired wheel catches it
   - the `pypi-testpypi` workflow (`workflow_dispatch`, `ref: main`) uploads an sdist to
     TestPyPI; this is the only exercise of the trusted publishing path before the real one

   The uploads authenticate through trusted publishing, so each index must list the workflow
   that publishes to it: on test.pypi.org, `pypi-testpypi.yaml` with environment `testpypi`;
   on pypi.org, `pypi-source.yaml` and `pypi-wheels.yaml` with environment `pypi`. A missing
   entry fails the upload with `invalid-publisher` after the build has succeeded, and only
   the project owner can add one.

   The pypi workflows check out the repository with `fetch-depth: 0` so that `setuptools_scm`
   can see the tag; a shallow checkout yields a `0.1.devN` version. An untagged commit versions
   as `X.Y.Z.devN` with no local `+gHASH` suffix, since the indices refuse local versions; both
   `pyproject.toml` and the `get_version` call in `setup.py` say so, and the two must agree.
   The wheel matrix names runner labels that still exist; GitHub retires macOS labels every
   year or so, and a retired label fails every cell on it.

6. **The release notes are written.** A title of a few words that says what the release is
   about, and a body that describes every change since the previous tag, grouped by area, with
   breaking changes first. The body is documentation for downstream maintainers: floors that
   moved, surfaces that were removed or renamed, and what replaced them. Pull request numbers
   and contributors are credited. Draft the body in a file; the release is created from it.

   ```
   git log --format='%h %s' vPREV..HEAD
   gh pr list --state merged --base main --limit 200
   ```

7. **The checklist itself is current.** If this walk changed the process, update this file
   before the tag so the tag carries the process that produced it.

## The tag

8. **Tag the tip of main.** An annotated tag, `vX.Y.Z`, with the release title as its message.
   Minor releases carry feature work or floor changes; patch releases carry fixes only.

   ```
   git tag -a vX.Y.Z -m "title"
   git push origin vX.Y.Z
   ```

   The tag is the version. Once pushed, it is not moved; a mistake is fixed by a patch release.

## The boot bundle

9. **Build the boot bundle from the tagged tree.** The bundle is the pure python of `pyre`,
   `journal`, `merlin` and `survey` plus the boot entry point, zipped by the `pyre.boot`
   family of `mm` targets. Its version comes from `git describe`, so it must be built after
   the tag exists and from a checkout at the tag.

   ```
   mm pyre.boot
   ```

   The archive lands at `{tmpdir}/release/X.Y.Z/pyre-boot.zip`; `mm builder.info` shows the
   staging directory. Check that `unzip -l` lists `__main__.py` and the four packages, and that
   `python pyre-boot.zip --help` runs.

## The GitHub release

10. **Create the release on the tag**, with the title, the notes, and the boot bundle attached.

    ```
    gh release create vX.Y.Z --title "title" --notes-file notes.md pyre-boot.zip
    ```

    Publishing the release is the event that starts the pip workflows, so the bundle is
    attached in the same command rather than uploaded afterwards. The `mm` bootstrap fetches
    `releases/download/vX.Y.Z/pyre-boot.zip`, so the asset name is fixed.

11. **Verify the bootstrap.** On a host without `pyre`, or in a fresh environment, `mm` from the
    `mm` repository downloads the bundle and runs. `python pyre-boot.zip` offers the new
    release in its menu.

## The distributions

12. **PyPI.** Publishing the release triggers `pypi-source` (the sdist) and `pypi-wheels` (one
    wheel per interpreter and platform in the matrix). Both upload through trusted publishing
    in the `pypi` environment. Watch them to completion:

    ```
    gh run list --workflow pypi-source.yaml --limit 1
    gh run list --workflow pypi-wheels.yaml --limit 1
    ```

    Then confirm that `https://pypi.org/project/pyre/` shows the version and the expected
    files, and that `pip install pyre==X.Y.Z` in a fresh environment installs a wheel that
    imports with its extensions loaded, on at least one platform. A wheel cell that fails
    leaves the others in place; fix the cell and rerun the workflow by hand
    (`workflow_dispatch`); the uploads skip files already present. A wheel that uploaded but
    does not work cannot be replaced under its name: delete the file on pypi.org (each file
    has its own delete, under the release's file list), keep the sdist, and cut a patch
    release.

13. **conda-forge.** The feedstock at `github.com/conda-forge/pyre-feedstock` builds from
    the GitHub tag tarball. The bot opens a version bump pull request within hours of the
    release; if it does not, open one by hand: `recipe/meta.yaml` gets the new version, the
    `sha256` of `https://github.com/pyre/pyre/archive/vX.Y.Z.tar.gz`, and `build: number: 0`.
    Review the recipe against the release: floors that moved (compilers, hdf5, python) belong
    in the requirements; tests that need packages the recipe does not list are excluded from
    the `ctest` invocation or the packages are added under `test: requires`. The recipe has
    listed neither `pyyaml` nor `ruamel.yaml` there, so the yaml codec tests are excluded and
    the editor tests skip themselves. Merge when the CI matrix is green, then confirm
    `conda search -c conda-forge pyre` lists the version.

## After the release

14. **Update the pins that could not be verified before.** If the bootstrap in either
    repository needed changes discovered in step 11, they land on `main` after the release
    and ride the next one.

15. **Record what the walk taught.** Anything that surprised, failed, or had to be done by
    hand goes into this file.

<!-- end of file -->
