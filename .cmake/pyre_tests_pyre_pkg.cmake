# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# pyre/primitives
#
pyre_test_python_testcase(pyre.pkg/primitives/sanity.py)
pyre_test_python_testcase(pyre.pkg/primitives/path_arithmetic.py)
pyre_test_python_testcase(pyre.pkg/primitives/path_parts.py)
pyre_test_python_testcase(pyre.pkg/primitives/path_resolution.py)
pyre_test_python_testcase(pyre.pkg/primitives/path_tuple.py)
pyre_test_python_testcase(pyre.pkg/primitives/pathhash.py)

# the {path_resolution} test requires setup+cleanup
# the setup involves making a directory with a bunchof symbolic links
set(scratch_setup
  "rm -rf scratch; mkdir scratch; cd scratch; ln -s . here; ln -s .. up"
  "ln -s cycle cycle; ln -s $(pwd)/loop loop; ln -s $(pwd)/cycle ramp"
  "ln -s tic toc; ln -s toc tic"
  )
# to cleanup, just remove the scratch directory
set(scratch_cleanup
  "rm -rf scratch"
  )
pyre_test_testcase_shell_fixture(
  "${scratch_setup}" "${scratch_cleanup}"
  pyre.pkg/primitives/path_resolution.py
  )


#
# pyre/patterns
#
pyre_test_python_testcase(pyre.pkg/patterns/sanity.py)
pyre_test_python_testcase(pyre.pkg/patterns/attributeFilter.py)
pyre_test_python_testcase(pyre.pkg/patterns/classifier.py)
pyre_test_python_testcase(pyre.pkg/patterns/extent.py)
# pyre_test_python_testcase(pyre.pkg/patterns/extent_counts.py)
pyre_test_python_testcase(pyre.pkg/patterns/named.py)
pyre_test_python_testcase(pyre.pkg/patterns/observable.py)
pyre_test_python_testcase(pyre.pkg/patterns/powerset.py)
pyre_test_python_testcase(pyre.pkg/patterns/singleton.py)
pyre_test_python_testcase(pyre.pkg/patterns/singleton_multi.py)
pyre_test_python_testcase(pyre.pkg/patterns/unique.py)
pyre_test_python_testcase(pyre.pkg/patterns/unique_base.py)
pyre_test_python_testcase(pyre.pkg/patterns/unique_derived.py)
pyre_test_python_testcase(pyre.pkg/patterns/unique_hash.py)
pyre_test_python_testcase(pyre.pkg/patterns/unique_registry.py)
pyre_test_python_testcase(pyre.pkg/patterns/unique_split.py)

#
# pyre/grid
#
pyre_test_python_testcase(pyre.pkg/grid/sanity.py)
pyre_test_python_testcase(pyre.pkg/grid/tile.py)
pyre_test_python_testcase(pyre.pkg/grid/grid.py)


#
# pyre/parsing
#
pyre_test_python_testcase(pyre.pkg/parsing/sanity.py)
pyre_test_python_testcase(pyre.pkg/parsing/exceptions.py)
pyre_test_python_testcase(pyre.pkg/parsing/scanner.py)
pyre_test_python_testcase(pyre.pkg/parsing/lexing.py)
pyre_test_python_testcase(pyre.pkg/parsing/lexing_tokenizationError.py)


#
# pyre/units
#
pyre_test_python_testcase(pyre.pkg/units/sanity.py)
pyre_test_python_testcase(pyre.pkg/units/exceptions.py)
pyre_test_python_testcase(pyre.pkg/units/one.py)
pyre_test_python_testcase(pyre.pkg/units/algebra.py)
pyre_test_python_testcase(pyre.pkg/units/parser.py)
pyre_test_python_testcase(pyre.pkg/units/formatting.py)


#
# pyre/filesystem
#
pyre_test_python_testcase(pyre.pkg/filesystem/sanity.py)
pyre_test_python_testcase(pyre.pkg/filesystem/exceptions.py)
pyre_test_python_testcase(pyre.pkg/filesystem/node.py)
pyre_test_python_testcase(pyre.pkg/filesystem/folder.py)
pyre_test_python_testcase(pyre.pkg/filesystem/filesystem.py)
pyre_test_python_testcase(pyre.pkg/filesystem/directory_walker.py)
pyre_test_python_testcase(pyre.pkg/filesystem/stat_recognizer.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_leaks.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_insert.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_insert_multiple.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_insert_badNode.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_find.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_subscripts.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_access.py)
pyre_test_python_testcase(pyre.pkg/filesystem/virtual_info.py)
pyre_test_python_testcase(pyre.pkg/filesystem/local.py)
pyre_test_python_testcase(pyre.pkg/filesystem/local_leaks.py)
pyre_test_python_testcase(pyre.pkg/filesystem/local_find.py)
pyre_test_python_testcase(pyre.pkg/filesystem/local_open.py)
pyre_test_python_testcase(pyre.pkg/filesystem/local_rootNonexistent.py)
pyre_test_python_testcase(pyre.pkg/filesystem/local_rootNotDirectory.py)
pyre_test_python_testcase(pyre.pkg/filesystem/local_make.py)
pyre_test_python_testcase(pyre.pkg/filesystem/zip.py)
pyre_test_python_testcase(pyre.pkg/filesystem/zip_open.py)
pyre_test_python_testcase(pyre.pkg/filesystem/zip_rootNonexistent.py)
pyre_test_python_testcase(pyre.pkg/filesystem/zip_rootNotZipfile.py)
pyre_test_python_testcase(pyre.pkg/filesystem/finder.py)
pyre_test_python_testcase(pyre.pkg/filesystem/finder_pattern.py)
pyre_test_python_testcase(pyre.pkg/filesystem/simple_explorer.py)
pyre_test_python_testcase(pyre.pkg/filesystem/tree_explorer.py)

# the {local_make} test modifes its local directory; so there are race conditions when running
# the test suite in parallel with all the test that explore the current directory; run it after
# the other test cases have finished
set_property(TEST pyre.pkg.filesystem.local_make.py PROPERTY DEPENDS
  pyre.pkg.filesystem.local.py ;
  pyre.pkg.filesystem.local_find.py ;
  pyre.pkg.filesystem.local_leaks.py ;
  pyre.pkg.filesystem.local_open.py ;
  pyre.pkg.filesystem.zip.py ;
  pyre.pkg.filesystem.zip_open.py
  )

# also, it requires cleanup to remove the folder created by the test case
set(filesystem_local_make_cleanup
  "rm -rf local-make"
  )
pyre_test_testcase_shell_fixture(
  "" "${filesystem_local_make_cleanup}"
  pyre.pkg/filesystem/local_make.py
  )

# the {zip} test requires setup+cleanup
# setup: zip the current directory
set(filesystem_zip_setup
  "zip -q sample.zip *"
  )
# cleanup: remove the zipfile
set(filesystem_zip_cleanup
  "rm sample.zip"
  )
pyre_test_testcase_shell_fixture(
  "${filesystem_zip_setup}" "${filesystem_zip_cleanup}"
  pyre.pkg/filesystem/zip.py
  )


#
# pyre/xml
#
pyre_test_python_testcase(pyre.pkg/xml/sanity.py)
pyre_test_python_testcase(pyre.pkg/xml/exceptions.py)
pyre_test_python_testcase(pyre.pkg/xml/reader.py)
pyre_test_python_testcase(pyre.pkg/xml/document.py)
pyre_test_python_testcase(pyre.pkg/xml/blank.py)
pyre_test_python_testcase(pyre.pkg/xml/empty.py)
pyre_test_python_testcase(pyre.pkg/xml/namespaces.py)
pyre_test_python_testcase(pyre.pkg/xml/schema.py)
pyre_test_python_testcase(pyre.pkg/xml/fs.py)
pyre_test_python_testcase(pyre.pkg/xml/fs_namespaces.py)
pyre_test_python_testcase(pyre.pkg/xml/fs_schema.py)
pyre_test_python_testcase(pyre.pkg/xml/fs_extra.py)


#
# pyre/schemata
#
pyre_test_python_testcase(pyre.pkg/schemata/sanity.py)
pyre_test_python_testcase(pyre.pkg/schemata/exceptions.py)
pyre_test_python_testcase(pyre.pkg/schemata/arrays.py)
pyre_test_python_testcase(pyre.pkg/schemata/booleans.py)
pyre_test_python_testcase(pyre.pkg/schemata/catalogs.py)
pyre_test_python_testcase(pyre.pkg/schemata/dates.py)
pyre_test_python_testcase(pyre.pkg/schemata/decimals.py)
pyre_test_python_testcase(pyre.pkg/schemata/dimensionals.py)
pyre_test_python_testcase(pyre.pkg/schemata/floats.py)
pyre_test_python_testcase(pyre.pkg/schemata/fractional.py)
pyre_test_python_testcase(pyre.pkg/schemata/inets.py)
pyre_test_python_testcase(pyre.pkg/schemata/integers.py)
pyre_test_python_testcase(pyre.pkg/schemata/istreams.py)
pyre_test_python_testcase(pyre.pkg/schemata/lists.py)
pyre_test_python_testcase(pyre.pkg/schemata/mappings.py)
pyre_test_python_testcase(pyre.pkg/schemata/ostreams.py)
pyre_test_python_testcase(pyre.pkg/schemata/paths.py)
pyre_test_python_testcase(pyre.pkg/schemata/sets.py)
pyre_test_python_testcase(pyre.pkg/schemata/strings.py)
pyre_test_python_testcase(pyre.pkg/schemata/times.py)
pyre_test_python_testcase(pyre.pkg/schemata/timestamps.py)
pyre_test_python_testcase(pyre.pkg/schemata/tuples.py)
pyre_test_python_testcase(pyre.pkg/schemata/uris.py)
pyre_test_python_testcase(pyre.pkg/schemata/typed.py)

# the {ostreams} test requires setup+cleanup
# setup: do nothing
set(schemata_ostreams_setup
  "echo nothing to do"
  )
# cleanup: remove the zipfile
set(schemata_ostreams_cleanup
  "rm output.cfg"
  )
pyre_test_testcase_shell_fixture(
  "${schemata_ostreams_setup}" "${schemata_ostreams_cleanup}"
  pyre.pkg/schemata/ostreams.py
  )


#
# pyre/constraints
#
pyre_test_python_testcase(pyre.pkg/constraints/sanity.py)
pyre_test_python_testcase(pyre.pkg/constraints/exceptions.py)
pyre_test_python_testcase(pyre.pkg/constraints/isBetween.py)
pyre_test_python_testcase(pyre.pkg/constraints/isEqual.py)
pyre_test_python_testcase(pyre.pkg/constraints/isGreater.py)
pyre_test_python_testcase(pyre.pkg/constraints/isGreaterEqual.py)
pyre_test_python_testcase(pyre.pkg/constraints/isLess.py)
pyre_test_python_testcase(pyre.pkg/constraints/isLessEqual.py)
pyre_test_python_testcase(pyre.pkg/constraints/isLike.py)
pyre_test_python_testcase(pyre.pkg/constraints/isMember.py)
pyre_test_python_testcase(pyre.pkg/constraints/isNegative.py)
pyre_test_python_testcase(pyre.pkg/constraints/isPositive.py)
pyre_test_python_testcase(pyre.pkg/constraints/isAll.py)
pyre_test_python_testcase(pyre.pkg/constraints/isAny.py)
pyre_test_python_testcase(pyre.pkg/constraints/isNot.py)
pyre_test_python_testcase(pyre.pkg/constraints/isSubset.py)
pyre_test_python_testcase(pyre.pkg/constraints/and.py)
pyre_test_python_testcase(pyre.pkg/constraints/or.py)


#
# pyre/algebraic
#
pyre_test_python_testcase(pyre.pkg/algebraic/sanity.py)
pyre_test_python_testcase(pyre.pkg/algebraic/exceptions.py)
pyre_test_python_testcase(pyre.pkg/algebraic/layout.py)
pyre_test_python_testcase(pyre.pkg/algebraic/arithmetic.py)
pyre_test_python_testcase(pyre.pkg/algebraic/ordering.py)
pyre_test_python_testcase(pyre.pkg/algebraic/boolean.py)
pyre_test_python_testcase(pyre.pkg/algebraic/dependencies.py)
pyre_test_python_testcase(pyre.pkg/algebraic/patch.py)


#
# pyre/calc
#
pyre_test_python_testcase(pyre.pkg/calc/sanity.py)
pyre_test_python_testcase(pyre.pkg/calc/exceptions.py)
pyre_test_python_testcase(pyre.pkg/calc/node_class.py)
pyre_test_python_testcase(pyre.pkg/calc/node_instance.py)
pyre_test_python_testcase(pyre.pkg/calc/node.py)
pyre_test_python_testcase(pyre.pkg/calc/substitute.py)
pyre_test_python_testcase(pyre.pkg/calc/replace.py)
pyre_test_python_testcase(pyre.pkg/calc/replace_probe.py)
pyre_test_python_testcase(pyre.pkg/calc/patch.py)
pyre_test_python_testcase(pyre.pkg/calc/explicit.py)
pyre_test_python_testcase(pyre.pkg/calc/probe.py)
pyre_test_python_testcase(pyre.pkg/calc/containers.py)
pyre_test_python_testcase(pyre.pkg/calc/reference.py)
pyre_test_python_testcase(pyre.pkg/calc/sum.py)
pyre_test_python_testcase(pyre.pkg/calc/aggregators.py)
pyre_test_python_testcase(pyre.pkg/calc/reductors.py)
pyre_test_python_testcase(pyre.pkg/calc/operations.py)
pyre_test_python_testcase(pyre.pkg/calc/algebra.py)
pyre_test_python_testcase(pyre.pkg/calc/expression.py)
pyre_test_python_testcase(pyre.pkg/calc/expression_escaped.py)
pyre_test_python_testcase(pyre.pkg/calc/expression_resolution.py)
pyre_test_python_testcase(pyre.pkg/calc/expression_circular.py)
pyre_test_python_testcase(pyre.pkg/calc/expression_syntaxerror.py)
pyre_test_python_testcase(pyre.pkg/calc/expression_typeerror.py)
pyre_test_python_testcase(pyre.pkg/calc/interpolation.py)
pyre_test_python_testcase(pyre.pkg/calc/interpolation_escaped.py)
pyre_test_python_testcase(pyre.pkg/calc/interpolation_circular.py)
pyre_test_python_testcase(pyre.pkg/calc/memo.py)
pyre_test_python_testcase(pyre.pkg/calc/memo_model.py)
pyre_test_python_testcase(pyre.pkg/calc/memo_expression.py)
pyre_test_python_testcase(pyre.pkg/calc/memo_interpolation.py)
pyre_test_python_testcase(pyre.pkg/calc/hierarchical.py)
pyre_test_python_testcase(pyre.pkg/calc/hierarchical_patch.py)
pyre_test_python_testcase(pyre.pkg/calc/hierarchical_alias.py)
pyre_test_python_testcase(pyre.pkg/calc/hierarchical_group.py)
pyre_test_python_testcase(pyre.pkg/calc/hierarchical_contains.py)
pyre_test_python_testcase(pyre.pkg/calc/model.py)


#
# pyre/descriptors
#
pyre_test_python_testcase(pyre.pkg/descriptors/sanity.py)
pyre_test_python_testcase(pyre.pkg/descriptors/booleans.py)
pyre_test_python_testcase(pyre.pkg/descriptors/decimals.py)
pyre_test_python_testcase(pyre.pkg/descriptors/floats.py)
pyre_test_python_testcase(pyre.pkg/descriptors/inets.py)
pyre_test_python_testcase(pyre.pkg/descriptors/integers.py)
pyre_test_python_testcase(pyre.pkg/descriptors/strings.py)
pyre_test_python_testcase(pyre.pkg/descriptors/dates.py)
pyre_test_python_testcase(pyre.pkg/descriptors/dimensionals.py)
pyre_test_python_testcase(pyre.pkg/descriptors/paths.py)
pyre_test_python_testcase(pyre.pkg/descriptors/times.py)
pyre_test_python_testcase(pyre.pkg/descriptors/timestamps.py)
pyre_test_python_testcase(pyre.pkg/descriptors/uris.py)
pyre_test_python_testcase(pyre.pkg/descriptors/arrays.py)
pyre_test_python_testcase(pyre.pkg/descriptors/tuples.py)
pyre_test_python_testcase(pyre.pkg/descriptors/lists.py)
pyre_test_python_testcase(pyre.pkg/descriptors/sets.py)
pyre_test_python_testcase(pyre.pkg/descriptors/istreams.py)
pyre_test_python_testcase(pyre.pkg/descriptors/ostreams.py)
pyre_test_python_testcase(pyre.pkg/descriptors/harvesting.py)
pyre_test_python_testcase(pyre.pkg/descriptors/defaults.py)
pyre_test_python_testcase(pyre.pkg/descriptors/inheritance.py)
pyre_test_python_testcase(pyre.pkg/descriptors/filtering.py)
pyre_test_python_testcase(pyre.pkg/descriptors/converters.py)

# the {ostreams} test requires setup+cleanup
# setup: do nothing
set(descriptors_ostreams_setup
  "echo nothing to do"
  )
# cleanup: remove the zipfile
set(descriptors_ostreams_cleanup
  "rm output.cfg"
  )
pyre_test_testcase_shell_fixture(
  "${descriptors_ostreams_setup}" "${descriptors_ostreams_cleanup}"
  pyre.pkg/descriptors/ostreams.py
  )


#
# pyre/records
#
pyre_test_python_testcase(pyre.pkg/records/sanity.py)
pyre_test_python_testcase(pyre.pkg/records/simple.py)
pyre_test_python_testcase(pyre.pkg/records/simple_layout.py)
pyre_test_python_testcase(pyre.pkg/records/simple_inheritance.py)
pyre_test_python_testcase(pyre.pkg/records/simple_inheritance_multi.py)
pyre_test_python_testcase(pyre.pkg/records/simple_immutable_data.py)
pyre_test_python_testcase(pyre.pkg/records/simple_immutable_kwds.py)
pyre_test_python_testcase(pyre.pkg/records/simple_immutable_conversions.py)
pyre_test_python_testcase(pyre.pkg/records/simple_immutable_validations.py)
pyre_test_python_testcase(pyre.pkg/records/simple_mutable_data.py)
pyre_test_python_testcase(pyre.pkg/records/simple_mutable_kwds.py)
pyre_test_python_testcase(pyre.pkg/records/simple_mutable_conversions.py)
pyre_test_python_testcase(pyre.pkg/records/simple_mutable_validations.py)
pyre_test_python_testcase(pyre.pkg/records/complex_layout.py)
pyre_test_python_testcase(pyre.pkg/records/complex_inheritance.py)
pyre_test_python_testcase(pyre.pkg/records/complex_inheritance_multi.py)
pyre_test_python_testcase(pyre.pkg/records/complex_immutable_data.py)
pyre_test_python_testcase(pyre.pkg/records/complex_immutable_kwds.py)
pyre_test_python_testcase(pyre.pkg/records/complex_immutable_conversions.py)
pyre_test_python_testcase(pyre.pkg/records/complex_immutable_validations.py)
pyre_test_python_testcase(pyre.pkg/records/complex_mutable_data.py)
pyre_test_python_testcase(pyre.pkg/records/complex_mutable_kwds.py)
pyre_test_python_testcase(pyre.pkg/records/complex_mutable_conversions.py)
pyre_test_python_testcase(pyre.pkg/records/complex_mutable_validations.py)
pyre_test_python_testcase(pyre.pkg/records/csv_instance.py)
pyre_test_python_testcase(pyre.pkg/records/csv_read_simple.py)
pyre_test_python_testcase(pyre.pkg/records/csv_read_partial.py)
pyre_test_python_testcase(pyre.pkg/records/csv_read_mutable.py)
pyre_test_python_testcase(pyre.pkg/records/csv_read_complex.py)
pyre_test_python_testcase(pyre.pkg/records/csv_bad_source.py)


#
# pyre/tabular
#
pyre_test_python_testcase(pyre.pkg/tabular/sanity.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_class_layout.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_class_inheritance.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_class_inheritance_multi.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_class_record.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_class_inheritance_record.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_instance.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_populate.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_columns.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_index.py)
pyre_test_python_testcase(pyre.pkg/tabular/sheet_updates.py)
pyre_test_python_testcase(pyre.pkg/tabular/view.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_class_layout.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_class_inheritance.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_instance.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_inferred.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_interval_config.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_interval.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_filter.py)
pyre_test_python_testcase(pyre.pkg/tabular/chart_sales.py)
pyre_test_python_testcase(pyre.pkg/tabular/pivot.py)
pyre_test_python_testcase(pyre.pkg/tabular/csv_instance.py)
pyre_test_python_testcase(pyre.pkg/tabular/csv_read.py)


#
# pyre/tracking
#
pyre_test_python_testcase(pyre.pkg/tracking/sanity.py)
pyre_test_python_testcase(pyre.pkg/tracking/simple.py)
pyre_test_python_testcase(pyre.pkg/tracking/lookup.py)
pyre_test_python_testcase(pyre.pkg/tracking/command.py)
pyre_test_python_testcase(pyre.pkg/tracking/file.py)
pyre_test_python_testcase(pyre.pkg/tracking/fileregion.py)
pyre_test_python_testcase(pyre.pkg/tracking/script.py)
pyre_test_python_testcase(pyre.pkg/tracking/chain.py)


#
#  pyre/codecs
#
pyre_test_python_testcase(pyre.pkg/codecs/sanity.py)
pyre_test_python_testcase(pyre.pkg/codecs/exceptions.py)
pyre_test_python_testcase(pyre.pkg/codecs/manager.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_empty.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_badRoot.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_unknownNode.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_badNode.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_badAttribute.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_package.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_packageNested.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_componentFamily.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_componentName.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_componentConditional.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_componentConditionalNested.py)
pyre_test_python_testcase(pyre.pkg/codecs/pml_sample.py)
pyre_test_python_testcase(pyre.pkg/codecs/cfg.py)
pyre_test_python_testcase(pyre.pkg/codecs/cfg_empty.py)
pyre_test_python_testcase(pyre.pkg/codecs/cfg_badToken.py)
pyre_test_python_testcase(pyre.pkg/codecs/cfg_marker.py)
pyre_test_python_testcase(pyre.pkg/codecs/cfg_open.py)
pyre_test_python_testcase(pyre.pkg/codecs/cfg_close.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_empty.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_package.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_packageNested.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_componentFamily.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_componentName.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_componentConditional.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_componentConditionalNested.py)
pyre_test_python_testcase(pyre.pkg/codecs/pfg_sample.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_empty.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_package.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_packageNested.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_componentFamily.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_componentName.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_componentConditional.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_componentConditionalNested.py)
pyre_test_python_testcase(pyre.pkg/codecs/yaml_sample.py)


#
# pyre/config
#
pyre_test_python_testcase(pyre.pkg/config/sanity.py)
pyre_test_python_testcase(pyre.pkg/config/exceptions.py)
pyre_test_python_testcase(pyre.pkg/config/events.py)
pyre_test_python_testcase(pyre.pkg/config/events_assignments.py)
pyre_test_python_testcase(pyre.pkg/config/configurator.py)
pyre_test_python_testcase(pyre.pkg/config/configurator_assignments.py)
pyre_test_python_testcase(pyre.pkg/config/configurator_load_pml.py)
pyre_test_python_testcase(pyre.pkg/config/configurator_load_cfg.py)
pyre_test_python_testcase(pyre.pkg/config/configurator_load_pfg.py)
pyre_test_python_testcase(pyre.pkg/config/command.py)
pyre_test_python_testcase(pyre.pkg/config/command_argv.py)
pyre_test_python_testcase(pyre.pkg/config/command_config.py)


#
# pyre/framework
#
pyre_test_python_testcase(pyre.pkg/framework/sanity.py)
pyre_test_python_testcase(pyre.pkg/framework/exceptions.py)
pyre_test_python_testcase(pyre.pkg/framework/slot.py)
pyre_test_python_testcase(pyre.pkg/framework/slot_instance.py)
pyre_test_python_testcase(pyre.pkg/framework/slot_algebra.py)
pyre_test_python_testcase(pyre.pkg/framework/slot_update.py)
pyre_test_python_testcase(pyre.pkg/framework/nameserver.py)
pyre_test_python_testcase(pyre.pkg/framework/nameserver_access.py)
pyre_test_python_testcase(pyre.pkg/framework/nameserver_aliases.py)
pyre_test_python_testcase(pyre.pkg/framework/fileserver.py)
pyre_test_python_testcase(pyre.pkg/framework/fileserver_uri.py)
pyre_test_python_testcase(pyre.pkg/framework/fileserver_mount.py)
pyre_test_python_testcase(pyre.pkg/framework/registrar.py)
pyre_test_python_testcase(pyre.pkg/framework/linker.py)
pyre_test_python_testcase(pyre.pkg/framework/linker_codecs.py)
pyre_test_python_testcase(pyre.pkg/framework/linker_shelves.py)
pyre_test_python_testcase(pyre.pkg/framework/externals.py)
pyre_test_python_testcase(pyre.pkg/framework/executive.py)
pyre_test_python_testcase(pyre.pkg/framework/executive_configuration.py)
pyre_test_python_testcase(pyre.pkg/framework/executive_resolve.py)
pyre_test_python_testcase(pyre.pkg/framework/executive_resolve_duplicate.py)
pyre_test_python_testcase(pyre.pkg/framework/executive_resolve_badImport.py)
pyre_test_python_testcase(pyre.pkg/framework/executive_resolve_syntaxError.py)


#
# pyre/components
#
pyre_test_python_testcase(pyre.pkg/components/sanity.py)
pyre_test_python_testcase(pyre.pkg/components/exceptions.py)
pyre_test_python_testcase(pyre.pkg/components/requirement.py)
pyre_test_python_testcase(pyre.pkg/components/role.py)
pyre_test_python_testcase(pyre.pkg/components/actor.py)
pyre_test_python_testcase(pyre.pkg/components/protocol.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_family.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_behavior.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_property.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_inheritance.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_shadow.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_inheritance_multi.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_compatibility.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_compatibility_reports.py)
pyre_test_python_testcase(pyre.pkg/components/protocol_instantiation.py)
pyre_test_python_testcase(pyre.pkg/components/component.py)
pyre_test_python_testcase(pyre.pkg/components/component_family.py)
pyre_test_python_testcase(pyre.pkg/components/component_behavior.py)
pyre_test_python_testcase(pyre.pkg/components/component_property.py)
pyre_test_python_testcase(pyre.pkg/components/component_facility.py)
pyre_test_python_testcase(pyre.pkg/components/component_inheritance.py)
pyre_test_python_testcase(pyre.pkg/components/component_shadow.py)
pyre_test_python_testcase(pyre.pkg/components/component_inheritance_multi.py)
pyre_test_python_testcase(pyre.pkg/components/component_compatibility.py)
pyre_test_python_testcase(pyre.pkg/components/component_compatibility_reports.py)
pyre_test_python_testcase(pyre.pkg/components/component_implements.py)
pyre_test_python_testcase(pyre.pkg/components/component_bad_implementations.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_registration.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_registration_inventory.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_registration_model.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_configuration.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_configuration_inheritance.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_configuration_inheritance_multi.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_binding.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_binding_import.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_binding_vfs.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_binding_conversions.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_validation.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_trait_matrix.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_private_locators.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_public_locators.py)
pyre_test_python_testcase(pyre.pkg/components/component_class_inventory.py)
pyre_test_python_testcase(pyre.pkg/components/component_defaults.py)
pyre_test_python_testcase(pyre.pkg/components/component_instantiation.py)
pyre_test_python_testcase(pyre.pkg/components/component_invocation.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_registration.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_configuration.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_configuration_constructor.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_configuration_inheritance.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_configuration_inheritance_multi.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_binding.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_binding_implicit.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_binding_configuration.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_binding_existing.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_binding_deferred.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_validation.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_private_locators.py)
pyre_test_python_testcase(pyre.pkg/components/component_instance_public_locators.py)
pyre_test_python_testcase(pyre.pkg/components/component_aliases.py --functor.μ=0.10 --gaussian.σ=0.10)
pyre_test_python_testcase(pyre.pkg/components/component_slots.py)
pyre_test_python_testcase(pyre.pkg/components/component_list.py)
pyre_test_python_testcase(pyre.pkg/components/component_dict.py)
pyre_test_python_testcase(pyre.pkg/components/quad.py)
pyre_test_python_testcase(pyre.pkg/components/monitor.py)
pyre_test_python_testcase(pyre.pkg/components/tracker.py)


#
# pyre/timers
#
pyre_test_python_testcase(pyre.pkg/timers/sanity.py)
pyre_test_python_testcase(pyre.pkg/timers/process_timer_instance.py)
pyre_test_python_testcase(pyre.pkg/timers/process_timer_example.py)
pyre_test_python_testcase(pyre.pkg/timers/wall_timer_instance.py)
pyre_test_python_testcase(pyre.pkg/timers/wall_timer_example.py)


#
# pyre/weaver
#
pyre_test_python_testcase(pyre.pkg/weaver/sanity.py)
pyre_test_python_testcase(pyre.pkg/weaver/weaver_raw.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_c.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_csh.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_cxx.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_f77.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_f90.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_html.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_latex.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_make.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_pfg.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_perl.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_python.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_sh.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_sql.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_svg.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_tex.py)
pyre_test_python_testcase(pyre.pkg/weaver/document_xml.py)
pyre_test_python_testcase(pyre.pkg/weaver/expressions_c.py)
pyre_test_python_testcase(pyre.pkg/weaver/expressions_cxx.py)
pyre_test_python_testcase(pyre.pkg/weaver/expressions_python.py)
pyre_test_python_testcase(pyre.pkg/weaver/expressions_sql.py)


#
# pyre/db
#
pyre_test_python_testcase(pyre.pkg/db/sanity.py)
pyre_test_python_testcase(pyre.pkg/db/table_declaration.py)
pyre_test_python_testcase(pyre.pkg/db/table_inheritance.py)
pyre_test_python_testcase(pyre.pkg/db/table_create.py)
pyre_test_python_testcase(pyre.pkg/db/table_references.py)
pyre_test_python_testcase(pyre.pkg/db/table_annotations.py)
pyre_test_python_testcase(pyre.pkg/db/table_delete.py)
pyre_test_python_testcase(pyre.pkg/db/table_instantiation.py)
pyre_test_python_testcase(pyre.pkg/db/table_insert.py)
pyre_test_python_testcase(pyre.pkg/db/table_update.py)
pyre_test_python_testcase(pyre.pkg/db/query_star.py)
pyre_test_python_testcase(pyre.pkg/db/query_projection.py)
pyre_test_python_testcase(pyre.pkg/db/query_projection_expressions.py)
pyre_test_python_testcase(pyre.pkg/db/query_projection_multitable.py)
pyre_test_python_testcase(pyre.pkg/db/query_restriction.py)
pyre_test_python_testcase(pyre.pkg/db/query_collation.py)
pyre_test_python_testcase(pyre.pkg/db/query_collation_explicit.py)
pyre_test_python_testcase(pyre.pkg/db/query_collation_expression.py)
pyre_test_python_testcase(pyre.pkg/db/query_inheritance.py)
pyre_test_python_testcase(pyre.pkg/db/persistent_declaration.py)


#
# pyre/ipc
#
pyre_test_python_testcase(pyre.pkg/ipc/sanity.py)
pyre_test_python_testcase(pyre.pkg/ipc/pickler.py)
pyre_test_python_testcase(pyre.pkg/ipc/pipe.py)
pyre_test_python_testcase(pyre.pkg/ipc/tcp.py)
pyre_test_python_testcase(pyre.pkg/ipc/pickler_over_pipe.py)
pyre_test_python_testcase(pyre.pkg/ipc/pickler_over_tcp.py)
pyre_test_python_testcase(pyre.pkg/ipc/scheduler.py)
pyre_test_python_testcase(pyre.pkg/ipc/scheduler_instantiation.py)
pyre_test_python_testcase(pyre.pkg/ipc/scheduler_alarms.py)
pyre_test_python_testcase(pyre.pkg/ipc/selector.py)
pyre_test_python_testcase(pyre.pkg/ipc/selector_instantiation.py)
pyre_test_python_testcase(pyre.pkg/ipc/selector_alarms.py)
pyre_test_python_testcase(pyre.pkg/ipc/selector_signals.py)
pyre_test_python_testcase(pyre.pkg/ipc/selector_pickler_over_pipe.py)
pyre_test_python_testcase(pyre.pkg/ipc/selector_pickler_over_tcp.py)


#
# pyre/nexus
#
pyre_test_python_testcase(pyre.pkg/nexus/sanity.py)
pyre_test_python_testcase(pyre.pkg/nexus/node.py)
pyre_test_python_testcase(pyre.pkg/nexus/node_instantiation.py)
pyre_test_python_testcase(pyre.pkg/nexus/node_signals.py)
pyre_test_python_testcase(pyre.pkg/nexus/pool.py)
pyre_test_python_testcase(pyre.pkg/nexus/pool.py --tasks=4 --team.size=2)


#
# pyre/platforms
#
pyre_test_python_testcase(pyre.pkg/platforms/sanity.py)
pyre_test_python_testcase(pyre.pkg/platforms/host.py)


#
# pyre/shells
#
pyre_test_python_testcase(pyre.pkg/shells/sanity.py)
pyre_test_python_testcase(pyre.pkg/shells/application_sanity.py)
pyre_test_python_testcase(pyre.pkg/shells/application_instantiation.py)
pyre_test_python_testcase(pyre.pkg/shells/application_inheritance.py)
pyre_test_python_testcase(pyre.pkg/shells/application_namespace.py)
pyre_test_python_testcase(pyre.pkg/shells/script_sanity.py)
pyre_test_python_testcase(pyre.pkg/shells/script_instantiation.py)
pyre_test_python_testcase(pyre.pkg/shells/fork_sanity.py)
pyre_test_python_testcase(pyre.pkg/shells/fork_instantiation.py)
pyre_test_python_testcase(pyre.pkg/shells/daemon_sanity.py)
pyre_test_python_testcase(pyre.pkg/shells/daemon_instantiation.py)
pyre_test_python_testcase(pyre.pkg/shells/colors256.py)
pyre_test_python_testcase(pyre.pkg/shells/colors24bit.py)
pyre_test_python_testcase(pyre.pkg/shells/script_launching.py)
pyre_test_python_testcase(pyre.pkg/shells/fork_launching.py)
pyre_test_python_testcase(pyre.pkg/shells/daemon_launching.py)


#
# pyre/externals
#
#pyre_test_python_testcase(pyre.pkg/externals/sanity.py)
#pyre_test_python_testcase(pyre.pkg/externals/locate.py)
#pyre_test_python_testcase(pyre.pkg/externals/blas.py)
#pyre_test_python_testcase(pyre.pkg/externals/blas.py --blas=gslcblas)
#pyre_test_python_testcase(pyre.pkg/externals/blas.py --blas=atlas)
#pyre_test_python_testcase(pyre.pkg/externals/blas.py --blas=openblas)
#pyre_test_python_testcase(pyre.pkg/externals/blas.py --blas=gslcblas\\\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/blas.py --blas=atlas\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/blas.py --blas=openblas\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/cython.py)
#pyre_test_python_testcase(pyre.pkg/externals/cython.py --cython=cython2)
#pyre_test_python_testcase(pyre.pkg/externals/cython.py --cython=cython3)
#pyre_test_python_testcase(pyre.pkg/externals/cython.py --cython=cython2\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/cython.py --cython=cython3\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/gcc.py)
#pyre_test_python_testcase(pyre.pkg/externals/gcc.py --gcc=gcc5)
#pyre_test_python_testcase(pyre.pkg/externals/gcc.py --gcc=gcc5\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/gsl.py)
#pyre_test_python_testcase(pyre.pkg/externals/gsl.py --gsl=default)
#pyre_test_python_testcase(pyre.pkg/externals/gsl.py --gsl=default\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/hdf5.py)
#pyre_test_python_testcase(pyre.pkg/externals/hdf5.py --hdf5=default)
#pyre_test_python_testcase(pyre.pkg/externals/hdf5.py --hdf5=default\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/mpi.py)
#pyre_test_python_testcase(pyre.pkg/externals/mpi.py --mpi=mpich)
#pyre_test_python_testcase(pyre.pkg/externals/mpi.py --mpi=openmpi)
#pyre_test_python_testcase(pyre.pkg/externals/mpi.py --mpi=mpich\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/mpi.py --mpi=openmpi\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/postgres.py)
#pyre_test_python_testcase(pyre.pkg/externals/postgres.py --postgres=default)
#pyre_test_python_testcase(pyre.pkg/externals/postgres.py --postgres=default\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/python.py)
#pyre_test_python_testcase(pyre.pkg/externals/python.py --python=python3)
#pyre_test_python_testcase(pyre.pkg/externals/python.py --python=python2)
#pyre_test_python_testcase(pyre.pkg/externals/python.py --python=python3\#python35)
#pyre_test_python_testcase(pyre.pkg/externals/python.py --python=python2\#python27)
#pyre_test_python_testcase(pyre.pkg/externals/python.py --python=python3\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/python.py --python=python2\#mga)
#pyre_test_python_testcase(pyre.pkg/externals/vtk.py)
#pyre_test_python_testcase(pyre.pkg/externals/vtk.py --vtk=vtk5)
#pyre_test_python_testcase(pyre.pkg/externals/vtk.py --vtk=vtk6)
#pyre_test_python_testcase(pyre.pkg/externals/vtk.py --vtk=vtk6\#mga)


#
# pyre/flow
#
pyre_test_python_testcase(pyre.pkg/flow/sanity.py)


#
# pyre/pyre
#
pyre_test_python_testcase(pyre.pkg/pyre/sanity.py)
pyre_test_python_testcase(pyre.pkg/pyre/loadConfiguration.py)
pyre_test_python_testcase(pyre.pkg/pyre/resolve.py)
pyre_test_python_testcase(pyre.pkg/pyre/spaces.py)
pyre_test_python_testcase(pyre.pkg/pyre/defaults.py)
pyre_test_python_testcase(pyre.pkg/pyre/play.py)
pyre_test_python_testcase(pyre.pkg/pyre/headers.py)


# end of file
